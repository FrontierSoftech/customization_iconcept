import frappe
from frappe.utils import nowdate

def create_journal_entry_for_pos(doc, method):

    # Only for POS Sales Invoice
    if doc.doctype != "Sales Invoice" and not doc.is_pos:
        return

    company_abbr = frappe.db.get_value("Company", doc.company, "abbr")

    accounts = []

    # Loop through each POS payment row
    for pay in doc.payments:
        mop = frappe.get_doc("Mode of Payment", pay.mode_of_payment)

        # Case 1: Custom customer exists on Mode of Payment
        if mop.custom_customer_name:
            if pay.base_amount > 0:
                accounts.append({
                    "account": f"Debtors - {company_abbr}",
                    "party_type": "Customer",
                    "party": mop.custom_customer_name,
                    "debit_in_account_currency": pay.base_amount,
                    "credit_in_account_currency": 0
                })

        # Case 2: Normal Mode of Payment account
        else:
            if pay.base_amount > 0:
                accounts.append({
                    "account": f"{pay.mode_of_payment} - {company_abbr}",
                    "debit_in_account_currency": pay.base_amount,
                    "credit_in_account_currency": 0
                })

    # Credit the invoice customer for total amount
    accounts.append({
        "account": f"Debtors - {company_abbr}",
        "party_type": "Customer",
        "party": doc.customer,
        "credit_in_account_currency": doc.grand_total,
        "debit_in_account_currency": 0
    })

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

# import frappe
# from frappe.utils import nowdate

# def create_journal_entry_for_pos(doc, method):

#     if doc.doctype == "Sales Invoice" and not doc.is_pos:
#         return
#     # Check if a journal entry already exists for this POS
#     if not frappe.db.exists("Mode of Payment", {"custom_customer_name": doc.customer}):
#         return
    
#     mode_of_payment_doc = frappe.get_doc("Mode of Payment", {"custom_customer_name": doc.customer})
    
#     if mode_of_payment_doc.accounts:
#         default_account = mode_of_payment_doc.accounts[0].default_account
#     else:
#         default_account = None
    
#     company_abbr = frappe.db.get_value("Company", doc.company, "abbr")
#     # Create Journal Entry
#     je = frappe.get_doc({
#         "doctype": "Journal Entry",
#         "posting_date": nowdate(),
#         "voucher_type": "Journal Entry",
#         "title": f"POS Entry - {doc.name}",
#         "accounts": [
#             {
#                 "account": default_account,
#                 "debit_in_account_currency": doc.grand_total,
#                 "credit_in_account_currency": 0,
#                 "party_type": None,
#                 "party": None
#             },
#             {
#                 "account": f"Debtors - {company_abbr}",
#                 "party_type": "Customer",
#                 "party": doc.customer,
#                 "credit_in_account_currency": doc.grand_total,
#                 "debit_in_account_currency": 0,  
#             }
#         ],
#         "reference_name": doc.name
#     })
#     je.insert()
#     je.submit()
