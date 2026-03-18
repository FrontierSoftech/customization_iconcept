# Copyright (c) 2026, Frontier Softech and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
import frappe
from frappe.utils import today, getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "ID", "fieldname": "name", "fieldtype": "Link", "options": "Serial No", "width": 160},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 160},
        {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 160},
        {"label": "Item Category", "fieldname": "custom_item_category", "fieldtype": "Link", "options": "Item Category", "width": 160},
        {"label": "Item Sub LOB", "fieldname": "custom_item_sub_lob", "fieldtype": "Link", "options": "Item Sub Lob", "width": 160},
        {"label": "Brand", "fieldname": "brand", "fieldtype": "Link", "options": "Brand", "width": 160},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 160},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 160},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 160},
        {"label": "Ageing", "fieldname": "ageing", "fieldtype": "Int", "width": 160},
    ]


def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("warehouse"):
        conditions += " AND sn.warehouse IN %(warehouse)s"
        values["warehouse"] = tuple(filters.get("warehouse"))

    if filters.get("item_code"):
        conditions += " AND sn.item_code IN %(item_code)s"
        values["item_code"] = tuple(filters.get("item_code"))

    if filters.get("item_group"):
        conditions += " AND i.item_group IN %(item_group)s"
        values["item_group"] = tuple(filters.get("item_group"))

    if filters.get("item_category"):
        conditions += " AND i.custom_item_category IN %(item_category)s"
        values["item_category"] = tuple(filters.get("item_category"))

    if filters.get("item_sub_lob"):
        conditions += " AND i.custom_item_sub_lob IN %(item_sub_lob)s"
        values["item_sub_lob"] = tuple(filters.get("item_sub_lob"))

    if filters.get("brand"):
        conditions += " AND i.brand IN %(brand)s"
        values["brand"] = tuple(filters.get("brand"))

    serials = frappe.db.sql(f"""
        SELECT
            sn.name,
            sn.item_code,
            i.item_group,
            i.custom_item_category,
            i.custom_item_sub_lob,
            i.brand,                
            sn.warehouse,
            sn.status,
            sn.company,
            sn.creation,
            DATEDIFF(CURDATE(), DATE(sn.creation)) AS ageing
        FROM
            `tabSerial No` sn
        LEFT JOIN 
            `tabItem` i ON sn.item_code = i.item_code
        WHERE
            sn.status = 'Active'
            {conditions}
    """.format(conditions=conditions), values, as_dict=True)

    return serials