
frappe.ui.form.on('Journal Entry', {

    refresh(frm) {
        frm.fields_dict['accounts'].grid.get_field('custom_reference_name_copy').get_query =
            function (doc, cdt, cdn) {
                const row = locals[cdt][cdn];

                if (row.reference_type !== "Journal Entry" || !row.account) {
                    return {};
                }

                return {
                    query: "customization_iconcept.api.journal_entry_with_outstanding",
                    filters: {
                        account: row.account,
                        party: row.party
                    }
                };
            };
    },

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

        if (frm.doc.custom_branch) {
            frappe.model.set_value(cdt, cdn, 'branch', frm.doc.custom_branch);
        }

        if (frm.doc.custom_cost_center) {
            frappe.model.set_value(cdt, cdn, 'cost_center', frm.doc.custom_cost_center);
        }
    },

    custom_reference_name_copy: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        refresh_reference_name_query(frm, cdt, cdn);
        setTimeout(() => {
            frappe.model.set_value(
                cdt,
                cdn,
                "reference_name",
                row.custom_reference_name_copy
            );
        }, 500);
    }
});

function refresh_reference_name_query(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    if (row.reference_type === "Journal Entry" && row.custom_reference_name_copy) {
        frappe.call({
            method: "customization_iconcept.api.get_journal_entry_outstanding",
            args: {
                journal_entry: row.custom_reference_name_copy,
                account: row.account,
                party: row.party
            },
            callback: function (r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, "credit_in_account_currency", r.message.outstanding);
                    frappe.model.set_value(cdt, cdn, "debit_in_account_currency", 0);
                }
            }
        });
    }
}