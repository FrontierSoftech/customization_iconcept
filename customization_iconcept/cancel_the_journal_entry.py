import frappe

def cancel_linked_journal_entery(doc, method):
    for row in doc.accounts:
        if row.reference_name:
            # Check if the reference is a Sales Invoice
            if frappe.db.exists("Sales Invoice", row.reference_name):
                si_status = frappe.db.get_value(
                    "Sales Invoice",
                    row.reference_name,
                    "docstatus"
                )
    
                # docstatus: 0 = Draft, 1 = Submitted, 2 = Cancelled
                if si_status != 2:
                    frappe.throw(
                        f"Sales Invoice <b>{row.reference_name}</b> is not cancelled. "
                        f"Please cancel this Sales Invoice first before cancelling the Journal Entry."
                    )
