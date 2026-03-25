import frappe

GST_STATES = {
    "01": "Jammu and Kashmir",
    "02": "Himachal Pradesh",
    "03": "Punjab",
    "04": "Chandigarh",
    "05": "Uttarakhand",
    "06": "Haryana",
    "07": "Delhi",
    "08": "Rajasthan",
    "09": "Uttar Pradesh",
    "10": "Bihar",
    "11": "Sikkim",
    "12": "Arunachal Pradesh",
    "13": "Nagaland",
    "14": "Manipur",
    "15": "Mizoram",
    "16": "Tripura",
    "17": "Meghalaya",
    "18": "Assam",
    "19": "West Bengal",
    "20": "Jharkhand",
    "21": "Odisha",
    "22": "Chhattisgarh",
    "23": "Madhya Pradesh",
    "24": "Gujarat",
    "26": "Dadra and Nagar Haveli and Daman and Diu",
    "27": "Maharashtra",
    "29": "Karnataka",
    "30": "Goa",
    "31": "Lakshadweep Islands",
    "32": "Kerala",
    "33": "Tamil Nadu",
    "34": "Puducherry",
    "35": "Andaman and Nicobar Islands",
    "36": "Telangana",
    "37": "Andhra Pradesh",
    "38": "Ladakh",
    "96": "Other Countries",
    "97": "Other Territory"
}

def set_place_of_supply(doc, method):
    if not doc.customer or not doc.branch:
        return

    customer = frappe.db.get_value(
        "Customer",
        doc.customer,
        ["customer_type", "gstin"],
        as_dict=True
    )

    if not customer:
        return

    if customer.customer_type == "Individual":

        if customer.gstin:
            state_code = customer.gstin[:2]

            state_name = GST_STATES.get(state_code)

            if state_name:
                doc.place_of_supply = f"{state_code}-{state_name}"
                return

        # fallback to branch field
        custom_place_of_supply = frappe.db.get_value(
            "Branch",
            doc.branch,
            "custom_place_of_supply"
        )

        if custom_place_of_supply:
            doc.place_of_supply = custom_place_of_supply

# import frappe

# def set_place_of_supply(doc, method):
#     # Ensure customer and branch are set
#     if not doc.customer or not doc.branch:
#         return

#     # Get customer details
#     customer = frappe.db.get_value(
#         "Customer",
#         doc.customer,
#         ["customer_type", "gstin"],
#         as_dict=True
#     )

#     if not customer:
#         return

#     # Check if customer is Individual
#     if customer.customer_type == "Individual":

#         # If GSTIN exists, derive state from GSTIN
#         if customer.gstin:
#             state_code = customer.gstin[:2]

#             # Find state using GST state code
#             state = frappe.db.get_value(
#                 "Address",
#                 {"gst_state_number": state_code},
#                 "gst_state"
#             )

#             if state:
#                 doc.place_of_supply = f"{state_code}-{state}"
#                 return

#         # If no GSTIN, fallback to Branch custom_place_of_supply
#         custom_place_of_supply = frappe.db.get_value(
#             "Branch",
#             doc.branch,
#             "custom_place_of_supply"
#         )

#         if custom_place_of_supply:
#             doc.place_of_supply = custom_place_of_supply




