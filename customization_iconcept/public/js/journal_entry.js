frappe.ui.form.on('Journal Entry', {
    custom_branch(frm) {
        if (frm.doc.custom_branch) {
            frm.doc.accounts.forEach(item => {
                item.branch = frm.doc.custom_branch;
            });
            frm.refresh_field('accounts');
        }
    },

    custom_cost_center(frm) {
        if (frm.doc.custom_cost_center) {
            frm.doc.accounts.forEach(item => {
                item.cost_center = frm.doc.custom_cost_center
            });
            frm.refresh_field('accounts')
        }
    }
});

frappe.ui.form.on('Journal Entry Account', {
    accounts_add(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if(frm.doc.custom_branch) {
            frappe.model.set_value(cdt, cdn, 'branch', frm.doc.custom_branch);
        }

        if (frm.doc.custom_cost_center) {
            frappe.model.set_value(cdt, cdn, 'cost_center', frm.doc.custom_cost_center);
        }
    }
});
