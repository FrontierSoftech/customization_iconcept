import frappe

def cancel_linked_journal_entry(doc, method):
    linked_journal_entries = frappe.get_all("Journal Entry", filters={
        "custom_reference_doctype": "Sales Invoice",
        "custom_reference_name": doc.name
    })

    for link in linked_journal_entries:
        journal_entry = frappe.get_doc("Journal Entry", link.name)
        if journal_entry.docstatus != 2:  # Check if not already canceled
            journal_entry.cancel()  # Cancel the journal entry
            frappe.msgprint(f"✅ Journal Entry {journal_entry.name} canceled for Sales Invoice {doc}.")
  
