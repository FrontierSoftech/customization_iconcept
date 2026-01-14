
// frappe.provide('frappe.ui.form');

// frappe.ui.form.CustomerQuickEntryForm = frappe.ui.form.QuickEntryForm.extend({
//     render_dialog: function() {
//         this._super(this.doctype, this.after_insert);
//         // Example: Move 'mobile_no' to the top of mandatory fields
//         this.mandatory = this.get_variant_fields().concat(this.mandatory);
//     },
//     get_variant_fields: function() {
//         return ['mobile_no']; // Fields to move to the top
//     }
// });