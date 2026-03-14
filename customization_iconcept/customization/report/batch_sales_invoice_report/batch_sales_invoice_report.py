# Copyright (c) 2026, Frontier Softech and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
import frappe
from frappe.utils import getdate, formatdate

def execute(filters=None):
    if not filters:
        filters = {}

    conditions = []
    if filters.get("company"):
        conditions.append(f"si.company = '{filters.get('company')}'")
    if filters.get("from_date"):
        conditions.append(f"si.posting_date >= '{filters.get('from_date')}'")
    if filters.get("to_date"):
        conditions.append(f"si.posting_date <= '{filters.get('to_date')}'")
    if filters.get("customer"):
        customers = "', '".join(filters.get("customer"))
        conditions.append(f"si.customer IN ('{customers}')")   
    if filters.get("set_warehouse"):
        warehouses = "', '".join(filters.get("set_warehouse"))
        conditions.append(f"si.set_warehouse IN ('{warehouses}')")   
    if filters.get("item_group"):
        item_groups = "', '".join(filters.get("item_group"))
        conditions.append(f"it.item_group IN ('{item_groups}')")   
    if filters.get("item_category"):
        item_categories = "', '".join(filters.get("item_category"))
        conditions.append(f"it.custom_item_category IN ('{item_categories}')")   
    # if filters.get("sub_lob"):
    #     sub_lobs = "', '".join(filters.get("sub_lob"))
    #     conditions.append(f"it.sub_lob IN ('{sub_lobs}')")   

    # if filters.get("customer"):
    #     conditions.append(f"si.customer = '{filters.get('customer')}'")
    # if filters.get("set_warehouse"):
    #     conditions.append(f"si.set_warehouse = '{filters.get('set_warehouse')}'")

    conditions_sql = " AND ".join(conditions)
    if conditions_sql:
        conditions_sql = " AND " + conditions_sql

    query = f"""
        SELECT
            si.company AS "Company Name",
            si.name AS "Voucher Number",
            si.posting_date AS "Date",
            si.branch AS "Voucher Type",
            si.customer AS "Party Name",
            st.sales_person AS "Salesman",
            sii.item_name AS "Item Name",
            sii.item_code AS "Item Part No",
            sii.item_code AS "Item Alias",
            it.custom_item_category AS "Item Category",
            it.item_group AS "Item Group",
            sii.warehouse AS "Godown",
            sbe.serial_no AS "Item Batch/Serial No",
            sbe.batch_no AS "Billed Qty",
            sii.qty AS "Rate",
            sii.rate AS "Batch Rate",
            sii.amount AS "Amount"

        FROM `tabSales Invoice` si

        LEFT JOIN `tabSales Invoice Item` sii
            ON si.name = sii.parent

        LEFT JOIN `tabSerial and Batch Bundle` sbb
            ON sbb.name = sii.serial_and_batch_bundle

        LEFT JOIN `tabSerial and Batch Entry` sbe
            ON sbe.parent = sbb.name
        
        JOIN
			`tabItem` it ON sii.item_code = it.item_code
        
        LEFT JOIN `tabSales Team` st ON si.name = st.parent

        WHERE si.docstatus = 1 {conditions_sql}

        ORDER BY si.posting_date DESC
    """

    data = frappe.db.sql(query, as_dict=True)

    columns = [
    {"label": "Company Name", "fieldname": "Company Name", "fieldtype": "Link", "options": "Company", "width": 150},
    {"label": "Voucher Number", "fieldname": "Voucher Number", "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
    {"label": "Date", "fieldname": "Date", "fieldtype": "Date", "width": 100},
    {"label": "Voucher Type", "fieldname": "Voucher Type", "fieldtype": "Data", "width": 120},
    {"label": "Party Name", "fieldname": "Party Name", "fieldtype": "Link", "options": "Customer", "width": 180},
    {"label": "Salesman", "fieldname": "Salesman", "fieldtype": "Link", "options": "Sales Person", "width": 150},
    {"label": "Item Name", "fieldname": "Item Name", "fieldtype": "Data", "width": 200},
    {"label": "Item Part No", "fieldname": "Item Part No", "fieldtype": "Link", "options": "Item", "width": 150},
    {"label": "Item Alias", "fieldname": "Item Alias", "fieldtype": "Data", "width": 150},
    {"label": "Item Category", "fieldname": "Item Category", "fieldtype": "Link", "options": "Item Group", "width": 150},
    {"label": "Item Group", "fieldname": "Item Group", "fieldtype": "Link", "options": "Item Group", "width": 150},
    {"label": "Godown", "fieldname": "Godown", "fieldtype": "Link", "options": "Warehouse", "width": 150},
    {"label": "Item Batch/Serial No", "fieldname": "Item Batch/Serial No", "fieldtype": "Data", "width": 200},
    {"label": "Billed Qty", "fieldname": "Billed Qty", "fieldtype": "Data", "width": 120},
    {"label": "Rate", "fieldname": "Rate", "fieldtype": "Float", "width": 120},
    {"label": "Batch Rate", "fieldname": "Batch Rate", "fieldtype": "Currency", "width": 120},
    {"label": "Amount", "fieldname": "Amount", "fieldtype": "Currency", "width": 120},
    ]

    return columns, data