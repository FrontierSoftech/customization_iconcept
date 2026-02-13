import frappe

def set_branch_and_cost_center(doc, method):

    # Check if fields exist in this DocType
    if not hasattr(doc, "branch") or not hasattr(doc, "cost_center"):
        return

    if doc.branch and doc.cost_center:

        # Update items table if exists
        if hasattr(doc, "items"):
            for row in doc.items:
                if hasattr(row, "branch"):
                    row.branch = doc.branch
                if hasattr(row, "cost_center"):
                    row.cost_center = doc.cost_center

        # Update taxes table if exists
        if hasattr(doc, "taxes"):
            for tax in doc.taxes:
                if hasattr(tax, "branch"):
                    tax.branch = doc.branch
                if hasattr(tax, "cost_center"):
                    tax.cost_center = doc.cost_center


# def set_branch_and_cost_center(doc, method):
#     if doc.branch or doc.cost_center:
#         for tax in doc.taxes:
#             if doc.branch:
#                 tax.branch = doc.branch
#             if doc.cost_center:
#                 tax.cost_center = doc.cost_center
#         for item in doc.items:
#             if doc.branch:
#                 item.branch = doc.branch
#             if doc.cost_center:
#                 item.cost_center = doc.cost_center