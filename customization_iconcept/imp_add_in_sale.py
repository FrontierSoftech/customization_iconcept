import frappe
from frappe import _

def check_address(doc, method):
    if doc.customer_address == 'Select address':
        frappe.throw(_('Please select a valid customer address'))
