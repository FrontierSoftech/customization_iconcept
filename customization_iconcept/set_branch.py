import frappe

def before_save(doc, method):
    
    if doc.pos_profile:
        branch_ = frappe.db.get_value("POS Profile", doc.pos_profile, "branch")
        if branch_:
            doc.branch = branch_