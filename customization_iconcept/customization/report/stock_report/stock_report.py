# Copyright (c) 2026, Frontier Softech and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
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
        {"label": "Item Category", "fieldname": "custom_item_category", "fieldtype": "Data", "width": 130},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": "Part Number", "fieldname": "item_code", "fieldtype": "Data", "width": 130},
        {"label": "Sub LOB", "fieldname": "custom_item_sub_lob", "fieldtype": "Data", "width": 130},
        {"label": "Stock Status", "fieldname": "stock_status", "fieldtype": "Data", "width": 130},
        {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 120},
    ]


def get_conditions(filters):
    conditions = ""

    if filters.get("company"):
        conditions += " AND w.company = %(company)s"

    if filters.get("warehouse"):
        conditions += " AND b.warehouse = %(warehouse)s"

    if filters.get("item_group"):
        conditions += " AND i.item_group = %(item_group)s"

    if filters.get("item_code"):
        conditions += " AND b.item_code = %(item_code)s"

    if filters.get("item_category"):
        conditions += " AND i.custom_item_category = %(item_category)s"

    if filters.get("sub_lob"):
        conditions += " AND i.custom_item_sub_lob = %(sub_lob)s"

    return conditions


def get_data(filters):

    conditions = get_conditions(filters)

    stock_data = frappe.db.sql(f"""
        SELECT
            b.item_code,
            b.warehouse,
            b.actual_qty,
            w.company,
            i.item_group,
            i.custom_item_category,
            i.item_name,
            i.custom_item_sub_lob
        FROM `tabBin` b
        LEFT JOIN `tabWarehouse` w ON w.name = b.warehouse
        LEFT JOIN `tabItem` i ON i.name = b.item_code
        WHERE 1=1 {conditions}
    """, filters, as_dict=1)

    pending_data = frappe.db.sql("""
        SELECT
            poi.item_code,
            po.set_warehouse AS warehouse,
            SUM(poi.qty - poi.received_qty) AS pending_qty
        FROM `tabPurchase Order Item` poi
        JOIN `tabPurchase Order` po ON poi.parent = po.name
        WHERE po.docstatus = 1
        GROUP BY poi.item_code, po.set_warehouse
    """, as_dict=1)

    pending_map = {(d.item_code, d.warehouse): d.pending_qty for d in pending_data}

    data = []

    for row in stock_data:

        key = (row.item_code, row.warehouse)

        actual_row = {
            "company": row.company,
            "warehouse": row.warehouse,
            "item_group": row.item_group,
            "custom_item_category": row.custom_item_category,
            "item_code": row.item_code,
            "item_name": row.item_name,
            "custom_item_sub_lob": row.custom_item_sub_lob,
            "stock_status": "Actual Qty",
            "qty": flt(row.actual_qty)
        }

        pending_row = {
            "company": row.company,
            "warehouse": row.warehouse,
            "item_group": row.item_group,
            "custom_item_category": row.custom_item_category,
            "item_code": row.item_code,
            "item_name": row.item_name,
            "custom_item_sub_lob": row.custom_item_sub_lob,
            "stock_status": "Pending Qty",
            "qty": flt(pending_map.get(key, 0))
        }

        if not filters.get("stock_status") or filters.get("stock_status") == "Actual Qty":
            data.append(actual_row)

        if not filters.get("stock_status") or filters.get("stock_status") == "Pending Qty":
            data.append(pending_row)

    return data
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
#         {"label": "Item Category", "fieldname": "custom_item_category", "fieldtype": "Data", "width": 130},
#         {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Link", "options": "Item", "width": 150},
#         {"label": "Part Number", "fieldname": "item_code", "fieldtype": "Data", "width": 130},
#         {"label": "Sub LOB", "fieldname": "custom_item_sub_lob", "fieldtype": "Data", "width": 130},
#         {"label": "Stock Status", "fieldname": "stock_status", "fieldtype": "Data", "width": 130},
#         {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 120},
#     ]


# def get_data(filters):

#     # Actual Stock from Bin
#     stock_data = frappe.db.sql("""
#         SELECT
#             b.item_code,
#             b.warehouse,
#             b.actual_qty,
#             w.company,
#         	i.item_group,
#         	i.custom_item_category,
#         	i.item_name,
#         	i.custom_item_sub_lob                   
#         FROM `tabBin` b
#         LEFT JOIN `tabWarehouse` w ON w.name = b.warehouse
#         LEFT JOIN `tabItem` i ON i.name = b.item_code
#     """, as_dict=1)

#     # Pending Qty from Purchase Order
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

#         # Row 1 → Actual Qty
#         data.append({
# 		    "company": row.company,
# 		    "warehouse": row.warehouse,
# 		    "item_group": row.item_group,
# 		    "custom_item_category": row.custom_item_category,
# 		    "item_code": row.item_code,
# 		    "item_name": row.item_name,
# 		    "custom_item_sub_lob": row.custom_item_sub_lob,
# 		    "stock_status": "Actual Qty",
# 		    "qty": flt(row.actual_qty)
# 		})

#         # Row 2 → Pending Qty
#         data.append({
# 		    "company": row.company,
# 		    "warehouse": row.warehouse,
# 		    "item_group": row.item_group,
# 		    "custom_item_category": row.custom_item_category,
# 		    "item_code": row.item_code,
# 		    "item_name": row.item_name,
# 		    "custom_item_sub_lob": row.custom_item_sub_lob,
# 		    "stock_status": "Pending Qty",
# 		    "qty": flt(pending_map.get(key, 0))
# 		})

#     return data