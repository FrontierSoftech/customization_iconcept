import frappe
from frappe.utils import nowdate

def create_finance_lender_jv(doc, method):
    """
    Create Journal Entry for each row in custom_finance_lender_payments
    """
    if doc.is_return:
        return
    
    customer_group = frappe.db.get_value(
        "Customer",
        doc.customer,
        "customer_group"
    )

    stop_auto_creation = frappe.db.get_value(
        "Customer Group",
        customer_group,
        "custom_stop_auto_creation"
    )

    if stop_auto_creation:
        return
    
    for row in doc.custom_finance_lender_payments:
        if not row.finance_lender or not row.amount:
            continue  # skip empty rows
        company_abbr = frappe.db.get_value("Company", doc.company, "abbr")
        if row.mode == "Customer":
            # Get finance lender account from Customer
            finance_lender_account = frappe.get_doc("Customer", {"name": row.finance_lender})


            if finance_lender_account.accounts:
                default_account = finance_lender_account.accounts[0].account
            else:
                default_account = None

            # Create first Journal Entry
            je1 = frappe.new_doc("Journal Entry")
            je1.voucher_type = "Journal Entry"
            je1.posting_date = nowdate()
            je1.company = doc.company
            je1.remark = f"Finance Lender Payment - {row.reference_no}"
            je1.cheque_no = row.reference_no
            je1.cheque_date = doc.posting_date
            je1.custom_reference_doctype = doc.doctype
            je1.custom_reference_name = doc.name
            je1.custom_branch = doc.branch
            je1.custom_cost_center = doc.cost_center

            # Debit / Credit entries
            je1.append("accounts", {
                "account": default_account,
                "party_type": "Customer",
                "party": row.finance_lender,
                "debit_in_account_currency": row.amount,
                "credit_in_account_currency": 0,
                "user_remark":row.reference_no,
                "branch":doc.branch,
                "cost_center": doc.cost_center
            })
            je1.append("accounts", {
                "account": f"Debtors - {company_abbr}",  # or another relevant account
                "party_type": "Customer",
                "party": doc.customer,
                "debit_in_account_currency": 0,
                "credit_in_account_currency": row.amount,
                "branch":doc.branch,
                "cost_center": doc.cost_center,
                "reference_type": doc.doctype,
                "reference_name": doc.name,
                "reference_due_date": doc.posting_date
            })

            je1.insert()
            je1.submit()
        else:

            je1 = frappe.new_doc("Journal Entry")
            je1.voucher_type = "Journal Entry"
            je1.posting_date = nowdate()
            je1.company = doc.company
            je1.remark = f"Finance Lender Payment - {row.reference_no}"
            je1.custom_reference_doctype = doc.doctype
            je1.custom_reference_name = doc.name
            je1.custom_branch = doc.branch
            je1.custom_cost_center = doc.cost_center

            # Debit / Credit entries
            je1.append("accounts", {
                "account": row.finance_lender,
                "debit_in_account_currency": row.amount,
                "credit_in_account_currency": 0,
                "user_remark":row.reference_no,
                "branch":doc.branch,
                "cost_center": doc.cost_center
            })
            je1.append("accounts", {
                "account": f"Debtors - {company_abbr}",  # or another relevant account
                "party_type": "Customer",
                "party": doc.customer,
                "debit_in_account_currency": 0,
                "credit_in_account_currency": row.amount,
                "branch":doc.branch,
                "cost_center": doc.cost_center,
                "reference_type": doc.doctype,
                "reference_name": doc.name,
                "reference_due_date": doc.posting_date
            })

            je1.insert()
            je1.submit()