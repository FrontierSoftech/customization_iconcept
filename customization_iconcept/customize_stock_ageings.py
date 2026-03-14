import frappe
from collections.abc import Iterator
from erpnext.stock.report.stock_ageing import stock_ageing as original_report
from frappe.utils import cint, date_diff, flt, get_datetime
original_report.FIFOSlots._FIFOSlots__get_warehouse_conditions = patched_get_warehouse_conditions

def patched_execute(filters=None):
    # Convert filters to frappe._dict for easier access
    filters = frappe._dict(filters or {})

    # --- MultiSelectList filter normalization ---
    multi_fields = ["warehouse", "item_code", "brand", "item_group", "item_category", "item_sub_lob"]
    for field in multi_fields:
        if filters.get(field):
            if isinstance(filters.get(field), str):
                filters[field] = [filters.get(field)]
            elif isinstance(filters.get(field), list):
                pass
            else:
                filters[field] = []

    # --- Original report logic ---
    to_date = filters["to_date"]
    filters.ranges = [num.strip() for num in filters.range.split(",") if num.strip().isdigit()]
    columns = original_report.get_columns(filters)
    item_details = original_report.FIFOSlots(filters).generate()
    data = original_report.format_report_data(filters, item_details, to_date)
    chart_data = original_report.get_chart_data(data, filters)

    return columns, data, None, chart_data

def __get_item_query(self) -> str:
	item_table = frappe.qb.DocType("Item")

	item = frappe.qb.from_(item_table).select(
		item_table.name,
		item_table.item_name,
		item_table.description,
		item_table.stock_uom,
		item_table.brand,
		item_table.item_group,
		item_table.has_serial_no,
		item_table.valuation_method,
	)

	# MULTI ITEM
	if self.filters.get("item_code"):
		item = item.where(item_table.name.isin(self.filters.get("item_code")))

	# MULTI BRAND
	if self.filters.get("brand"):
		item = item.where(item_table.brand.isin(self.filters.get("brand")))

	# MULTI ITEM GROUP
	if self.filters.get("item_group"):
		item = item.where(item_table.item_group.isin(self.filters.get("item_group")))

	return item

def __get_stock_ledger_entries(self) -> Iterator[dict]:
	sle = frappe.qb.DocType("Stock Ledger Entry")
	item = self.__get_item_query()  # used as derived table in sle query
	to_date = get_datetime(self.filters.get("to_date") + " 23:59:59")
	sle_query = (
		frappe.qb.from_(sle)
		.from_(item)
		.select(
			item.name,
			item.item_name,
			item.item_group,
			item.brand,
			item.description,
			item.stock_uom,
			item.has_serial_no,
			item.valuation_method,
			sle.actual_qty,
			sle.stock_value_difference,
			sle.valuation_rate,
			sle.posting_date,
			sle.voucher_type,
			sle.voucher_no,
			sle.serial_no,
			sle.batch_no,
			sle.qty_after_transaction,
			sle.serial_and_batch_bundle,
			sle.warehouse,
		)
		.where(
			(sle.item_code == item.name)
			& (sle.company == self.filters.get("company"))
			& (sle.posting_datetime <= to_date)
			& (sle.is_cancelled != 1)
		)
	)
	if self.filters.get("warehouse"):
		sle_query = sle_query.where(sle.warehouse.isin(self.filters.get("warehouse")))
	elif self.filters.get("warehouse_type"):
		warehouses = frappe.get_all(
			"Warehouse",
			filters={"warehouse_type": self.filters.get("warehouse_type"), "is_group": 0},
			pluck="name",
		)
		if warehouses:
			sle_query = sle_query.where(sle.warehouse.isin(warehouses))
	sle_query = sle_query.orderby(sle.posting_datetime, sle.creation)
	return sle_query.run(as_dict=True, as_iterator=True)

def __get_warehouse_conditions(self, sle, sle_query):
	warehouse = frappe.qb.DocType("Warehouse")

	selected_warehouses = self.filters.get("warehouse")
	if not selected_warehouses:
		return sle_query

	if isinstance(selected_warehouses, str):
		selected_warehouses = [selected_warehouses]

	all_warehouses = []

	for wh in selected_warehouses:
		lft, rgt = frappe.db.get_value("Warehouse", wh, ["lft", "rgt"])

		results = (
			frappe.qb.from_(warehouse)
			.select(warehouse.name)
			.where((warehouse.lft >= lft) & (warehouse.rgt <= rgt))
			.run()
		)

		all_warehouses.extend([x[0] for x in results])

	# remove duplicates
	all_warehouses = list(set(all_warehouses))

	return sle_query.where(sle.warehouse.isin(all_warehouses))

def __get_bundle_wise_serial_nos(self) -> dict:
	bundle = frappe.qb.DocType("Serial and Batch Bundle")
	entry = frappe.qb.DocType("Serial and Batch Entry")
	query = (
		frappe.qb.from_(bundle)
		.join(entry)
		.on(bundle.name == entry.parent)
		.select(bundle.name, entry.serial_no)
		.where(
			(bundle.docstatus == 1)
			& (entry.serial_no.isnotnull())
			& (bundle.company == self.filters.get("company"))
			& (bundle.posting_date <= self.filters.get("to_date"))
		)
	)
	for field in ["item_code"]:
		if self.filters.get(field):
			query = query.where(bundle[field] == self.filters.get(field))
	if self.filters.get("warehouse"):
		query = query.where(bundle.warehouse.isin(self.filters.get("warehouse")))
	bundle_wise_serial_nos = frappe._dict({})
	for bundle_name, serial_no in query.run():
		bundle_wise_serial_nos.setdefault(bundle_name, []).append(serial_no)
	return bundle_wise_serial_nos