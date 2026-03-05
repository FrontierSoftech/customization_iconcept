frappe.ui.form.on('Sales Invoice', {

    customer: function(frm) {
        if (frm.doc.customer === "IConcept") {
            frm.set_value("custom_is_stock_transfer", 1);
        } else {
            frm.set_value("custom_is_stock_transfer", 0);
        }
    },

    onload: function(frm) {
        if (frm.doc.customer === "IConcept") {
            frm.set_value("custom_is_stock_transfer", 1);
        }
    }

});