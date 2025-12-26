import frappe
from frappe.utils import nowdate

def create_journal_entry_for_pos(doc, method):

    # Only for POS Sales Invoice
    if doc.doctype == "Sales Invoice" and not doc.is_pos:
        return

    company_abbr = frappe.db.get_value("Company", doc.company, "abbr")

    branch_ = frappe.db.get_value("POS Profile", doc.pos_profile, "branch") if doc.pos_profile else None

    doc.branch = branch_ if branch_ else doc.branch

    accounts = []
    total_base_amount = 0
    forward_process = False
    # Loop through each POS payment row
    for pay in doc.payments:
        mop = frappe.get_doc("Mode of Payment", pay.mode_of_payment)

        # Case 1: Custom customer exists on Mode of Payment
        if mop.custom_customer_name:
            if pay.base_amount > 0:
                forward_process = True
                accounts.append({
                    "account": f"Debtors - {company_abbr}",
                    "party_type": "Customer",
                    "party": mop.custom_customer_name,
                    "debit_in_account_currency": pay.base_amount,
                    "credit_in_account_currency": 0,
                    "reference_detail_no": pay.reference_no,
                    "branch": branch_ or doc.branch
                })
            total_base_amount += pay.base_amount
        # Case 2: Normal Mode of Payment account
        # else:
        #     if pay.base_amount > 0:
        #         accounts.append({
        #             "account": f"{pay.mode_of_payment} - {company_abbr}",
        #             "debit_in_account_currency": pay.base_amount,
        #             "credit_in_account_currency": 0  ,
        #             "branch": doc.branch                 
        #         })

    # Credit the invoice customer for total amount
    accounts.append({
        "account": f"Debtors - {company_abbr}",
        "party_type": "Customer",
        "party": doc.customer,
        "credit_in_account_currency": total_base_amount,
        "debit_in_account_currency": 0,
        "branch": branch_ or doc.branch
    })

    if not forward_process:
        return
    # Create Journal Entry
    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "posting_date": nowdate(),
        "voucher_type": "Journal Entry",
        "title": f"POS Entry - {doc.name}",
        "accounts": accounts,
        "reference_name": doc.name
    })

    je.insert(ignore_permissions=True)
    je.submit()

