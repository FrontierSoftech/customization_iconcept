import frappe
@frappe.whitelist()
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
    
@frappe.whitelist()
def notify_store_managers_for_open(method=None):
    # 🔹 Fetch all open POS entries
    pos_entries = frappe.get_all(
        "POS Opening Entry",
        filters={"status": "Open"},
        fields=["name", "pos_profile"]
    )

    if not pos_entries:
        return

    for entry in pos_entries:
        if not entry.pos_profile:
            continue

        # Get POS Profile
        pos_profile = frappe.get_doc("POS Profile", entry.pos_profile)
        if not pos_profile.branch:
            continue

        branch_doc = frappe.get_doc("Branch", pos_profile.branch)
        emails = []

        # Collect emails from child table
        for row in branch_doc.custom_store_manager_user:
            if row.user:
                email = frappe.db.get_value("User", row.user, "email")
                if email:
                    emails.append(email)

        if not emails:
            continue

        # Prepare email
        subject = f"POS Opened - {entry.name}"
        message = f"""
        <h3>POS Closing Notification</h3>
        <p><b>POS Opening:</b> <a href="{frappe.utils.get_url_to_form('POS Opening Entry', entry.name)}">{entry.name}</a></p>
        <p><b>Branch:</b> {pos_profile.branch}</p>
        <p>Please Close the POS.</p>
        """

        # Send email
        frappe.sendmail(recipients=emails, subject=subject, message=message)
    