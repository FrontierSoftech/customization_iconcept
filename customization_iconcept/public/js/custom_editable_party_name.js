frappe.ui.form.on('Sales Invoice', {
    customer(frm) {
        if (!frm.doc.customer) return;

        frappe.db.get_value(
            'Customer',
            frm.doc.customer,
            'custom_party_name_for_print'
        ).then(r => {
            if (r.message) {
                frm.set_value(
                    'custom_party_name',
                    r.message.custom_party_name_for_print
                );
            }
        });
    },

    custom_party_name(frm) {
        // mark that user changed the value
        frm._party_name_changed = true;
    },

    before_save(frm) {
        if (!frm._party_name_changed || !frm.doc.customer) return;

        frappe.call({
            method: 'frappe.client.set_value',
            args: {
                doctype: 'Customer',
                name: frm.doc.customer,
                fieldname: 'custom_party_name_for_print',
                value: frm.doc.custom_party_name
            },
            callback() {
                frm._party_name_changed = false;
            }
        });
    }
});

