import frappe
# Ensure branch exists
def share_internal_trans_to_sm(doc, method):
    if doc.custom_internal_branch:

        # Get Branch document
        branch = frappe.get_doc("Branch", doc.custom_internal_branch)

        # Loop through child table of store manager users
        if branch.custom_store_manager_user:
            for row in branch.custom_store_manager_user:
                store_manager = row.user  # or whatever the fieldname is in child table

                # Check existing share
                exists = frappe.db.exists(
                    "DocShare",
                    {
                        "share_doctype": doc.doctype,
                        "share_name": doc.name,
                        "user": store_manager
                    }
                )

                if not exists:
                    share = frappe.new_doc("DocShare")
                    share.share_doctype = doc.doctype
                    share.share_name = doc.name
                    share.user = store_manager
                    share.read = 1
                    share.write = 1
                    share.submit = 0
                    share.share = 0

                    # IMPORTANT for server script
                    share.flags.ignore_permissions = True
                    share.insert()