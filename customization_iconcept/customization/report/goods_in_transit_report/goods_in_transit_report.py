# Copyright (c) 2026, Frontier Softech and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
# import frappe
# from frappe.utils import flt


# def execute(filters=None):
#     filters = frappe._dict(filters or {})

#     # IMPORTANT: safe LIKE pattern (fixes your error)
#     filters.git_pattern = "Goods In Transit%"

#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data


# def get_columns():
#     return [
#         {"label": "Company Name", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
#         {"label": "Godown", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
#         {"label": "Branch Warehouse", "fieldname": "custom_branch_warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
#         {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 130},
#         {"label": "Item Category", "fieldname": "custom_item_category", "fieldtype": "Link", "options": "Item Category", "width": 130},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 150},
#         {"label": "Part Number", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 130},
#         {"label": "Sub LOB", "fieldname": "custom_item_sub_lob", "fieldtype": "Link", "options": "Item Sub Lob", "width": 130},
#         {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 120}
#     ]


# def get_data(filters):

#     # convert IN filters safely
#     for key in ["item_group", "item_code", "item_category", "sub_lob"]:
#         if filters.get(key):
#             filters[key] = tuple(filters.get(key))

#     # ---------------- STOCK CONDITIONS ----------------
#     conditions = get_conditions()

#     # ---------------- STOCK DATA ----------------
#     stock_data = frappe.db.sql(f"""
#         SELECT
#             b.item_code,
#             b.warehouse,
#             b.actual_qty AS qty,
#             w.company,
#             i.item_group,
#             i.custom_item_category,
#             i.item_name,
#             i.custom_item_sub_lob,
#             'Stock' AS stock_status
#         FROM `tabBin` b
#         LEFT JOIN `tabWarehouse` w ON w.name = b.warehouse
#         LEFT JOIN `tabItem` i ON i.name = b.item_code
#         WHERE 1=1 {conditions}
#     """, {
#         **filters,
#         "git_pattern": filters.git_pattern
#     }, as_dict=1)

#     # ---------------- INTERNAL TRANSFER ----------------
#     transfer_data = frappe.db.sql("""
#         SELECT
#             sii.item_code,
#             si.custom_branch_warehouse AS warehouse,
#             SUM(sii.qty - sii.delivered_qty) AS transfer_qty
#         FROM `tabSales Invoice Item` sii
#         JOIN `tabSales Invoice` si ON sii.parent = si.name
#         LEFT JOIN `tabPurchase Invoice` pi 
#             ON pi.inter_company_invoice_reference = si.name
#         WHERE
#             si.docstatus = 1
#             AND si.is_internal_customer = 1
#             AND pi.name IS NULL
#         GROUP BY sii.item_code, si.custom_branch_warehouse
#     """, {
#         "git_pattern": filters.git_pattern
#     }, as_dict=1)

#     # ---------------- MERGE DATA ----------------
#     transfer_map = {}
#     for t in transfer_data:
#         transfer_map[(t.item_code, t.warehouse)] = t.transfer_qty

#     result = []
#     for s in stock_data:
#         s.transfer_qty = flt(transfer_map.get((s.item_code, s.warehouse), 0))
#         result.append(s)

#     return result


# def get_conditions():
#     conditions = ""

#     # SAFE LIKE (no raw % in SQL string → prevents your error)
#     conditions += " AND b.warehouse LIKE %(git_pattern)s"

#     return conditions


# import frappe
# from frappe.utils import flt


# def execute(filters=None):
#     filters = frappe._dict(filters or {})

#     filters.git_pattern = "Goods In Transit%"

#     columns = get_columns()
#     data = get_data(filters)

#     return columns, data


# def get_columns():
#     return [
#         {"label": "Company Name", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 120},
#         {"label": "Godown", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
#         {"label": "Branch Warehouse", "fieldname": "custom_branch_warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 120},
#         {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 130},
#         {"label": "Item Category", "fieldname": "custom_item_category", "fieldtype": "Link", "options": "Item Category", "width": 130},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 150},
#         {"label": "Part Number", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 130},
#         {"label": "Sub LOB", "fieldname": "custom_item_sub_lob", "fieldtype": "Link", "options": "Item Sub Lob", "width": 130},
#         {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 120},
#     ]


# def get_data(filters):

#     # ---------------- BASE STOCK (BIN) ----------------
#     stock_data = frappe.db.sql("""
#         SELECT
#             b.item_code,
#             b.warehouse,
#             b.actual_qty AS qty,
#             w.company,
#             i.item_group,
#             i.custom_item_category,
#             i.item_name,
#             i.custom_item_sub_lob
#         FROM `tabBin` b
#         LEFT JOIN `tabWarehouse` w ON w.name = b.warehouse
#         LEFT JOIN `tabItem` i ON i.name = b.item_code
#         WHERE b.warehouse LIKE %(git_pattern)s
#     """, {
#         "git_pattern": filters.git_pattern
#     }, as_dict=1)

#     # ---------------- SALES INVOICE SPLIT ----------------
#     si_data = frappe.db.sql("""
#         SELECT
#             sii.item_code,
#             si.custom_branch_warehouse,
#             SUM(sii.qty - sii.delivered_qty) AS qty
#         FROM `tabSales Invoice Item` sii
#         JOIN `tabSales Invoice` si ON si.name = sii.parent
#         LEFT JOIN `tabPurchase Invoice` pi 
#             ON pi.inter_company_invoice_reference = si.name
#         WHERE
#             si.docstatus = 1
#             AND si.is_internal_customer = 1
#             AND pi.name IS NULL
#         GROUP BY
#             sii.item_code,
#             si.custom_branch_warehouse
#     """, as_dict=1)

#     # ---------------- MAP SALES QTY BY ITEM ----------------
#     si_map = {}
#     for r in si_data:
#         si_map.setdefault(r.item_code, []).append(r)

#     # ---------------- SPLIT STOCK ----------------
#     result = []

#     for s in stock_data:

#         item_entries = si_map.get(s.item_code)

#         # if no sales invoice mapping → show as single row
#         if not item_entries:
#             row = s.copy()
#             row.custom_branch_warehouse = None
#             result.append(row)
#             continue

#         total_si_qty = sum(x.qty for x in item_entries)

#         for x in item_entries:
#             row = s.copy()
#             row.custom_branch_warehouse = x.custom_branch_warehouse

#             # proportional split logic
#             if total_si_qty:
#                 row.qty = flt(s.qty * (x.qty / total_si_qty))
#             else:
#                 row.qty = 0

#             result.append(row)

#     return result

import frappe
from frappe.utils import flt


def execute(filters=None):
    filters = frappe._dict(filters or {})

    filters.git_pattern = filters.get("git_pattern") or "Goods In Transit%"
    filters.from_date = filters.get("from_date")
    filters.to_date = filters.get("to_date")

    columns = get_columns()
    data = get_data(filters)

    return columns, data


# ---------------- COLUMNS ----------------
def get_columns():
    return [
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Posting Time", "fieldname": "posting_time", "fieldtype": "Time", "width": 90},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 120},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 120},
        {"label": "Branch Warehouse", "fieldname": "custom_branch_warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 120},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 130},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 150},
        {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 130},
        {"label": "Item Category", "fieldname": "custom_item_category", "fieldtype": "Link", "options": "Item Category", "width": 130},
        {"label": "Sub LOB", "fieldname": "custom_item_sub_lob", "fieldtype": "Link", "options": "Item Sub Lob", "width": 130},
        {"label": "In Qty", "fieldname": "in_qty", "fieldtype": "Float", "width": 100},
        {"label": "Out Qty", "fieldname": "out_qty", "fieldtype": "Float", "width": 100},
        {"label": "Balance Qty", "fieldname": "balance_qty", "fieldtype": "Float", "width": 120},
        {"label": "Voucher Type", "fieldname": "voucher_type", "fieldtype": "Data", "width": 120},
        {"label": "Voucher No", "fieldname": "voucher_no", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150},
    ]


# ---------------- DATA ----------------
def get_data(filters):

    conditions = ""
    values = {
        "git_pattern": filters.git_pattern,
    }

    # ---------------- DATE FILTER ----------------
    if filters.from_date and filters.to_date:
        conditions += " AND sle.posting_date BETWEEN %(from_date)s AND %(to_date)s"
        values.update({
            "from_date": filters.from_date,
            "to_date": filters.to_date
        })

    # ---------------- MULTISELECT FILTERS ----------------

    if filters.company:
        conditions += " AND w.company IN %(company)s"
        values["company"] = tuple(filters.company)

    if filters.item_code:
        conditions += " AND sle.item_code IN %(item_code)s"
        values["item_code"] = tuple(filters.item_code)

    if filters.item_group:
        conditions += " AND i.item_group IN %(item_group)s"
        values["item_group"] = tuple(filters.item_group)

    if filters.custom_item_category:
        conditions += " AND i.custom_item_category IN %(custom_item_category)s"
        values["custom_item_category"] = tuple(filters.custom_item_category)

    if filters.custom_item_sub_lob:
        conditions += " AND i.custom_item_sub_lob IN %(custom_item_sub_lob)s"
        values["custom_item_sub_lob"] = tuple(filters.custom_item_sub_lob)

    if filters.voucher_type:
        conditions += " AND sle.voucher_type IN %(voucher_type)s"
        values["voucher_type"] = tuple(filters.voucher_type)

    if filters.voucher_no:
        conditions += " AND sle.voucher_no IN %(voucher_no)s"
        values["voucher_no"] = tuple(filters.voucher_no)

    # ---------------- SLE DATA ----------------
    sle_data = frappe.db.sql(f"""
        SELECT
            sle.item_code,
            sle.warehouse,
            sle.posting_date,
            sle.posting_time,
            sle.actual_qty,
            sle.voucher_type,
            sle.voucher_no,
            w.company,
            i.item_name,
            i.item_group,
            i.custom_item_category,
            i.custom_item_sub_lob
        FROM `tabStock Ledger Entry` sle
        LEFT JOIN `tabWarehouse` w ON w.name = sle.warehouse
        LEFT JOIN `tabItem` i ON i.name = sle.item_code
        WHERE
            sle.is_cancelled = 0
            AND sle.warehouse LIKE %(git_pattern)s
            {conditions}
        ORDER BY
            sle.item_code,
            sle.warehouse,
            sle.posting_date,
            sle.posting_time
    """, values, as_dict=1)

    # ---------------- SALES INVOICE MAP ----------------
    si_map = frappe._dict()

    si_data = frappe.db.sql("""
        SELECT
            name,
            custom_branch_warehouse
        FROM `tabSales Invoice`
        WHERE docstatus = 1
    """, as_dict=1)

    for si in si_data:
        si_map[si.name] = si.custom_branch_warehouse

    # ---------------- RUNNING BALANCE ----------------
    balance_map = {}
    result = []

    for row in sle_data:
        key = (row.item_code, row.warehouse)

        balance_map.setdefault(key, 0)
        balance_map[key] += flt(row.actual_qty)

        new_row = {
            "posting_date": row.posting_date,
            "posting_time": row.posting_time,
            "company": row.company,
            "warehouse": row.warehouse,
            "item_code": row.item_code,
            "item_name": row.item_name,
            "item_group": row.item_group,
            "custom_item_category": row.custom_item_category,
            "custom_item_sub_lob": row.custom_item_sub_lob,
            "in_qty": row.actual_qty if row.actual_qty > 0 else 0,
            "out_qty": abs(row.actual_qty) if row.actual_qty < 0 else 0,
            "balance_qty": balance_map[key],
            "voucher_type": row.voucher_type,
            "voucher_no": row.voucher_no,
        }

        # Branch Warehouse only for Sales Invoice
        if row.voucher_type == "Sales Invoice":
            new_row["custom_branch_warehouse"] = si_map.get(row.voucher_no)
        else:
            new_row["custom_branch_warehouse"] = None

        result.append(new_row)

    return result