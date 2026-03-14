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
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 160},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 160},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 160},
        {"label": "Ageing", "fieldname": "ageing", "fieldtype": "Int", "width": 160},
    ]


def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("warehouse"):
        conditions += " AND warehouse IN %(warehouse)s"
        values["warehouse"] = tuple(filters.get("warehouse"))

    if filters.get("item_code"):
        conditions += " AND item_code IN %(item_code)s"
        values["item_code"] = tuple(filters.get("item_code"))

    serials = frappe.db.sql(f"""
        SELECT
            name,
            item_code,
            warehouse,
            status,
            company,
            creation,
            DATEDIFF(CURDATE(), DATE(creation)) AS ageing
        FROM
            `tabSerial No`
        WHERE
            status = 'Active'
            {conditions}
    """.format(conditions=conditions), values, as_dict=True)

    return serials