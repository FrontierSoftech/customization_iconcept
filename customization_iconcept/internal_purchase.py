
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt

from erpnext.accounts.doctype.sales_invoice.sales_invoice import (
	make_inter_company_purchase_invoice as erpnext_make_ic_pi
)
from erpnext.accounts.party import  get_party_details

@frappe.whitelist()
def make_internal_transfer_sales_invoice(source_name, target_doc=None, args=None):
	# return erpnext_make_ic_pi(source_name, target_doc)
	doc = erpnext_make_ic_pi(source_name, target_doc)

	# Fetch source Sales Invoice
	si = frappe.get_doc("Sales Invoice", source_name)

	# ---- Header warehouse mapping ----
	# Sales Invoice -> Purchase Invoice
	# doc.set_warehouse = si.set_warehouse
	doc.set_from_warehouse = si.set_target_warehouse
	doc.supplier_address = si.company_address
	doc.shipping_address =  si.customer_address

	# ---- Force branch to be NULL ----
	doc.branch = si.custom_internal_branch
	doc.shipping_address_display = si.address_display
	doc.bill_no = si.name
	
	party_details = get_party_details(
		party=doc.supplier,
		party_type="Supplier",
		company=doc.company,
		doctype="Purchase Invoice",
		party_address=doc.supplier_address,
		company_address=doc.company_address,
	)

	# Apply Purchase Tax Template automatically
	doc.taxes_and_charges = party_details.get("taxes_and_charges")

	if party_details.get("taxes"):
		doc.set("taxes", party_details.get("taxes"))

	doc.run_method("calculate_taxes_and_totals")
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


