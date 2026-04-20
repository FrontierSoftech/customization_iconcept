
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
@frappe.validate_and_sanitize_search_inputs
def query_available_internal_sales_invoices(doctype, txt, searchfield, start, page_len, filters):
	import json
	if isinstance(filters, str):
		filters = json.loads(filters)

	filters = filters or {}
	company = filters.get("company")
	customer = filters.get("customer")
	branch = filters.get("custom_internal_branch")
	posting_date = filters.get("posting_date")

	extra_conditions = []
	values = {"company": company, "txt": f"%{txt}%", "page_len": int(page_len), "start": int(start)}

	if customer:
		extra_conditions.append("AND si.customer = %(customer)s")
		values["customer"] = customer
	if branch:
		extra_conditions.append("AND si.custom_internal_branch = %(branch)s")
		values["branch"] = branch
	if posting_date:
		extra_conditions.append("AND si.posting_date = %(posting_date)s")
		values["posting_date"] = posting_date

	return frappe.db.sql(
		f"""
		SELECT si.name, si.customer, si.posting_date, si.company, si.custom_internal_branch
		FROM `tabSales Invoice` si
		WHERE
			si.docstatus = 1
			AND si.is_internal_customer = 1
			AND si.is_return = 0
			AND si.company = %(company)s
			AND si.name LIKE %(txt)s
			AND si.name NOT IN (
				SELECT DISTINCT pi.inter_company_invoice_reference
				FROM `tabPurchase Invoice` pi
				WHERE
					pi.docstatus = 1
					AND pi.is_internal_supplier = 1
					AND pi.inter_company_invoice_reference IS NOT NULL
			)
			{"".join(extra_conditions)}
		ORDER BY si.posting_date DESC
		LIMIT %(page_len)s OFFSET %(start)s
		""",
		values,
		as_dict=True,
	)


