# import frappe

# @frappe.whitelist()
# def get_internal_transfer_sales_invoices(company):
# 	return frappe.db.sql("""
# 		SELECT
# 			si.name,
# 			si.customer,
# 			si.grand_total
# 		FROM
# 			`tabSales Invoice` si
# 		WHERE
# 			si.docstatus = 1
# 			AND si.is_internal_transfer = 1
# 			AND si.company = %s
# 			AND NOT EXISTS (
# 				SELECT 1
# 				FROM `tabPurchase Invoice` pi
# 				WHERE pi.internal_transfer_sales_invoice = si.name
# 				AND pi.docstatus < 2
# 			)
# 		ORDER BY si.posting_date DESC
# 	""", company, as_dict=True)

# import frappe
# from frappe.model.mapper import get_mapped_doc


# @frappe.whitelist()
# def get_internal_transfer_sales_invoices(company):
# 	return frappe.db.sql("""
# 		SELECT
# 			si.name
# 		FROM
# 			`tabSales Invoice` si
# 		WHERE
# 			si.docstatus = 1
# 			AND si.company = %s
# 			AND si.name NOT IN (
# 				SELECT inter_company_invoice_reference
# 				FROM `tabPurchase Invoice`
# 				WHERE docstatus < 2
# 				AND inter_company_invoice_reference IS NOT NULL
# 			)
# 		ORDER BY si.posting_date DESC
# 	""", company, as_dict=True)


# @frappe.whitelist()
# def make_purchase_invoice_from_sales_invoice(sales_invoice):

# 	def postprocess(source, target):
# 		# Link Sales Invoice
# 		target.inter_company_invoice_reference = source.name

# 		# Set Supplier using inter-company rule (SAFE)
# 		supplier = frappe.get_value(
# 			"Supplier",
# 			{"represents_company": source.company},
# 			"name"
# 		)
# 		if supplier:
# 			target.supplier = supplier

# 	return get_mapped_doc(
# 		"Sales Invoice",
# 		sales_invoice,
# 		{
# 			"Sales Invoice": {
# 				"doctype": "Purchase Invoice",
# 				"field_map": {
# 					"name": "inter_company_invoice_reference",
# 					"posting_date": "posting_date",
# 					"due_date": "due_date"
# 				}
# 			},
# 			"Sales Invoice Item": {
# 				"doctype": "Purchase Invoice Item",
# 				"field_map": {
# 					"item_code": "item_code",
# 					"qty": "qty",
# 					"rate": "rate",
# 					"amount": "amount"
# 				}
# 			}
# 		},
# 		target_doc=None,
# 		postprocess=postprocess
# 	)

# import frappe
# from frappe.model.mapper import get_mapped_doc

# @frappe.whitelist()
# def get_internal_transfer_sales_invoices(company):
#     """
#     Fetch submitted Sales Invoices that do not yet have
#     a linked Purchase Invoice (Inter-Company).
#     """
#     return frappe.db.sql("""
#         SELECT
#             si.name
#         FROM
#             `tabSales Invoice` si
#         WHERE
#             si.docstatus = 1
#             AND si.company = %s
#             AND si.name NOT IN (
#                 SELECT inter_company_invoice_reference
#                 FROM `tabPurchase Invoice`
#                 WHERE docstatus < 2
#                 AND inter_company_invoice_reference IS NOT NULL
#             )
#         ORDER BY si.posting_date DESC
#     """, company, as_dict=True)


# @frappe.whitelist()
# def make_purchase_invoice_from_sales_invoice(sales_invoice):
#     """
#     Create a new Purchase Invoice from a Sales Invoice
#     for internal transfer purposes.
#     """

#     def postprocess(source, target):
#         # Link Sales Invoice
#         target.inter_company_invoice_reference = source.name

#         # Set Supplier safely using represents_company
#         supplier = frappe.get_value(
#             "Supplier",
#             {"represents_company": source.company},
#             "name"
#         )
#         if supplier:
#             target.supplier = supplier

#         # Remove any taxes to avoid template mismatch errors
#         target.taxes = []
#         target.taxes_and_charges = None

#     return get_mapped_doc(
#         "Sales Invoice",
#         sales_invoice,
#         {
#             "Sales Invoice": {
#                 "doctype": "Purchase Invoice",
#                 "field_map": {
#                     "name": "inter_company_invoice_reference",
#                     "posting_date": "posting_date",
#                     "due_date": "due_date"
#                 }
#             },
#             "Sales Invoice Item": {
#                 "doctype": "Purchase Invoice Item",
#                 "field_map": {
#                     "item_code": "item_code",
#                     "qty": "qty",
#                     "rate": "rate",
#                     "amount": "amount"
#                 }
#             }
#         },
#         target_doc=None,
#         postprocess=postprocess
#     )

import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def get_internal_transfer_sales_invoices(company):
    """
    Fetch submitted Sales Invoices that do not yet have
    a linked Purchase Invoice (Inter-Company).
    """
    return frappe.db.sql("""
        SELECT
            si.name
        FROM
            `tabSales Invoice` si
        WHERE
            si.docstatus = 1
            AND si.company = %s
            AND si.name NOT IN (
                SELECT inter_company_invoice_reference
                FROM `tabPurchase Invoice`
                WHERE docstatus < 2
                AND inter_company_invoice_reference IS NOT NULL
            )
        ORDER BY si.posting_date DESC
    """, company, as_dict=True)


@frappe.whitelist()
def make_purchase_invoice_from_sales_invoice(sales_invoice):
    """
    Create a new Purchase Invoice from a Sales Invoice
    for internal transfer purposes.
    """

    def postprocess(source, target):
        # Link Sales Invoice
        target.inter_company_invoice_reference = source.name

        # Set Supplier safely
        supplier = frappe.get_value(
            "Supplier",
            {"represents_company": source.company},
            "name"
        )
        if supplier:
            target.supplier = supplier

        # Remove any Taxes to avoid template mismatch errors
        target.taxes = []
        target.taxes_and_charges = None

    return get_mapped_doc(
        "Sales Invoice",
        sales_invoice,
        {
            "Sales Invoice": {
                "doctype": "Purchase Invoice",
                "field_map": {
                    "name": "inter_company_invoice_reference",
                    "posting_date": "posting_date",
                    "due_date": "due_date"
                }
            },
            "Sales Invoice Item": {
                "doctype": "Purchase Invoice Item",
                "field_map": {
                    "item_code": "item_code",
                    "qty": "qty",
                    "rate": "rate",
                    "amount": "amount"
                },
                "add_if_empty": True  # Ensures at least one row is created
            }
        },
        target_doc=None,
        postprocess=postprocess
    )

