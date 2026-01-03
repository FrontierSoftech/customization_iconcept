import frappe
from frappe.model.naming import make_autoname

def before_insert(doc, method):
    if doc.is_pos:
        for item in doc.items:
            if item.pos_invoice:
                doc.name = item.pos_invoice
                doc.naming_series = item.pos_invoice
                break
    else:
        if doc.is_return:
            # doc.custom_vch_abbr = "SR"
            doc.naming_series = f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./SR-.YY./.#"
            doc.name = f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./SR-.YY./.#"
            # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./SR-.YY./.#")
        else:
            # doc.custom_vch_abbr = "S"
            doc.naming_series = f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./S-.YY./.#"
            doc.name = f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./S-.YY./.#"
            # doc.name = make_autoname(f".{doc.custom_company_abbr}.-.{doc.custom_branch_code}./S-.YY./.#")
