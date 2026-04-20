# Copyright (c) 2026, Frontier Softech and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
# import frappe
# from frappe.utils import flt


# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)

#     return columns, data


# def get_columns():
#     return [
#         {"label": "Company Name", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
#         {"label": "Godown", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
#         {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 130},
#         {"label": "Item Category", "fieldname": "custom_item_category", "fieldtype": "Link", "options": "Item Category", "width": 130},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 150},
#         {"label": "Part Number", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 130},
#         {"label": "Sub LOB", "fieldname": "custom_item_sub_lob", "fieldtype": "Link", "options": "Item Sub Lob", "width": 130},
#         {"label": "Stock Status", "fieldname": "stock_status", "fieldtype": "Data", "width": 130},
#         {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 120},
#         {"label": "Serial Number", "fieldname": "serial_no", "fieldtype": "Data", "width": 150},
#     ]


# def get_conditions(filters):
#     conditions = ""

#     if filters.get("company"):
#         conditions += " AND w.company = %(company)s"
    
#     if filters.get("warehouse"):
#         conditions += " AND b.warehouse IN %(warehouse)s"

#     if filters.get("item_group"):
#         conditions += " AND i.item_group IN %(item_group)s"

#     if filters.get("item_code"):
#         conditions += " AND b.item_code IN %(item_code)s"

#     if filters.get("item_category"):
#         conditions += " AND i.custom_item_category IN %(item_category)s"

#     if filters.get("sub_lob"):
#         conditions += " AND i.custom_item_sub_lob IN %(sub_lob)s"

#     return conditions


# def get_data(filters):

#     # Convert filters to tuple for SQL IN
#     for key in ["warehouse", "item_group", "item_code", "item_category", "sub_lob"]:
#         if filters.get(key):
#             filters[key] = tuple(filters.get(key))

#     conditions = get_conditions(filters)

#     # ✅ Stock + Serial Data
#     stock_data = frappe.db.sql(f"""
#         SELECT
#             b.item_code,
#             b.warehouse,
#             b.actual_qty,
#             w.company,
#             i.item_group,
#             i.custom_item_category,
#             i.item_name,
#             i.custom_item_sub_lob,
#             i.has_serial_no,
#             s.name AS serial_no
#         FROM `tabBin` b
#         LEFT JOIN `tabWarehouse` w ON w.name = b.warehouse
#         LEFT JOIN `tabItem` i ON i.name = b.item_code
#         LEFT JOIN `tabSerial No` s 
#             ON s.item_code = b.item_code 
#             AND s.warehouse = b.warehouse
#             AND s.status = 'Active'
#         WHERE 1=1 {conditions}
#     """, filters, as_dict=1)

#     # ✅ Pending (In-Transit)
#     pending_data = frappe.db.sql("""
#         SELECT
#             poi.item_code,
#             po.set_warehouse AS warehouse,
#             SUM(poi.qty - poi.received_qty) AS pending_qty
#         FROM `tabPurchase Order Item` poi
#         JOIN `tabPurchase Order` po ON poi.parent = po.name
#         WHERE po.docstatus = 1
#         GROUP BY poi.item_code, po.set_warehouse
#     """, as_dict=1)

#     pending_map = {(d.item_code, d.warehouse): d.pending_qty for d in pending_data}

#     data = []
#     added_in_transit = set()

#     for row in stock_data:

#         key = (row.item_code, row.warehouse)
#         pending_qty = flt(pending_map.get(key, 0))

#         is_serialized = row.has_serial_no

#         # ✅ Handle qty logic
#         if is_serialized:
#             actual_qty = 1 if row.serial_no else 0
#         else:
#             actual_qty = flt(row.actual_qty)

#         # ✅ Actual Row
#         actual_row = {
#             "company": row.company,
#             "warehouse": row.warehouse,
#             "item_group": row.item_group,
#             "custom_item_category": row.custom_item_category,
#             "item_code": row.item_code,
#             "item_name": row.item_name,
#             "custom_item_sub_lob": row.custom_item_sub_lob,
#             "stock_status": "Actual Qty",
#             "qty": actual_qty,
#             "serial_no": row.serial_no if is_serialized else ''
#         }

#         # ✅ In-Transit Row (only once)
#         pending_row = {
#             "company": row.company,
#             "warehouse": row.warehouse,
#             "item_group": row.item_group,
#             "custom_item_category": row.custom_item_category,
#             "item_code": row.item_code,
#             "item_name": row.item_name,
#             "custom_item_sub_lob": row.custom_item_sub_lob,
#             "stock_status": "In-Transit",
#             "qty": pending_qty,
#             "serial_no": ''
#         }

#         # ✅ Append Actual Qty
#         if (not filters.get("stock_status") or filters.get("stock_status") == "Actual Qty") and actual_qty != 0:
#             data.append(actual_row)

#         # ✅ Append In-Transit (no duplicates)
#         if (not filters.get("stock_status") or filters.get("stock_status") == "In-Transit") and pending_qty != 0:
#             if key not in added_in_transit:
#                 data.append(pending_row)
#                 added_in_transit.add(key)

#     return data



# import frappe
# from frappe.utils import flt


# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)

#     return columns, data


# def get_columns():
#     return [
#         {"label": "Company Name", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
#         {"label": "Godown", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
#         {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 130},
#         {"label": "Item Category", "fieldname": "custom_item_category", "fieldtype": "Link","options": "Item Category", "width": 130},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 150},
#         {"label": "Part Number", "fieldname": "item_code", "fieldtype": "Link", "options": "Item","width": 130},
#         {"label": "Sub LOB", "fieldname": "custom_item_sub_lob", "fieldtype": "Link", "options": "Item Sub Lob", "width": 130},
#         {"label": "Stock Status", "fieldname": "stock_status", "fieldtype": "Data", "width": 130},
#         {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 120},
#     ]


# def get_conditions(filters):
#     conditions = ""

#     if filters.get("company"):
#         conditions += " AND w.company = %(company)s"
    
#     if filters.get("warehouse"):
#         conditions += " AND b.warehouse IN %(warehouse)s"

#     if filters.get("item_group"):
#         conditions += " AND i.item_group IN %(item_group)s"

#     if filters.get("item_code"):
#         conditions += " AND b.item_code IN %(item_code)s"

#     if filters.get("item_category"):
#         conditions += " AND i.custom_item_category IN %(item_category)s"

#     if filters.get("sub_lob"):
#         conditions += " AND i.custom_item_sub_lob IN %(sub_lob)s"

#     # if filters.get("warehouse"):
#     #     conditions += " AND b.warehouse = %(warehouse)s"

#     # if filters.get("item_group"):
#     #     conditions += " AND i.item_group = %(item_group)s"

#     # if filters.get("item_code"):
#     #     conditions += " AND b.item_code = %(item_code)s"

#     # if filters.get("item_category"):
#     #     conditions += " AND i.custom_item_category = %(item_category)s"

#     # if filters.get("sub_lob"):
#     #     conditions += " AND i.custom_item_sub_lob = %(sub_lob)s"

#     return conditions


# def get_data(filters):

#     for key in ["warehouse", "item_group", "item_code", "item_category", "sub_lob"]:
#         if filters.get(key):
#             filters[key] = tuple(filters.get(key))

#     conditions = get_conditions(filters)

#     stock_data = frappe.db.sql(f"""
#         SELECT
#             b.item_code,
#             b.warehouse,
#             b.actual_qty,
#             w.company,
#             i.item_group,
#             i.custom_item_category,
#             i.item_name,
#             i.custom_item_sub_lob
#         FROM `tabBin` b
#         LEFT JOIN `tabWarehouse` w ON w.name = b.warehouse
#         LEFT JOIN `tabCompany` c ON c.name = w.company
#         LEFT JOIN `tabItem` i ON i.name = b.item_code              
#         WHERE 1=1 {conditions} AND b.warehouse != CONCAT('Goods In Transit - ', c.abbr)
#     """, filters, as_dict=1)

#     pending_data = frappe.db.sql("""
#         SELECT
#             poi.item_code,
#             po.set_warehouse AS warehouse,
#             SUM(poi.qty - poi.received_qty) AS pending_qty
#         FROM `tabPurchase Order Item` poi
#         JOIN `tabPurchase Order` po ON poi.parent = po.name
#         WHERE po.docstatus = 1
#         GROUP BY poi.item_code, po.set_warehouse
#     """, as_dict=1)

#     pending_map = {(d.item_code, d.warehouse): d.pending_qty for d in pending_data}

#     data = []

#     for row in stock_data:

#         key = (row.item_code, row.warehouse)
#         pending_qty = flt(pending_map.get(key, 0))
#         actual_qty = flt(row.actual_qty)

#         actual_row = {
#             "company": row.company,
#             "warehouse": row.warehouse,
#             "item_group": row.item_group,
#             "custom_item_category": row.custom_item_category,
#             "item_code": row.item_code,
#             "item_name": row.item_name,
#             "custom_item_sub_lob": row.custom_item_sub_lob,
#             "stock_status": "Actual Qty",
#             "qty": flt(row.actual_qty)
#         }

#         pending_row = {
#             "company": row.company,
#             "warehouse": row.warehouse,
#             "item_group": row.item_group,
#             "custom_item_category": row.custom_item_category,
#             "item_code": row.item_code,
#             "item_name": row.item_name,
#             "custom_item_sub_lob": row.custom_item_sub_lob,
#             "stock_status": "In-Transit",
#             "qty": flt(pending_map.get(key, 0))
#         }

#         if (not filters.get("stock_status") or filters.get("stock_status") == "Actual Qty") and actual_qty != 0:
#             data.append(actual_row)

#         if (not filters.get("stock_status") or filters.get("stock_status") == "In-Transit") and pending_qty != 0:
#             data.append(pending_row)

#     return data




# import frappe
# from frappe.utils import flt

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     return [
#         {"label": "Company Name", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
#         {"label": "Godown", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
#         {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 130},
#         {"label": "Item Category", "fieldname": "custom_item_category", "fieldtype": "Link","options": "Item Category", "width": 130},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 150},
#         {"label": "Part Number", "fieldname": "item_code", "fieldtype": "Link", "options": "Item","width": 130},
#         {"label": "Sub LOB", "fieldname": "custom_item_sub_lob", "fieldtype": "Link", "options": "Item Sub Lob", "width": 130},
#         {"label": "Stock Status", "fieldname": "stock_status", "fieldtype": "Data", "width": 130},
#         {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 120},
#     ]

# def get_conditions(filters):
#     conditions = ""
#     if filters.get("company"):
#         conditions += " AND w.company = %(company)s"
#     if filters.get("warehouse"):
#         conditions += " AND b.warehouse IN %(warehouse)s"
#     if filters.get("item_group"):
#         conditions += " AND i.item_group IN %(item_group)s"
#     if filters.get("item_code"):
#         conditions += " AND b.item_code IN %(item_code)s"
#     if filters.get("item_category"):
#         conditions += " AND i.custom_item_category IN %(item_category)s"
#     if filters.get("sub_lob"):
#         conditions += " AND i.custom_item_sub_lob IN %(sub_lob)s"
#     return conditions

# def get_data(filters):
#     # convert filters to tuples for SQL IN clauses
#     for key in ["warehouse", "item_group", "item_code", "item_category", "sub_lob"]:
#         if filters.get(key):
#             filters[key] = tuple(filters.get(key))

#     conditions = get_conditions(filters)

#     # ---------------- STOCK DATA ----------------
#     stock_data = frappe.db.sql(f"""
#         SELECT
#             b.item_code,
#             b.warehouse,
#             b.actual_qty,
#             w.company,
#             i.item_group,
#             i.custom_item_category,
#             i.item_name,
#             i.custom_item_sub_lob
#         FROM `tabBin` b
#         LEFT JOIN `tabWarehouse` w ON w.name = b.warehouse
#         LEFT JOIN `tabItem` i ON i.name = b.item_code              
#         WHERE 1=1 {conditions}
#     """, filters, as_dict=1)

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
        
#     """, as_dict=1)

#     transfer_map = {(d.item_code, d.warehouse): flt(d.transfer_qty) for d in transfer_data}

#     # ---------------- PENDING PO ----------------
#     pending_data = frappe.db.sql("""
#         SELECT
#             poi.item_code,
#             po.set_warehouse AS warehouse,
#             SUM(poi.qty - poi.received_qty) AS pending_qty
#         FROM `tabPurchase Order Item` poi
#         JOIN `tabPurchase Order` po ON poi.parent = po.name
#         WHERE po.docstatus = 1
#         GROUP BY poi.item_code, po.set_warehouse
#     """, as_dict=1)

#     pending_map = {(d.item_code, d.warehouse): flt(d.pending_qty) for d in pending_data}

#     data = []
#     all_keys = set()

#     # ---------------- MERGE STOCK + TRANSFERS ----------------
#     for row in stock_data:
#         key = (row.item_code, row.warehouse)
#         all_keys.add(key)

#         transfer_qty = flt(transfer_map.get(key, 0))
#         actual_qty = flt(row.actual_qty) + transfer_qty

#         if (not filters.get("stock_status") or filters.get("stock_status") == "Actual Qty") and actual_qty != 0:
#             data.append({
#                 "company": row.company,
#                 "warehouse": row.warehouse,
#                 "item_group": row.item_group,
#                 "custom_item_category": row.custom_item_category,
#                 "item_code": row.item_code,
#                 "item_name": row.item_name,
#                 "custom_item_sub_lob": row.custom_item_sub_lob,
#                 "stock_status": "Actual Qty",
#                 "qty": actual_qty
#             })

#         # Add pending PO if exists
#         pending_qty = flt(pending_map.get(key, 0))
#         if (not filters.get("stock_status") or filters.get("stock_status") == "In-Transit") and pending_qty != 0:
#             data.append({
#                 "company": row.company,
#                 "warehouse": row.warehouse,
#                 "item_group": row.item_group,
#                 "custom_item_category": row.custom_item_category,
#                 "item_code": row.item_code,
#                 "item_name": row.item_name,
#                 "custom_item_sub_lob": row.custom_item_sub_lob,
#                 "stock_status": "In-Transit",
#                 "qty": pending_qty
#             })

#     # ---------------- HANDLE TRANSFERS NOT IN STOCK ----------------
#     for key, transfer_qty in transfer_map.items():
#         if key not in all_keys and transfer_qty != 0:
#             item_code, warehouse = key
#             item = frappe.db.get_value("Item", item_code, ["item_name", "item_group", "custom_item_category", "custom_item_sub_lob"], as_dict=1)
#             warehouse_doc = frappe.db.get_value("Warehouse", warehouse, ["company"], as_dict=1)
            
#             if filters.get("company") and warehouse_doc and warehouse_doc.company != filters["company"]:
#                 continue
#             if filters.get("warehouse") and warehouse not in filters["warehouse"]:
#                 continue
#             if filters.get("item_group") and item and item.item_group not in filters["item_group"]:
#                 continue
#             if filters.get("item_code") and item_code not in filters["item_code"]:
#                 continue
#             if filters.get("item_category") and item and item.custom_item_category not in filters["item_category"]:
#                 continue
#             if filters.get("sub_lob") and item and item.custom_item_sub_lob not in filters["sub_lob"]:
#                 continue

#             if not filters.get("stock_status") or filters.get("stock_status") == "Actual Qty":
#                 data.append({
#                     "company": warehouse_doc.company if warehouse_doc else "",
#                     "warehouse": warehouse,
#                     "item_group": item.item_group if item else "",
#                     "custom_item_category": item.custom_item_category if item else "",
#                     "item_code": item_code,
#                     "item_name": item.item_name if item else "",
#                     "custom_item_sub_lob": item.custom_item_sub_lob if item else "",
#                     "stock_status": "Actual Qty",
#                     "qty": transfer_qty
#                 })

    

#     return data

import frappe
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        {"label": "Company Name", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Godown", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
        {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 130},
        {"label": "Item Category", "fieldname": "custom_item_category", "fieldtype": "Link", "options": "Item Category", "width": 130},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 150},
        {"label": "Part Number", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 130},
        {"label": "Sub LOB", "fieldname": "custom_item_sub_lob", "fieldtype": "Link", "options": "Item Sub Lob", "width": 130},
        {"label": "Stock Status", "fieldname": "stock_status", "fieldtype": "Data", "width": 130},
        {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 120},
    ]


def get_conditions(filters):
    conditions = ""

    if filters.get("company"):
        conditions += " AND w.company = %(company)s"

    if filters.get("warehouse"):
        conditions += " AND b.warehouse IN %(warehouse)s"

    if filters.get("item_group"):
        conditions += " AND i.item_group IN %(item_group)s"

    if filters.get("item_code"):
        conditions += " AND b.item_code IN %(item_code)s"

    if filters.get("item_category"):
        conditions += " AND i.custom_item_category IN %(item_category)s"

    if filters.get("sub_lob"):
        conditions += " AND i.custom_item_sub_lob IN %(sub_lob)s"

    if filters.get("from_date") and filters.get("to_date"):
        conditions += """ AND EXISTS (
            SELECT 1 FROM `tabStock Ledger Entry` sle
            WHERE sle.item_code = b.item_code
            AND sle.warehouse = b.warehouse
            AND sle.posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND sle.is_cancelled = 0
        )"""

    return conditions


def get_data(filters):

    if not filters:
        filters = {}

    # Convert list filters to tuple for SQL IN
    for key in ["warehouse", "item_group", "item_code", "item_category", "sub_lob"]:
        if filters.get(key):
            filters[key] = tuple(filters.get(key))

    conditions = get_conditions(filters)

    stock_data = frappe.db.sql(f"""
        SELECT
            b.item_code,
            b.warehouse,
            b.actual_qty,
            b.ordered_qty,
            w.company,
            i.item_group,
            i.custom_item_category,
            i.item_name,
            i.custom_item_sub_lob
        FROM `tabBin` b
        LEFT JOIN `tabWarehouse` w ON w.name = b.warehouse
        LEFT JOIN `tabCompany` c ON c.name = w.company
        LEFT JOIN `tabItem` i ON i.name = b.item_code              
        WHERE 1=1 {conditions}
        AND b.warehouse != CONCAT('Goods In Transit - ', c.abbr)
    """, filters, as_dict=1)

    data = []

    for row in stock_data:

        actual_qty = flt(row.actual_qty)
        in_transit_qty = flt(row.ordered_qty)

        actual_row = {
            "company": row.company,
            "warehouse": row.warehouse,
            "item_group": row.item_group,
            "custom_item_category": row.custom_item_category,
            "item_code": row.item_code,
            "item_name": row.item_name,
            "custom_item_sub_lob": row.custom_item_sub_lob,
            "stock_status": "Actual Qty",
            "qty": actual_qty
        }

        in_transit_row = {
            "company": row.company,
            "warehouse": row.warehouse,
            "item_group": row.item_group,
            "custom_item_category": row.custom_item_category,
            "item_code": row.item_code,
            "item_name": row.item_name,
            "custom_item_sub_lob": row.custom_item_sub_lob,
            "stock_status": "In-Transit",
            "qty": in_transit_qty
        }

        # Append based on filter
        if (not filters.get("stock_status") or filters.get("stock_status") == "Actual Qty") and actual_qty != 0:
            data.append(actual_row)

        if (not filters.get("stock_status") or filters.get("stock_status") == "In-Transit") and in_transit_qty != 0:
            data.append(in_transit_row)

    return data