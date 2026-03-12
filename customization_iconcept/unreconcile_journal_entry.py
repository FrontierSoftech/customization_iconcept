import frappe

def unreconcile_payments_for_credit_note(doc, method):
    """
    Automatically create Unreconcile Payment entries for Credit Note
    """
    if not doc.is_return or not doc.return_against:
        return

    # Get all submitted Journal Entries linked to the original Sales Invoice
    linked_journal_entries = frappe.get_all(
        "Journal Entry",
        filters={
            "custom_reference_name": doc.return_against,
            "docstatus": 1
        },
        fields=["name"]
    )

    for je in linked_journal_entries:
        je_doc = frappe.get_doc("Journal Entry", je.name)

        # For each account in the JE, create an Unreconcile Payment if amount exists
        unreconcile = frappe.new_doc("Unreconcile Payment")
        unreconcile.company = je_doc.company
        unreconcile.voucher_type = "Journal Entry"
        unreconcile.voucher_no = je_doc.name
        unreconcile.append("allocations", {
                "reference_doctype": "Sales Invoice",
                "reference_name": doc.return_against,
                "allocated_amount": je_doc.total_debit,
                "unlinked": 0
        })
        
        unreconcile.insert()
        unreconcile.submit()

        frappe.db.set_value(
            "Sales Invoice",
            doc.return_against,
            "status",
            "Credit Note Issued"
        )
