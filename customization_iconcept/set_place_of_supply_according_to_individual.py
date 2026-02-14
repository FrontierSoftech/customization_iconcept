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


# import frappe

# def set_place_of_supply(doc, method):
#     """
#     Set place_of_supply on Sales Invoice based on:
#     1. billing_address_gstin
#     2. fallback to Branch custom_place_of_supply
#     """

#     place_of_supply = None
#     gstin = None

#     if doc.get("billing_address_gstin"):
#         gstin = doc.billing_address_gstin.strip()


#     if gstin and len(gstin) >= 2:
#         state_code = gstin[:2]

#         # Get State name from State doctype
#         state_name = frappe.db.get_value(
#             "State",
#             {"gst_state_number": state_code},
#             "state_name"
#         )

#         if state_name:
#             place_of_supply = state_name.strip()


#     if not place_of_supply and doc.get("branch"):
#         branch_supply = frappe.db.get_value(
#             "Branch",
#             doc.branch,
#             "custom_place_of_supply"
#         )
#         if branch_supply:
#             place_of_supply = branch_supply.strip()


#     if place_of_supply:
#         doc.place_of_supply = place_of_supply
#     else:
#         # Optional: clear field if no value found
#         doc.place_of_supply = ""







