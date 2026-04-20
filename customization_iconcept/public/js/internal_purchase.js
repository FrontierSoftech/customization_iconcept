frappe.ui.form.on("Purchase Invoice", {
	refresh(frm) {
		if (!frm.is_new()) return;

		frm.add_custom_button(
			__("Internal Transfer"),
			() => {
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
					get_query: () => ({
						query: "customization_iconcept.internal_purchase.query_available_internal_sales_invoices",
						filters: {
							company: frm.doc.company,
							customer: frm.doc.supplier,
							custom_internal_branch: frm.doc.branch,
						},
					}),
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
