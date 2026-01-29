
frappe.ui.form.on('Journal Entry', {

    // refresh(frm) {
    //     frm.fields_dict['accounts'].grid.get_field('custom_reference_name_copy').get_query =
    //         function (doc, cdt, cdn) {
    //             const row = locals[cdt][cdn];

    //             if (row.reference_type !== "Journal Entry" || !row.account) {
    //                 return {};
    //             }

    //             return {
    //                 query: "customization_iconcept.api.journal_entry_with_outstanding",
    //                 filters: {
    //                     account: row.account,
    //                     party: row.party
    //                 }
    //             };
    //         };
    // },
    refresh(frm) {
        frm.fields_dict['accounts'].grid.get_field('custom_reference_name_copy').get_query =
            function (doc, cdt, cdn) {

                let jvd = locals[cdt][cdn];

                // ---- JOURNAL ENTRY (custom query) ----
                if (jvd.reference_type === "Journal Entry") {
                    frappe.model.validate_missing(jvd, "account");
                    frappe.model.validate_missing(jvd, "party");

                    return {
                        query: "customization_iconcept.api.journal_entry_with_outstanding",
                        filters: {
                            account: jvd.account,
                            party: jvd.party
                        }
                    };
                }

                // ---- STANDARD ERPNext LOGIC ----
                let out = {
                    filters: [[jvd.reference_type, "docstatus", "=", 1]]
                };

                if (["Sales Invoice", "Purchase Invoice"].includes(jvd.reference_type)) {
                    out.filters.push([jvd.reference_type, "outstanding_amount", "!=", 0]);

                    if (jvd.cost_center) {
                        out.filters.push([
                            jvd.reference_type,
                            "cost_center",
                            "in",
                            ["", jvd.cost_center]
                        ]);
                    }

                    frappe.model.validate_missing(jvd, "account");
                    let party_account_field =
                        jvd.reference_type === "Sales Invoice" ? "debit_to" : "credit_to";

                    out.filters.push([
                        jvd.reference_type,
                        party_account_field,
                        "=",
                        jvd.account
                    ]);
                }

                if (["Sales Order", "Purchase Order"].includes(jvd.reference_type)) {
                    frappe.model.validate_missing(jvd, "party_type");
                    frappe.model.validate_missing(jvd, "party");
                    out.filters.push([jvd.reference_type, "per_billed", "<", 100]);
                }

                if (jvd.party_type && jvd.party) {
                    let party_field = "";

                    if (jvd.reference_type.startsWith("Sales")) {
                        party_field = "customer";
                    } else if (jvd.reference_type.startsWith("Purchase")) {
                        party_field = "supplier";
                    }

                    if (party_field) {
                        out.filters.push([jvd.reference_type, party_field, "=", jvd.party]);
                    }
                }

                return out;
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