# import frappe
# from erpnext.controllers.queries import purchase_order_query as core_query


# @frappe.whitelist()
# def purchase_order_query(doctype, txt, searchfield, start, page_len, filters):
#     columns, data = core_query(
#         doctype, txt, searchfield, start, page_len, filters
#     )

#     # Insert our custom column definition
#     columns.append({
#         "label": "Supplier Invoice No",
#         "fieldname": "custom_supplier_invoice_no",
#         "fieldtype": "Data",
#         "width": 180
#     })

#     # Add data value to each row
#     for row in data:
#         row.custom_supplier_invoice_no = frappe.db.get_value(
#             "Purchase Order", row.name, "custom_supplier_invoice_no"
#         )

#     return columns, data
