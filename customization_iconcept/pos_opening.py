import frappe

def notify_store_managers(doc, method=None):
    if not doc.pos_profile:
        return

    # Get POS Profile
    pos_profile = frappe.get_doc("POS Profile", doc.pos_profile)

    if not pos_profile.branch:
        return

    branch_name = pos_profile.branch

    # Get Branch
    branch_doc = frappe.get_doc("Branch", branch_name)

    emails = []

    # 🔁 IMPORTANT: replace 'store_managers' with your actual child table fieldname
    for row in branch_doc.custom_store_manager_user:
        if row.user:
            email = frappe.db.get_value("User", row.user, "email")
            if email:
                emails.append(email)

    if not emails:
        return

    # 📧 Email content
    subject = f"POS Opened - {doc.name}"

    message = f"""
    <h3>POS Opening Notification</h3>
    <p><b>POS Opening:</b> {doc.name}</p>
    <p><b>Branch:</b> {branch_name}</p>
    <p>The POS has been successfully opened.</p>
    """

    frappe.sendmail(
        recipients=emails,
        subject=subject,
        message=message
    )