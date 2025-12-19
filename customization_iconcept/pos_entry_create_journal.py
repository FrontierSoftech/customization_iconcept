import frappe
from frappe.utils import nowdate

def create_journal_entry_for_pos(doc, method):
    # Check if a journal entry already exists for this POS
    if not frappe.db.exists("Mode of Payment", {"custom_customer_name": doc.customer}):
        return
    
    mode_of_payment_doc = frappe.get_doc("Mode of Payment", {"custom_customer_name": doc.customer})
    
    if mode_of_payment_doc.accounts:
        default_account = mode_of_payment_doc.accounts[0].default_account
    else:
        default_account = None
    
    company_abbr = frappe.db.get_value("Company", doc.company, "abbr")
    # Create Journal Entry
    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "posting_date": nowdate(),
        "voucher_type": "Journal Entry",
        "title": f"POS Entry - {doc.name}",
        "accounts": [
            {
                "account": default_account,
                "debit_in_account_currency": doc.grand_total,
                "credit_in_account_currency": 0,
                "party_type": None,
                "party": None
            },
            {
                "account": f"Debtors - {company_abbr}",
                "party_type": "Customer",
                "party": doc.customer,
                "credit_in_account_currency": doc.grand_total,
                "debit_in_account_currency": 0,  
            }
        ],
        "reference_name": doc.name
    })
    je.insert()
    je.submit()
