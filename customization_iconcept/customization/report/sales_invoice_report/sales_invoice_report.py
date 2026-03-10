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
    if filters.get("customer_name"):
        conditions.append(f"c.customer_name = '{filters.get('customer_name')}'")
    if filters.get("customer_group"):
        conditions.append(f"c.customer_group = '{filters.get('customer_group')}'")
    if filters.get("set_warehouse"):
        conditions.append(f"si.set_warehouse = '{filters.get('set_warehouse')}'")

    conditions_sql = " AND ".join(conditions)
    if conditions_sql:
        conditions_sql = " AND " + conditions_sql

    query = f"""
        SELECT
            si.company AS "Company Name",
            si.set_warehouse AS "Item Godown",
            si.name AS "Voucher Number",
            si.posting_date AS "Date",
            c.customer_name AS "Party Name",
            c.customer_group AS "Party Group",
            si.custom_party_name AS "Mailing Name",
            c.mobile_no AS "Contact No",
            it.brand AS "Brand Name",
            sii.item_name AS "Item Name",
            sii.item_code AS "Item Part No",
            it.item_group AS "Item Group",
            it.custom_item_category AS "Item Category",
            it.custom_item_sub_lob AS "Sub LOB",
            sii.qty AS "Actual Quantity",
            sii.rate AS "Basic Rate",
            sii.rate AS "Batch Rate",
            sii.amount AS "Amount",
            si.base_grand_total AS "Company Final",
            si.custom_day AS "Day",
            si.custom_month AS "Month",
            si.custom_quarter AS "QTR",
            si.billing_address_gstin AS "Bill Type",
            si.customer AS "Cust Nature",
            si.custom_internal_branch AS "Payment Mode",
            si.custom_branch_warehouse AS "Trade In",
            st.sales_person AS "Salesman",
            st.sales_person AS "Combo LOB Discount",
            sii.price_list_rate AS "MRP",
            sii.discount_percentage AS "Discount",
            sii.rate AS "SaleRate",
            c.custom_profession AS "Profession of a customer",
            c.gstin AS "GST Number",
            c.gst_category AS "GST Type"
        FROM
            `tabSales Invoice` si
        JOIN
            `tabSales Invoice Item` sii ON si.name = sii.parent
        JOIN
            `tabCustomer` c ON si.customer = c.name
        JOIN
			`tabItem` it ON sii.item_code = it.item_code
        LEFT JOIN
			`tabSales Team` st ON si.name = st.parent
        WHERE
            si.docstatus = 1
            {conditions_sql}
        ORDER BY si.posting_date DESC
    """

    data = frappe.db.sql(query, as_dict=True)

    columns = [
        {"label": "Company Name", "fieldname": "Company Name", "fieldtype": "Data", "width": 150},
        {"label": "Item Godown", "fieldname": "Item Godown", "fieldtype": "Data", "width": 150},
        {"label": "Voucher Number", "fieldname": "Voucher Number", "fieldtype": "Data", "width": 120},
        {"label": "Date", "fieldname": "Date", "fieldtype": "Date", "width": 100},
        {"label": "Party Name", "fieldname": "Party Name", "fieldtype": "Data", "width": 150},
        {"label": "Party Group", "fieldname": "Party Group", "fieldtype": "Data", "width": 120},
        {"label": "Mailing Name", "fieldname": "Mailing Name", "fieldtype": "Data", "width": 150},
        {"label": "Contact No", "fieldname": "Contact No", "fieldtype": "Data", "width": 120},
        {"label": "Brand Name", "fieldname": "Brand Name", "fieldtype": "Data", "width": 120},
        {"label": "Item Name", "fieldname": "Item Name", "fieldtype": "Data", "width": 150},
        {"label": "Item Part No", "fieldname": "Item Part No", "fieldtype": "Data", "width": 120},
        {"label": "Item Group", "fieldname": "Item Group", "fieldtype": "Data", "width": 120},
        {"label": "Item Category", "fieldname": "Item Category", "fieldtype": "Data", "width": 120},
        {"label": "Sub LOB", "fieldname": "Sub LOB", "fieldtype": "Data", "width": 120},
        {"label": "Actual Quantity", "fieldname": "Actual Quantity", "fieldtype": "Float", "width": 100},
        {"label": "Basic Rate", "fieldname": "Basic Rate", "fieldtype": "Currency", "width": 100},
        {"label": "Batch Rate", "fieldname": "Batch Rate", "fieldtype": "Currency", "width": 100},
        {"label": "Amount", "fieldname": "Amount", "fieldtype": "Currency", "width": 100},
        {"label": "Company Final", "fieldname": "Company Final", "fieldtype": "Currency", "width": 120},
        {"label": "Day", "fieldname": "Day", "fieldtype": "Int", "width": 100},
        {"label": "Month", "fieldname": "Month", "fieldtype": "Int", "width": 100},
        {"label": "QTR", "fieldname": "QTR", "fieldtype": "Int", "width": 100},
        {"label": "Bill Type", "fieldname": "Bill Type", "fieldtype": "Data", "width": 100},
        {"label": "Cust Nature", "fieldname": "Cust Nature", "fieldtype": "Data", "width": 100},
        {"label": "Payment Mode", "fieldname": "Payment Mode", "fieldtype": "Data", "width": 100},
        {"label": "Trade In", "fieldname": "Trade In", "fieldtype": "Data", "width": 100},
        {"label": "Salesman", "fieldname": "Salesman", "fieldtype": "Data", "width": 120},
        {"label": "Combo LOB Discount", "fieldname": "Combo LOB Discount", "fieldtype": "Data", "width": 120},
        {"label": "MRP", "fieldname": "MRP", "fieldtype": "Data", "width": 120},
        {"label": "Discount", "fieldname": "Discount", "fieldtype": "Percent", "width": 80},
        {"label": "SaleRate", "fieldname": "SaleRate", "fieldtype": "Currency", "width": 100},
        {"label": "Profession of a customer", "fieldname": "Profession of a customer", "fieldtype": "Data", "width": 100},
        {"label": "GST Number", "fieldname": "GST Number", "fieldtype": "Data", "width": 120},
        {"label": "GST Type", "fieldname": "GST Type", "fieldtype": "Data", "width": 100},
    ]

    return columns, data