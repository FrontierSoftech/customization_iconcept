// frappe.ui.form.on("Purchase Invoice", {
// 	refresh(frm) {
// 		frm.add_custom_button(
// 			__("Internal Transfer Sales Invoices"),
// 			function () {
// 				frappe.call({
// 					method: "customization_iconcept.internal_purchase.get_internal_transfer_sales_invoices",
// 					args: {
// 						company: frm.doc.company
// 					},
// 					callback: function (r) {
// 						if (!r.message || r.message.length === 0) {
// 							frappe.msgprint(__("No pending Internal Transfer Sales Invoices found."));
// 							return;
// 						}

// 						frappe.prompt(
// 							[
// 								{
// 									fieldname: "sales_invoices",
// 									fieldtype: "MultiCheck",
// 									label: __("Sales Invoices"),
// 									options: r.message.map(d => ({
// 										label: `${d.name} | ${d.customer} | ${d.grand_total}`,
// 										value: d.name
// 									}))
// 								}
// 							],
// 							function (data) {
// 								console.log("Selected:", data.sales_invoices);
// 								// you can map items or create PI here
// 							},
// 							__("Select Sales Invoices"),
// 							__("Get Items")
// 						);
// 					}
// 				});
// 			},
// 			__("Get Items From")
// 		);
// 	}
// });

// frappe.ui.form.on("Purchase Invoice", {
// 	refresh(frm) {
// 		console.log("🔥 Internal Transfer JS loaded");

// 		// BUTTON — always visible
// 		frm.add_custom_button(
// 			__("Internal Transfer Sales Invoice"),
// 			function () {

// 				// Fetch eligible Sales Invoices
// 				frappe.call({
// 					method: "customization_iconcept.internal_purchase.get_internal_transfer_sales_invoices",
// 					args: {
// 						company: frm.doc.company
// 					},
// 					callback(r) {
// 						if (!r.message || !r.message.length) {
// 							frappe.msgprint(__("No Internal Transfer Sales Invoices found."));
// 							return;
// 						}

// 						const d = new frappe.ui.Dialog({
// 							title: __("Select Sales Invoice"),
// 							fields: [
// 								{
// 									fieldtype: "Select",
// 									fieldname: "sales_invoice",
// 									label: __("Sales Invoice"),
// 									options: r.message.map(row => row.name),
// 									reqd: 1
// 								}
// 							],
// 							primary_action_label: __("Get Items"),
// 							primary_action(values) {

// 								frappe.call({
// 									method: "customization_iconcept.internal_purchase.make_purchase_invoice_from_sales_invoice",
// 									args: {
// 										sales_invoice: values.sales_invoice
// 									},
// 									callback(r) {
// 										if (r.message) {
// 											frappe.model.sync(r.message);
// 											frappe.set_route(
// 												"Form",
// 												r.message.doctype,
// 												r.message.name
// 											);
// 										}
// 									}
// 								});

// 								d.hide();
// 							}
// 						});

// 						d.show();
// 					}
// 				});
// 			}
// 		);
// 	}
// });

frappe.ui.form.on("Purchase Invoice", {
	refresh(frm) {
		console.log("🔥 Internal Transfer JS Loaded");

		// Button to fetch Internal Transfer Sales Invoice
		frm.add_custom_button(
			__("Internal Transfer Sales Invoice"),
			function () {

				// Call server to get eligible Sales Invoices
				frappe.call({
					method: "customization_iconcept.internal_purchase.get_internal_transfer_sales_invoices",
					args: { company: frm.doc.company },
					callback(r) {
						if (!r.message || !r.message.length) {
							frappe.msgprint(__("No Internal Transfer Sales Invoices found."));
							return;
						}

						const d = new frappe.ui.Dialog({
							title: __("Select Sales Invoice"),
							fields: [
								{
									fieldtype: "Select",
									fieldname: "sales_invoice",
									label: __("Sales Invoice"),
									options: r.message.map(row => row.name),
									reqd: 1
								}
							],
							primary_action_label: __("Get Items"),
							primary_action(values) {
								frappe.call({
									method: "customization_iconcept.internal_purchase.make_purchase_invoice_from_sales_invoice",
									args: { sales_invoice: values.sales_invoice },
									callback(r) {
										if (r.message) {
											frappe.model.sync(r.message);
											frappe.set_route(
												"Form",
												r.message.doctype,
												r.message.name
											);
										}
									}
								});
								d.hide();
							}
						});
						d.show();
					}
				});
			}
		);
	}
});

