import frappe

def set_supplier_title(doc, method):
    if doc.supplier:
        doc.title = frappe.db.get_value(
            "Supplier",
            doc.supplier,
            "supplier_name"
        )