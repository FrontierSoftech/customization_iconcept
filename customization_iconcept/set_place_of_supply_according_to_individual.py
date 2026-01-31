import frappe

def set_place_of_supply(doc, method):
    # Ensure customer and branch are set
    if not doc.customer or not doc.branch:
        return

    # Get customer type
    customer_type = frappe.db.get_value(
        "Customer",
        doc.customer,
        "customer_type"
    )

    # Check if customer is Individual
    if customer_type == "Individual":

        # Get custom_place_of_supply from Branch
        custom_place_of_supply = frappe.db.get_value(
            "Branch",
            doc.branch,
            "custom_place_of_supply"
        )

        # Set place_of_supply in Sales Invoice
        if custom_place_of_supply:
            doc.place_of_supply = custom_place_of_supply


