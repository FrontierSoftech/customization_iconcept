frappe.ui.form.on('Sales Invoice Item', {
    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Bin",
                filters: {
                    item_code: row.item_code,
                    warehouse: row.warehouse
                },
                fieldname: "valuation_rate"
            },
            callback: function(r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, 'custom_valuation_rate', r.message.valuation_rate);
                }
            }
        });
    },
    warehouse: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Bin",
                filters: {
                    item_code: row.item_code,
                    warehouse: row.warehouse
                },
                fieldname: "valuation_rate"
            },
            callback: function(r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, 'custom_valuation_rate', r.message.valuation_rate);
                }
            }
        });
    }
    
});