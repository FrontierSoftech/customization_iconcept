import frappe
from frappe.utils import comma_and, cstr, flt, fmt_money, formatdate, get_link_to_form, nowdate

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
# def journal_entry_with_outstanding(doctype, txt, searchfield, start, page_len, filters):
#     account = filters.get("account")
#     party = filters.get("party")

#     if not account or not party:
#         return []

#     data = frappe.db.sql("""
#         SELECT
#             gle.voucher_no AS name,
#             je.posting_date,
#             SUM(gle.debit - gle.credit) AS balance
#         FROM `tabGL Entry` gle
#         INNER JOIN `tabJournal Entry` je ON je.name = gle.voucher_no
#         WHERE
#             gle.voucher_type = 'Journal Entry'
#             AND gle.party_type = 'Customer'
#             AND gle.party = %(party)s
#             AND gle.account = %(account)s
#             AND gle.is_cancelled = 0
#             AND je.docstatus = 1
#             AND gle.voucher_no LIKE %(txt)s
#         GROUP BY gle.voucher_no, je.posting_date
#         HAVING balance > 0
#         ORDER BY je.posting_date DESC
#         LIMIT %(page_len)s OFFSET %(start)s
#     """, {
#         "party": party,
#         "account": account,
#         "txt": f"%{txt}%",
#         "page_len": page_len,
#         "start": start
#     }, as_dict=True)

#     result = []
#     for row in data:
#         result.append([
#             row.name,
#             row.posting_date,
#             f"Outstanding: {flt(row.balance):,.2f}"
#         ])

#     return result
def journal_entry_with_outstanding(doctype, txt, searchfield, start, page_len, filters):
    """
    Returns Journal Entries for a customer with Total Amount and Outstanding Amount,
    exactly like Accounts Receivable report.
    """

    account = filters.get("account")
    party = filters.get("party")

    if not account or not party:
        return []

    # Get all Journal Entry GL Entries for this customer + account
    gl_entries = frappe.db.sql("""
        SELECT
            gle.voucher_no,
            je.posting_date,
            SUM(gle.debit) AS total_debit,
            SUM(gle.credit) AS total_credit
        FROM `tabGL Entry` gle
        INNER JOIN `tabJournal Entry` je ON je.name = gle.voucher_no
        WHERE
            gle.voucher_type = 'Journal Entry'
            AND gle.party_type = 'Customer'
            AND gle.party = %s
            AND gle.account = %s
            AND gle.is_cancelled = 0
            AND je.docstatus = 1
            AND gle.voucher_no LIKE %s
        GROUP BY gle.voucher_no, je.posting_date
        ORDER BY je.posting_date DESC
        LIMIT %s OFFSET %s
    """, (party, account, f"%{txt}%", page_len, start), as_dict=True)

    result = []

    for gle in gl_entries:
        # Calculate real Outstanding Amount considering reconciliations
        # sum of GL entries against this voucher (like AR report)
        # Total = total_debit
        total_amount = gle.total_debit

        # Calculate payments/reconciled amounts applied to this voucher
        paid_amount = frappe.db.sql("""
            SELECT SUM(credit - debit) 
            FROM `tabGL Entry`
            WHERE
                against_voucher = %s
                AND party_type = 'Customer'
                AND party = %s
                AND is_cancelled = 0
        """, (gle.voucher_no, party))[0][0] or 0.0

        # Outstanding = Total - Paid
        outstanding_amount = total_amount - paid_amount

        # Only show if outstanding > 0
        if outstanding_amount > 0:
            # Combine into one column for Link field display
            display_amount = f"Total: {total_amount:,.2f} | Outstanding: {outstanding_amount:,.2f}"
            result.append([gle.voucher_no, str(gle.posting_date), display_amount])

    return result

@frappe.whitelist()
def get_journal_entry_outstanding(journal_entry, account, party):
    """
    Returns the outstanding amount for a selected Journal Entry
    """
    total_debit = frappe.db.sql("""
        SELECT SUM(debit) 
        FROM `tabGL Entry`
        WHERE voucher_no=%s AND account=%s AND party=%s AND is_cancelled=0
    """, (journal_entry, account, party))[0][0] or 0.0

    paid_amount = frappe.db.sql("""
        SELECT SUM(credit - debit)
        FROM `tabGL Entry`
        WHERE against_voucher=%s AND party_type='Customer' AND party=%s AND is_cancelled=0
    """, (journal_entry, party))[0][0] or 0.0

    outstanding = total_debit - paid_amount
    return {"outstanding": outstanding if outstanding > 0 else 0.0}
