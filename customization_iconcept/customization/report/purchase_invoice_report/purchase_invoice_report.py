# Copyright (c) 2026, Frontier Softech and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

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
        conditions.append(f"pi.company = '{filters.get('company')}'")
    if filters.get("from_date"):
        conditions.append(f"pi.posting_date >= '{filters.get('from_date')}'")
    if filters.get("to_date"):
        conditions.append(f"pi.posting_date <= '{filters.get('to_date')}'")
    if filters.get("supplier"):
        suppliers = "', '".join(filters.get("supplier"))
        conditions.append(f"pi.supplier IN ('{suppliers}')")    
    # MULTI PARTY GROUP
    if filters.get("supplier_group"):
        groups = "', '".join(filters.get("supplier_group"))
        conditions.append(f"sup.supplier_group IN ('{groups}')")
    # MULTI WAREHOUSE
    if filters.get("set_warehouse"):
        warehouses = "', '".join(filters.get("set_warehouse"))
        conditions.append(f"pii.warehouse IN ('{warehouses}')")
    if filters.get("item_group"):
        item_groups = "', '".join(filters.get("item_group"))
        conditions.append(f"item.item_group IN ('{item_groups}')")
    if filters.get("item_category"):
        categories = "', '".join(filters.get("item_category"))
        conditions.append(f"item.custom_item_category IN ('{categories}')")
    if filters.get("sub_lob"):
        sub_lobs = "', '".join(filters.get("sub_lob"))
        conditions.append(f"item.custom_item_sub_lob IN ('{sub_lobs}')")
    # if filters.get("supplier"):
    #     conditions.append(f"pi.supplier = '{filters.get('supplier')}'")
    # if filters.get("supplier_group"):
    #     conditions.append(f"sup.supplier_group = '{filters.get('supplier_group')}'")
    # if filters.get("set_warehouse"):
    #     conditions.append(f"pi.set_warehouse = '{filters.get('set_warehouse')}'")

    conditions_sql = " AND ".join(conditions)
    if conditions_sql:
        conditions_sql = " AND " + conditions_sql

    query = f"""
        SELECT
            pi.company AS "Company Name",
            pi.name AS "Voucher Number",
            pi.bill_no AS "Supplier Invoice No",
            pi.bill_date AS "Supplier Invoice Date",
            pi.posting_date AS "Date",
            pi.branch AS "Voucher Type",
            pi.supplier AS "Party Name",
            addr.city AS "City",
            sup.supplier_name AS "Is Export",
            sup.supplier_name AS "Export Date & Time",
            sup.supplier_name AS "Party Alias",
            addr.address_line1 AS "Party Address",
            addr.pincode AS "Party Pincode",
            pi.contact_person AS "Party Contact Person",
            con.phone AS "Party Telephone No",
            sup.mobile_no AS "Party Mobile No",
            addr.fax AS "Party Fax No",
            con.email_id AS "Party Email",
            sup.supplier_group AS "Party Group",
            addr.state AS "Party State",
            addr.gstin AS "CST Number",
            pii.item_name AS "Item Name",
            item.item_name AS "Item Alias",
            item.item_code AS "Item Part No",
            item.item_group AS "Item Group",
            item.custom_item_category AS "Item Category",
            pii.description AS "Item Description ",
            pii.description AS "Item Notes",
            pii.description AS "Item Tariff Class",
            pii.warehouse AS "Godown",
            item.brand AS "Brand Name",
            item.custom_item_sub_lob AS "Sub Lob",
            pii.brand AS "NPI",
            pii.brand AS "Applicable From",
            pii.brand AS "Non-NPI",
            pii.brand AS "Applicable From",
            pii.brand AS "Extra 1",
            pii.brand AS "Extra 2",
            pii.brand AS "IMEI One",
            pii.brand AS "IMEI Two",
            sbe.serial_no AS "Serial No",
            sbe.batch_no AS "Item Batch",
            pii.serial_no AS "Apple HQ ID",
            pii.rate AS "Batch Rate",
            pii.qty AS "Actual Quantity",
            pii.qty AS "Billed Quantity",
            pii.qty AS "Alternate Actual Quantity",
            pii.qty AS "Alternate Billed Quantity",
            pii.rate AS "Purchase Price",
            pii.rate AS "Rate",
            pii.uom AS "Unit",
            pii.discount_percentage AS "Discount",
            pii.discount_amount AS "Discount Amount",
            pii.amount AS "Amount",
            pii.amount AS "Standard Cost",
            pii.amount AS "Standard Price",
            pii.expense_account AS "Purchase/Sales Ledger",
            pi.remarks AS "Narration"

        FROM
            `tabPurchase Invoice` pi

        LEFT JOIN
            `tabPurchase Invoice Item` pii
            ON pii.parent = pi.name

        LEFT JOIN `tabSerial and Batch Bundle` sbb
            ON sbb.name = pii.serial_and_batch_bundle

        LEFT JOIN `tabSerial and Batch Entry` sbe
            ON sbe.parent = sbb.name

        LEFT JOIN
            `tabSupplier` sup
            ON sup.name = pi.supplier

        LEFT JOIN
            `tabAddress` addr
            ON addr.name = pi.supplier_address

        LEFT JOIN
            `tabContact` con
            ON con.name = pi.contact_person

        LEFT JOIN
            `tabItem` item
            ON item.name = pii.item_code

        WHERE
            pi.docstatus = 1
            {conditions_sql}
        ORDER BY pi.posting_date DESC
    """

    data = frappe.db.sql(query, as_dict=True)

    columns = [
        {"label": "Company Name", "fieldname": "Company Name", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Voucher Number", "fieldname": "Voucher Number", "fieldtype": "Link", "options": "Purchase Invoice", "width": 150},
        {"label": "Supplier Invoice No", "fieldname": "Supplier Invoice No", "fieldtype": "Data", "width": 120},
        {"label": "Supplier Invoice Date", "fieldname": "Supplier Invoice Date", "fieldtype": "Date", "width": 100},
        {"label": "Date", "fieldname": "Date", "fieldtype": "Date", "width": 100},
        {"label": "Voucher Type", "fieldname": "Voucher Type", "fieldtype": "Data", "width": 150},
        {"label": "Party Name", "fieldname": "Party Name", "fieldtype": "Link", "options": "Supplier", "width": 120},
        {"label": "City", "fieldname": "City", "fieldtype": "Data", "width": 150},
        {"label": "Is Export", "fieldname": "Is Export", "fieldtype": "Data", "width": 120},
        {"label": "Export Date & Time", "fieldname": "Export Date & Time", "fieldtype": "Data", "width": 120},
        {"label": "Party Alias", "fieldname": "Party Alias", "fieldtype": "Data", "width": 150},
        {"label": "Party Address", "fieldname": "Party Address", "fieldtype": "Data", "width": 120},
        {"label": "Party Pincode", "fieldname": "Party Pincode", "fieldtype": "Data", "width": 120},
        {"label": "Party Contact Person", "fieldname": "Party Contact Person", "fieldtype": "Data", "width": 120},
        {"label": "Party Telephone No", "fieldname": "Party Telephone No.", "fieldtype": "Data", "width": 120},
        {"label": "Party Mobile No", "fieldname": "Party Mobile No.", "fieldtype": "Data", "width": 120},
        {"label": "Party Fax No", "fieldname": "Party Fax No.", "fieldtype": "Data", "width": 120},
        {"label": "Party E-Mail", "fieldname": "Party E-Mail", "fieldtype": "Data", "width": 120},
        {"label": "Party Group", "fieldname": "Party Group", "fieldtype": "Data", "width": 120},
        {"label": "Party State", "fieldname": "Party State", "fieldtype": "Data", "width": 120},
        {"label": "CST Number", "fieldname": "CST Number", "fieldtype": "Int", "width": 100},
        {"label": "Item Name", "fieldname": "Item Name", "fieldtype": "Data", "width": 150},
        {"label": "Item Alias", "fieldname": "Item Alias", "fieldtype": "Data", "width": 150},
        {"label": "Item Part No", "fieldname": "Item Part No", "fieldtype": "Data", "width": 100},
        {"label": "Item Group", "fieldname": "Item Group", "fieldtype": "Data", "width": 100},
        {"label": "Item Category", "fieldname": "Item Category", "fieldtype": "Data", "width": 100},
        {"label": "Item Description", "fieldname": "Item Description", "fieldtype": "Data", "width": 100},
        {"label": "Item Notes", "fieldname": "Item Notes", "fieldtype": "Data", "width": 120},
        {"label": "Item Tariff Class", "fieldname": "Item Tariff Class", "fieldtype": "Data", "width": 120},
        {"label": "Godown", "fieldname": "Godown", "fieldtype": "Data", "width": 120},
        {"label": "Brand Name", "fieldname": "Brand Name", "fieldtype": "Data", "width": 120},
        {"label": "Sub Lob", "fieldname": "Sub Lob", "fieldtype": "Data", "width": 100},
        {"label": "NPI", "fieldname": "NPI", "fieldtype": "Data", "width": 100},
        {"label": "Applicable From", "fieldname": "Applicable From", "fieldtype": "Data", "width": 120},
        {"label": "Non-NPI", "fieldname": "Non-NPI", "fieldtype": "Data", "width": 100},
        {"label": "Applicable From", "fieldname": "Applicable From", "fieldtype": "Data", "width": 120},
        {"label": "Extra 1", "fieldname": "Extra 1", "fieldtype": "Data", "width": 120},
        {"label": "Extra 2", "fieldname": "Extra 2", "fieldtype": "Data", "width": 120},
        {"label": "IMEI One", "fieldname": "IMEI One", "fieldtype": "Data", "width": 120},
        {"label": "IMEI Two", "fieldname": "IMEI Two", "fieldtype": "Data", "width": 120},
        {"label": "Serial No", "fieldname": "Serial No", "fieldtype": "Data", "width": 120},
        {"label": "Item Batch", "fieldname": "Item Batch", "fieldtype": "Data", "width": 120},
        {"label": "Apple HQ ID", "fieldname": "Apple HQ ID", "fieldtype": "Data", "width": 120},
        {"label": "Batch Rate", "fieldname": "Batch Rate", "fieldtype": "Data", "width": 120},
        {"label": "Actual Quantity", "fieldname": "Actual Quantity", "fieldtype": "Data", "width": 120},
        {"label": "Billed Quantity", "fieldname": "Billed Quantity", "fieldtype": "Data", "width": 120},
        {"label": "Alternate Actual Quantity", "fieldname": "Alternate Actual Quantity", "fieldtype": "Data", "width": 120},
        {"label": "Alternate Billed Quantity", "fieldname": "Alternate Billed Quantity", "fieldtype": "Data", "width": 120},
        {"label": "Purchase Price", "fieldname": "Purchase Price", "fieldtype": "Data", "width": 120},
        {"label": "Rate", "fieldname": "Rate", "fieldtype": "Data", "width": 120},
        {"label": "Unit", "fieldname": "Unit", "fieldtype": "Data", "width": 120},
        {"label": "Discount", "fieldname": "Discount", "fieldtype": "Data", "width": 120},
        {"label": "Discount Amount", "fieldname": "Discount Amount", "fieldtype": "Data", "width": 120},
        {"label": "Amount", "fieldname": "Amount", "fieldtype": "Data", "width": 120},
        {"label": "Standard Cost", "fieldname": "Standard Cost", "fieldtype": "Data", "width": 120},
        {"label": "Purchase/Sales Ledger", "fieldname": "Purchase/Sales Ledger", "fieldtype": "Data", "width": 120},
        {"label": "Narration", "fieldname": "Narration", "fieldtype": "Data", "width": 120},
    ]

    return columns, data