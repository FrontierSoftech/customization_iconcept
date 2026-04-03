import frappe
from frappe import _

def check_address(doc, method):
    if doc.customer_address == 'Select address':
        frappe.throw(_('Please select a valid customer address'))
        
def mandatory_item_value(doc, method):
    if doc.is_internal_customer:
        for item in doc.items:
            if item.rate == 0:
                frappe.throw(f"Row #{item.idx}: Rate cannot be 0 for internal customer")
