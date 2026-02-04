
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt

from erpnext.accounts.doctype.sales_invoice.sales_invoice import (
	make_inter_company_purchase_invoice as erpnext_make_ic_pi
)

# @frappe.whitelist()
# def make_internal_transfer_sales_invoice(source_name, target_doc=None, args=None):
# 	source_doc = frappe.get_doc("Sales Invoice", source_name)

# 	def validate_internal_transfer(source_doc):
# 		if source_doc.docstatus != 1:
# 			frappe.throw(_("Only submitted Sales Invoices can be used"))
# 		if source_doc.is_return:
# 			frappe.throw(_("Return Sales Invoices are not allowed"))
# 		if not source_doc.is_internal_customer:
# 			frappe.throw(_("Sales Invoice is not marked as Internal Customer"))

# 	validate_internal_transfer(source_doc)

# 	def set_missing_values(source, target):
# 		target.is_internal_supplier = 1
# 		# target.run_method("set_missing_values")
# 		target.run_method("calculate_taxes_and_totals")

# 	def update_details(source, target, source_parent):
# 		target.company = source.company
# 		target.posting_date = source.posting_date
# 		target.supplier = source.customer
# 		target.currency = source.currency
# 		target.ignore_pricing_rule = 1
# 		target.inter_company_invoice_reference = source.name

# 	def update_item(source, target, source_parent):
# 		target.qty = flt(source.qty)
# 		target.rate = source.rate
# 		target.amount = flt(source.qty) * flt(source.rate)

# 		# Preserve warehouse for stock entry alignment
# 		if source.warehouse:
# 			target.warehouse = source.warehouse

# 		# Link back to Sales Invoice
# 		target.sales_invoice = source.parent
# 		target.sales_invoice_item = source.name

# 	item_field_map = {
# 		"doctype": "Purchase Invoice Item",
# 		"field_map": {
# 			"name": "sales_invoice_item",
# 			"item_code": "item_code",
# 			"item_name": "item_name",
# 			"description": "description",
# 			"uom": "uom",
# 			"conversion_factor": "conversion_factor",
# 			"income_account": "expense_account",
# 		},
# 		"postprocess": update_item,
# 		"condition": lambda doc: doc.qty > 0,
# 	}

# 	doclist = get_mapped_doc(
# 		"Sales Invoice",
# 		source_name,
# 		{
# 			"Sales Invoice": {
# 				"doctype": "Purchase Invoice",
# 				"postprocess": update_details,
# 				"field_no_map": [
# 					"taxes_and_charges",
# 					"set_warehouse",
# 				],
# 			},
# 			"Sales Invoice Item": item_field_map,
# 		},
# 		target_doc,
# 		set_missing_values,
# 	)

# 	return doclist

@frappe.whitelist()
def make_internal_transfer_sales_invoice(source_name, target_doc=None, args=None):
	# return erpnext_make_ic_pi(source_name, target_doc)
	doc = erpnext_make_ic_pi(source_name, target_doc)

	# Fetch source Sales Invoice
	si = frappe.get_doc("Sales Invoice", source_name)

	# ---- Header warehouse mapping ----
	# Sales Invoice -> Purchase Invoice
	doc.set_warehouse = si.set_warehouse
	doc.set_from_warehouse = si.set_target_warehouse

	# ---- Force branch to be NULL ----
	doc.branch = None
	return doc

@frappe.whitelist()
def get_sales_invoices_already_transferred(company):
	"""
	Return Sales Invoices that already have an Internal Transfer Purchase Invoice
	"""
	return frappe.db.sql_list(
		"""
		SELECT DISTINCT inter_company_invoice_reference
		FROM `tabPurchase Invoice`
		WHERE
			docstatus = 1
			AND is_internal_supplier = 1
			AND inter_company_invoice_reference IS NOT NULL
			AND company = %s
		""",
		(company,),
	)
