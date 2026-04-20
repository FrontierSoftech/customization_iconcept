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

    # --- STATIC CONDITIONS ---
    conditions = []
    if filters.get("company"):
        conditions.append(f"si.company = '{filters.get('company')}'")
    if filters.get("from_date"):
        conditions.append(f"si.posting_date >= '{filters.get('from_date')}'")
    if filters.get("to_date"):
        conditions.append(f"si.posting_date <= '{filters.get('to_date')}'")
    if filters.get("customer_name"):
        customers = "', '".join(filters.get("customer_name"))
        conditions.append(f"si.customer IN ('{customers}')")    
    if filters.get("customer_group"):
        groups = "', '".join(filters.get("customer_group"))
        conditions.append(f"c.customer_group IN ('{groups}')")
    if filters.get("set_warehouse"):
        warehouses = "', '".join(filters.get("set_warehouse"))
        conditions.append(f"si.set_warehouse IN ('{warehouses}')")
    if filters.get("item_group"):
        item_groups = "', '".join(filters.get("item_group"))
        conditions.append(f"it.item_group IN ('{item_groups}')")
    if filters.get("sub_lob"):
        sub_lobs = "', '".join(filters.get("sub_lob"))
        conditions.append(f"it.custom_item_sub_lob IN ('{sub_lobs}')")
    if filters.get("item_category"):
        item_categories = "', '".join(filters.get("item_category"))
        conditions.append(f"it.custom_item_category IN ('{item_categories}')")

    conditions_sql = " AND ".join(conditions)
    if conditions_sql:
        conditions_sql = " AND " + conditions_sql

    # --- FETCH DYNAMIC COLUMNS ---
    # 1. Accounts (Bank/Cash, not group)
    accounts = frappe.db.get_list(
        "Account",
        filters={
            "account_type": ["in", ["Bank", "Cash"]],
            "is_group": 0,
            "company": filters.get("company")  # Filter by selected company
        },
        fields=["name"]
    )

    account_columns = []
    account_map = []  # For fetching values
    for acc in accounts:
        account_columns.append({
            "label": acc['name'],
            "fieldname": acc['name'],
            "fieldtype": "Currency",
            "width": 120
        })
        account_map.append(acc['name'])

    # --- DYNAMIC CUSTOMER COLUMNS ---
    descendants = frappe.db.get_list(
        "Customer Group",
        filters={"parent_customer_group": "Finance Lender"},
        fields=["name"]
    )
    # descendant_names = [d["name"] for d in descendants]
    # finance_customers = frappe.db.get_list(
    #     "Customer",
    #     filters={"customer_group": ["in", descendant_names]},
    #     fields=["name"]
    # )
    customer_columns = []
    customer_map = []
    for cust in descendants:
        customer_columns.append({
            "label": cust['name'],
            "fieldname": cust['name'],
            "fieldtype": "Currency",
            "width": 120
        })
        customer_map.append(cust['name'])

    # --- BASE QUERY ---
    query = f"""
        SELECT
            si.company AS "Company Name",
            si.set_warehouse AS "Item Godown",
            si.name AS "Voucher Number",
            si.posting_date AS "Date",
            c.customer_name AS "Party Name",
            si.custom_party_name AS "Mailing Name",
            c.mobile_no AS "Contact No",
            it.brand AS "Brand Name",
            sii.item_name AS "Item Name",
            sii.item_code AS "Item Part No",
            it.item_group AS "Item Group",
            it.custom_item_category AS "Item Category",
            it.custom_item_sub_lob AS "Sub LOB",
            sii.qty AS "Actual Quantity",
            (sii.qty * sle.incoming_rate) AS "Buying Amount",
            sii.net_rate AS "Basic Rate",
            sii.taxable_value AS "Taxable Amount",
            (sii.taxable_value - (sii.qty * sle.incoming_rate)) AS "Gross Profit",
            ((sii.taxable_value - (sii.qty * sle.incoming_rate)) / sii.taxable_value * 100) AS "Gross Profit Percent",
            si.custom_day AS "Day",
            si.custom_week AS "Week",
            si.custom_month AS "Month",
            si.custom_quarter AS "QTR",
            st.sales_person AS "Salesman",
            sii.price_list_rate AS "MRP",
            sii.discount_percentage AS "Discount",
            '' AS "NEED Purchase Price",
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
        JOIN `tabStock Ledger Entry` sle 
             ON sle.item_code = sii.item_code 
             AND sle.voucher_no = si.name
             AND sle.warehouse = si.set_warehouse
        WHERE
            si.docstatus = 1
            AND c.customer_group NOT IN ('Internal Customer', 'Company Associates')
            {conditions_sql}
        ORDER BY si.posting_date DESC
    """

    data = frappe.db.sql(query, as_dict=True)

    # --- FETCH CHILD TABLE AMOUNTS ---
    for row in data:
        payments = frappe.db.get_all(
            "Finance Lender Options",
            filters={"parent": row["Voucher Number"]},
            fields=["finance_lender", "amount"]
        )
        advance = frappe.get_all(
            "Sales Invoice Advance",
            filters={"parent": row["Voucher Number"]},
            fields=["allocated_amount"]
        )
        # Sum all amounts for this invoice
        row["Advance"] = sum(p["allocated_amount"] for p in advance) if advance else 0
        # Account amounts
        for acc_name in account_map:
            row[acc_name] = sum(p["amount"] for p in payments if p["finance_lender"] == acc_name)

        # Customer (finance lender) amounts
        for cust_name in customer_map:
            row[cust_name] = sum(p["amount"] for p in payments if frappe.db.get_value("Customer", p["finance_lender"], "customer_group") == cust_name)

    # Replace None/empty with "N/A"
    for row in data:
        for key, val in row.items():
            if val is None or val == "":
                row[key] = "N/A"

    # --- DEFINE COLUMNS ---
    columns = [
        {"label": "Company Name", "fieldname": "Company Name", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Item Godown", "fieldname": "Item Godown", "fieldtype": "Link", "options": "Warehouse", "width": 150},
        {"label": "Voucher Number", "fieldname": "Voucher Number", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
        {"label": "Date", "fieldname": "Date", "fieldtype": "Date", "width": 100},
        {"label": "Party Name", "fieldname": "Party Name", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Mailing Name", "fieldname": "Mailing Name", "fieldtype": "Data", "width": 150},
        # {"label": "Contact No", "fieldname": "Contact No", "fieldtype": "Data", "width": 120},
        {"label": "Brand Name", "fieldname": "Brand Name", "fieldtype": "Data", "width": 120},
        {"label": "Item Name", "fieldname": "Item Name", "fieldtype": "Data", "width": 150},
        {"label": "Item Part No", "fieldname": "Item Part No", "fieldtype": "Link", "options": "Item", "width": 120},
        {"label": "Item Group", "fieldname": "Item Group", "fieldtype": "Link", "options": "Item Group", "width": 120},
        {"label": "Item Category", "fieldname": "Item Category", "fieldtype": "Link", "options": "Item Category", "width": 120},
        {"label": "Sub LOB", "fieldname": "Sub LOB", "fieldtype": "Link", "options": "Item Sub Lob", "width": 120},
        {"label": "Actual Quantity", "fieldname": "Actual Quantity", "fieldtype": "Float", "width": 100},
        {"label": "Buying Amount", "fieldname": "Buying Amount", "fieldtype": "Currency", "width": 100},
        {"label": "Basic Rate", "fieldname": "Basic Rate", "fieldtype": "Currency", "width": 100},
        {"label": "Taxable Amount", "fieldname": "Taxable Amount", "fieldtype": "Currency", "width": 100},
        {"label": "Gross Profit", "fieldname": "Gross Profit", "fieldtype": "Currency", "width": 100},
        {"label": "Gross Profit Percent", "fieldname": "Gross Profit Percent", "fieldtype": "Percent", "width": 100},
        {"label": "Day", "fieldname": "Day", "fieldtype": "Data", "width": 100},
        {"label": "Week", "fieldname": "Week", "fieldtype": "Data", "width": 100},
        {"label": "Month", "fieldname": "Month", "fieldtype": "Data", "width": 100},
        {"label": "QTR", "fieldname": "QTR", "fieldtype": "Data", "width": 100},
        {"label": "Salesman", "fieldname": "Salesman", "fieldtype": "Data", "width": 120},
        {"label": "MRP", "fieldname": "MRP", "fieldtype": "Data", "width": 120},
        # {"label": "Discount", "fieldname": "Discount", "fieldtype": "Percent", "width": 80},
        # {"label": "Need Purchase Price", "fieldname": "Need Purchase Price", "fieldtype": "Currency", "width": 150},
        {"label": "Profession of a customer", "fieldname": "Profession of a customer", "fieldtype": "Data", "width": 100},
        {"label": "GST Number", "fieldname": "GST Number", "fieldtype": "Data", "width": 120},
        {"label": "GST Type", "fieldname": "GST Type", "fieldtype": "Data", "width": 100},
    ]
    # columns.append({
    # "label": "Advance",
    # "fieldname": "Advance",
    # "fieldtype": "Currency",
    # "width": 120
    # })
    # Add dynamic columns after GST Type
    # columns.extend(account_columns)
    columns.extend(customer_columns)

    return columns, data
# import frappe
# from frappe.utils import getdate, formatdate

# def execute(filters=None):
#     if not filters:
#         filters = {}

#     conditions = []
#     if filters.get("company"):
#         conditions.append(f"si.company = '{filters.get('company')}'")
#     if filters.get("from_date"):
#         conditions.append(f"si.posting_date >= '{filters.get('from_date')}'")
#     if filters.get("to_date"):
#         conditions.append(f"si.posting_date <= '{filters.get('to_date')}'")
#     if filters.get("customer_name"):
#         customers = "', '".join(filters.get("customer_name"))
#         conditions.append(f"si.customer IN ('{customers}')")    
#     if filters.get("customer_group"):
#         groups = "', '".join(filters.get("customer_group"))
#         conditions.append(f"c.customer_group IN ('{groups}')")
#     if filters.get("set_warehouse"):
#         warehouses = "', '".join(filters.get("set_warehouse"))
#         conditions.append(f"si.set_warehouse IN ('{warehouses}')")
#     if filters.get("item_group"):
#         item_groups = "', '".join(filters.get("item_group"))
#         conditions.append(f"it.item_group IN ('{item_groups}')")
#     if filters.get("sub_lob"):
#         sub_lobs = "', '".join(filters.get("sub_lob"))
#         conditions.append(f"it.custom_item_sub_lob IN ('{sub_lobs}')")
#     if filters.get("item_category"):
#         item_categories = "', '".join(filters.get("item_category"))
#         conditions.append(f"it.custom_item_category IN ('{item_categories}')")
#     # if filters.get("customer_name"):
#     #     conditions.append(f"c.customer_name = '{filters.get('customer_name')}'")
#     # if filters.get("customer_group"):
#     #     conditions.append(f"c.customer_group = '{filters.get('customer_group')}'")
#     # if filters.get("set_warehouse"):
#     #     conditions.append(f"si.set_warehouse = '{filters.get('set_warehouse')}'")

#     conditions_sql = " AND ".join(conditions)
#     if conditions_sql:
#         conditions_sql = " AND " + conditions_sql

#     query = f"""
#         SELECT
#             si.company AS "Company Name",
#             si.set_warehouse AS "Item Godown",
#             si.name AS "Voucher Number",
#             si.posting_date AS "Date",
#             c.customer_name AS "Party Name",
#             c.customer_group AS "Party Group",
#             si.custom_party_name AS "Mailing Name",
#             c.mobile_no AS "Contact No",
#             it.brand AS "Brand Name",
#             sii.item_name AS "Item Name",
#             sii.item_code AS "Item Part No",
#             it.item_group AS "Item Group",
#             it.custom_item_category AS "Item Category",
#             it.custom_item_sub_lob AS "Sub LOB",
#             sii.qty AS "Actual Quantity",
#             sii.net_rate AS "Basic Rate",
#                        (
#                 CASE
#                     WHEN IFNULL(sii.igst_amount, 0) > 0
#                         THEN sii.net_rate + IFNULL(sii.igst_amount, 0)
#                     ELSE
#                         sii.net_rate + IFNULL(sii.cgst_amount, 0) + IFNULL(sii.sgst_amount, 0)
#                 END
#             ) AS "Rate Inclusive",
#             sii.base_net_amount AS "Taxable Amount",
#                       (
#                 CASE
#                     WHEN IFNULL(sii.igst_amount, 0) > 0
#                         THEN ((sii.net_rate * sii.qty)+ IFNULL(sii.igst_amount, 0)) 
#                     ELSE
#                         ((sii.net_rate * sii.qty) + IFNULL(sii.cgst_amount, 0) + IFNULL(sii.sgst_amount, 0)) 
#                 END
#             ) AS "Amount Inclusive",
#             si.rounded_total AS "Rounded Total",
#             si.base_grand_total AS "Company Final",
#             si.custom_day AS "Day",
#             si.custom_month AS "Month",
#             si.custom_quarter AS "QTR",
#             si.billing_address_gstin AS "Bill Type",
#             si.customer AS "Cust Nature",
#             si.custom_internal_branch AS "Payment Mode",
#             si.custom_branch_warehouse AS "Trade In",
#             st.sales_person AS "Salesman",
#             st.sales_person AS "Combo LOB Discount",
#             sii.price_list_rate AS "MRP",
#             sii.discount_percentage AS "Discount",
#             sii.rate AS "SaleRate",
#             c.custom_profession AS "Profession of a customer",
#             c.gstin AS "GST Number",
#             c.gst_category AS "GST Type"
#         FROM
#             `tabSales Invoice` si
#         JOIN
#             `tabSales Invoice Item` sii ON si.name = sii.parent
#         JOIN
#             `tabCustomer` c ON si.customer = c.name
#         JOIN
# 			`tabItem` it ON sii.item_code = it.item_code
#         LEFT JOIN
# 			`tabSales Team` st ON si.name = st.parent
#         WHERE
#             si.docstatus = 1
#             {conditions_sql}
#         ORDER BY si.posting_date DESC
#     """

#     data = frappe.db.sql(query, as_dict=True)

#     columns = [
#         {"label": "Company Name", "fieldname": "Company Name", "fieldtype": "Link", "options": "Company", "width": 150},
#         {"label": "Item Godown", "fieldname": "Item Godown", "fieldtype": "Link", "options": "Warehouse", "width": 150},
#         {"label": "Voucher Number", "fieldname": "Voucher Number", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
#         {"label": "Date", "fieldname": "Date", "fieldtype": "Date", "width": 100},
#         {"label": "Party Name", "fieldname": "Party Name", "fieldtype": "Link", "options": "Customer", "width": 150},
#         {"label": "Party Group", "fieldname": "Party Group", "fieldtype": "Link", "options": "Customer Group", "width": 120},
#         {"label": "Mailing Name", "fieldname": "Mailing Name", "fieldtype": "Data", "width": 150},
#         {"label": "Contact No", "fieldname": "Contact No", "fieldtype": "Data", "width": 120},
#         {"label": "Brand Name", "fieldname": "Brand Name", "fieldtype": "Data", "width": 120},
#         {"label": "Item Name", "fieldname": "Item Name", "fieldtype": "Data", "width": 150},
#         {"label": "Item Part No", "fieldname": "Item Part No", "fieldtype": "Link", "options": "Item", "width": 120},
#         {"label": "Item Group", "fieldname": "Item Group", "fieldtype": "Link", "options": "Item Group", "width": 120},
#         {"label": "Item Category", "fieldname": "Item Category", "fieldtype": "Link", "options": "Item Category", "width": 120},
#         {"label": "Sub LOB", "fieldname": "Sub LOB", "fieldtype": "Link", "options": "Item Sub Lob", "width": 120},
#         {"label": "Actual Quantity", "fieldname": "Actual Quantity", "fieldtype": "Float", "width": 100},
#         {"label": "Basic Rate", "fieldname": "Basic Rate", "fieldtype": "Currency", "width": 100},
#         {"label": "Rate Inclusive", "fieldname": "Rate Inclusive", "fieldtype": "Currency", "width": 100},
#         {"label": "Taxable Amount", "fieldname": "Taxable Amount", "fieldtype": "Currency", "width": 100},
#         {"label": "Amount Inclusive", "fieldname": "Amount Inclusive", "fieldtype": "Currency", "width": 100},
#         {"label": "Company Final", "fieldname": "Company Final", "fieldtype": "Currency", "width": 120},
#         {"label": "Day", "fieldname": "Day", "fieldtype": "Int", "width": 100},
#         {"label": "Month", "fieldname": "Month", "fieldtype": "Int", "width": 100},
#         {"label": "QTR", "fieldname": "QTR", "fieldtype": "Int", "width": 100},
#         {"label": "Bill Type", "fieldname": "Bill Type", "fieldtype": "Data", "width": 100},
#         {"label": "Cust Nature", "fieldname": "Cust Nature", "fieldtype": "Data", "width": 100},
#         {"label": "Payment Mode", "fieldname": "Payment Mode", "fieldtype": "Data", "width": 100},
#         {"label": "Trade In", "fieldname": "Trade In", "fieldtype": "Data", "width": 100},
#         {"label": "Salesman", "fieldname": "Salesman", "fieldtype": "Data", "width": 120},
#         {"label": "Combo LOB Discount", "fieldname": "Combo LOB Discount", "fieldtype": "Data", "width": 120},
#         {"label": "MRP", "fieldname": "MRP", "fieldtype": "Data", "width": 120},
#         {"label": "Discount", "fieldname": "Discount", "fieldtype": "Percent", "width": 80},
#         {"label": "SaleRate", "fieldname": "SaleRate", "fieldtype": "Currency", "width": 100},
#         {"label": "Profession of a customer", "fieldname": "Profession of a customer", "fieldtype": "Data", "width": 100},
#         {"label": "GST Number", "fieldname": "GST Number", "fieldtype": "Data", "width": 120},
#         {"label": "GST Type", "fieldname": "GST Type", "fieldtype": "Data", "width": 100},
#     ]

#     return columns, data