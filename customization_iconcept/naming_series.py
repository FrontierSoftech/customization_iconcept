import frappe
from frappe.model.naming import make_autoname
from frappe.utils import getdate

fy = frappe.db.get_value("Fiscal Year",{"year_start_date": ["<=", getdate()], "year_end_date": [">=", getdate()]}, "name")
if "-" in fy:
    start_year = fy.split("-")[0]
else:
    start_year = fy
def before_insert(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    internal_customer = frappe.db.get_value("Customer",doc.customer,"is_internal_customer")

    if doc.is_return:
        # doc.custom_vch_abbr = "SR"
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./SR-{start_year}/.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./SR-{start_year}/.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./SR-{start_year}/.#")
    elif internal_customer:
        # doc.custom_vch_abbr = "IC"
        doc.naming_series = f".{company_abbr}{doc.custom_branch_code}.-SO-{start_year}/.#"
        doc.name = f".{company_abbr}{doc.custom_branch_code}.-SO-{start_year}/.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./IC-{start_year}/.#")    
    else:
        # doc.custom_vch_abbr = "S"
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./S-{start_year}/.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./S-{start_year}/.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./S-{start_year}/.#")

def naming_series_sales_order(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./SO-{start_year}/.#"
    doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./SO-{start_year}/.#"
    # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./SO-{start_year}/.#")

def naming_series_delivery_note(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./DN-{start_year}/.#"
    doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./DN-{start_year}/.#"
    # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./DN-{start_year}/.#")

def naming_series_purchase_invoice(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    internal_customer = frappe.db.get_value("Supplier",doc.supplier,"is_internal_supplier")
    if doc.is_return:
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./PR-{start_year}/.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./PR-{start_year}/.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./PR-{start_year}/.#")
    elif internal_customer:
        # doc.custom_vch_abbr = "IC"
        doc.naming_series = f".{company_abbr}{doc.custom_branch_code}.-SI-{start_year}/.#"
        doc.name = f".{company_abbr}{doc.custom_branch_code}.-SI-{start_year}/.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./IC-{start_year}/.#")        
    else:
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./PI-{start_year}/.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./PI-{start_year}/.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./PI-{start_year}/.#")

def naming_series_purchase_order(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./PO-{start_year}/.#"
    doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./PO-{start_year}/.#"
    # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./PO-{start_year}/.#")

def naming_series_purchase_receipt(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./PR-{start_year}/.#"
    doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./PR-{start_year}/.#"
    # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./PR-{start_year}/.#")

def naming_series_payment_entry(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    if doc.payment_type == "Receive":
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./RC-{start_year}/.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./RC-{start_year}/.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./RC-{start_year}/.#")
    else:
        doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./PY-{start_year}/.#"
        doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./PY-{start_year}/.#"
        # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./PY-{start_year}/.#")

def naming_series_journal_entry(doc, method):
    company_abbr = doc.get("custom_company_abbr")[:2]
    doc.naming_series = f".{company_abbr}.-.{doc.custom_branch_code}./JE-{start_year}/.#"
    doc.name = f".{company_abbr}.-.{doc.custom_branch_code}./JE-{start_year}/.#"
    # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./JE-{start_year}/.#")


