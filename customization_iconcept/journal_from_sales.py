import frappe
from frappe.utils import nowdate

def create_finance_lender_jv(doc, method):
    """
    Create Journal Entry for each row in custom_finance_lender_payments
    """
    if doc.is_return:
        return
    
    # customer_group = frappe.db.get_value(
    #     "Customer",
    #     doc.customer,
    #     "customer_group"
    # )

    # stop_auto_creation = frappe.db.get_value(
    #     "Customer Group",
    #     customer_group,
    #     "custom_stop_auto_creation"
    # )

    # if stop_auto_creation:
    #     return
    
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
            je1.posting_date = doc.posting_date
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
            je1.posting_date = doc.posting_date
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
            
    if doc.custom_discount_ledger and doc.additional_discount_account:
        je2 = frappe.new_doc("Journal Entry")
        je2.voucher_type = "Journal Entry"
        je2.posting_date = doc.posting_date
        je2.company = doc.company
        je2.custom_reference_doctype = doc.doctype
        je2.custom_reference_name = doc.name
        je2.custom_branch = doc.branch
        je2.custom_cost_center = doc.cost_center

        total_discount = 0

        # Debit entries
        for row in doc.custom_discount_ledger:
            if not row.discount_ledger or not row.discount:
                continue

            total_discount += row.discount

            je2.append("accounts", {
                "account": row.discount_ledger,
                "debit_in_account_currency": row.discount,
                "credit_in_account_currency": 0,
                "branch": doc.branch,
                "cost_center": doc.cost_center
            })

        # Credit entry (Receivable / Discount account)
        je2.append("accounts", {
            "account": doc.additional_discount_account,
            "debit_in_account_currency": 0,
            "credit_in_account_currency": total_discount,
            "branch": doc.branch,
            "cost_center": doc.cost_center,            # ⭐ MUST match invoice customer
            # "reference_type": doc.doctype,
            # "reference_name": doc.name,
            # "reference_due_date": doc.posting_date
        })

        je2.insert()
        je2.submit()