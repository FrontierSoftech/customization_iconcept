frappe.ui.form.on('Purchase Invoice', {
    bill_date: function(frm) {
        calculate_due_date(frm);
    },

    custom_credit_days: function(frm) {
        calculate_due_date(frm);
    },

    supplier: function(frm) {
        calculate_due_date(frm);
    },

    refresh: function(frm) {
        calculate_due_date(frm);
    }
});

function calculate_due_date(frm) {

    if (!frm.doc.bill_date || !frm.doc.custom_credit_days) {
        return;
    }

    let credit_days = cint(frm.doc.custom_credit_days);

    let calculated_due_date = frappe.datetime.add_days(
        frm.doc.bill_date,
        credit_days
    );

    // Clear payment terms to prevent override
    if (frm.doc.payment_terms_template) {
        frm.set_value("payment_terms_template", "");
    }

    frm.set_value("due_date", calculated_due_date);
}
