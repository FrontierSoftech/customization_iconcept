import frappe

def supplier_name(doc, method=None):
    if doc.supplier:
        doc.title = frappe.db.set_value("Supplier",doc.supplier,"supplier_name")