import frappe
from frappe.model.naming import make_autoname

def before_insert(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]

    if doc.is_return:
        # doc.custom_vch_abbr = "SR"
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./SR-.YY./.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./SR-.YY./.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./SR-.YY./.#")
    else:
        # doc.custom_vch_abbr = "S"
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./S-.YY./.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./S-.YY./.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./S-.YY./.#")

def naming_series_sales_order(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./SO-.YY./.#"
    doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./SO-.YY./.#"
    # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./SO-.YY./.#")

def naming_series_delivery_note(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./DN-.YY./.#"
    doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./DN-.YY./.#"
    # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./DN-.YY./.#")

def naming_series_purchase_invoice(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    if doc.is_return:
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./PR-.YY./.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./PR-.YY./.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./PR-.YY./.#")
    else:
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./PI-.YY./.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./PI-.YY./.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./PI-.YY./.#")

def naming_series_purchase_order(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./PO-.YY./.#"
    doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./PO-.YY./.#"
    # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./PO-.YY./.#")

def naming_series_purchase_receipt(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./PR-.YY./.#"
    doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./PR-.YY./.#"
    # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./PR-.YY./.#")

def naming_series_payment_entry(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    if doc.payment_type == "Receive":
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./RC-.YY./.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./RC-.YY./.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./RC-.YY./.#")
    else:
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./PY-.YY./.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./PY-.YY./.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./PY-.YY./.#")

def naming_series_journal_entry(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./JE-.YY./.#"
    doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./JE-.YY./.#"
    # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./JE-.YY./.#")