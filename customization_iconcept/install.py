# hooks.py
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field, get_custom_field

def after_install():
    # Check if field already exists
    if not get_custom_field("Mode of Payment", "custom_customer_name"):
        create_custom_field("Mode of Payment", {
            "fieldname": "custom_customer_name",
            "label": "Custom Customer",
            "fieldtype": "Link",
            "options": "Customer",  # Link to Customer DocType
            "insert_after": "enabled"
        })
