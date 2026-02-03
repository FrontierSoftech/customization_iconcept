frappe.ui.form.on('Purchase Invoice', {
        custom_debit_note: function (frm) {
        if (frm.doc.custom_debit_note) {
            frm.set_value('is_return', 1);
        }else {
            frm.set_value('is_return', 0);
        }
    },
});