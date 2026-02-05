frappe.ui.form.on("Purchase Invoice", {
	refresh(frm) {
		if (!frm.is_new()) return;

		frm.add_custom_button(
			__("Internal Transfer"),
			async () => {
				// Fetch already transferred Sales Invoices
				const r = await frappe.call({
					method: "customization_iconcept.internal_purchase.get_sales_invoices_already_transferred",
					args: {
						company: frm.doc.company,
					},
				});
				
				const excluded_sales_invoices = r.message || [];

				erpnext.utils.map_current_doc({
					method: "customization_iconcept.internal_purchase.make_internal_transfer_sales_invoice",
					source_doctype: "Sales Invoice",
					target: frm,
					setters: {
							custom_internal_branch: frm.doc.branch,
							customer: frm.doc.supplier,
							posting_date: undefined,
							company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1,
						is_internal_customer: 1,
						is_return: 0,
						company: frm.doc.company,
						name: ["not in", excluded_sales_invoices || []],
					},
					allow_child_item_selection: true,
					child_fieldname: "items",
					child_columns: [
						"item_code",
						"item_name",
						"qty",
						"rate",
						"amount",
						"warehouse",
					],
				});
			},
			__("Get Items From")
		);
	},
	
});
