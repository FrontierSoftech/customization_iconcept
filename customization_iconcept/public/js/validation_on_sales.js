frappe.ui.form.on('Sales Invoice', {

    discount_amount: function (frm) {
        calculate_grand_total1(frm);
        calculate_grand_total(frm);
    },

    before_submit: async function (frm) {
        try {

            calculate_grand_total1(frm);
            calculate_grand_total(frm);

            if (frm.doc.is_return) {
                return;
            }
            // Step 1: Get the Customer Group from the selected Customer
            const customer_res = await frappe.db.get_value("Customer", frm.doc.customer, "customer_group");
            if (customer_res.message) {
                const customer_group = customer_res.message.customer_group;
                // Step 2: Get the custom checkbox value from the Customer Group
                const group_res = await frappe.db.get_value("Customer Group", customer_group, "custom_stop_auto_creation");
                if (group_res.message) {
                    const stop_auto_creation = group_res.message.custom_stop_auto_creation;
                    // If auto creation is stopped (i.e. checkbox is checked), prevent saving
                    if (!stop_auto_creation) {
                        if (frm.doc.custom_balance !== 0) {
                            frappe.msgprint(__('Payment List Amount Should be Zero .', [frm.doc.custom_balance]));
                            frappe.validated = false;
                        }
                    }
                }
            }
        } catch (err) {
            console.error(err);
            frappe.throw(__('An error occurred while checking customer group settings.'));
        }

    },

    custom_is_this_tax_included_in_basic_rate(frm) {
        const checked = frm.doc.custom_is_this_tax_included_in_basic_rate;

        frm.doc.taxes.forEach(row => {
            frappe.model.set_value(row.doctype, row.name, 'included_in_print_rate', checked);
        });

        calculate_grand_total1(frm);
        calculate_grand_total(frm);
    },
    refresh(frm) {
        const checked = frm.doc.custom_is_this_tax_included_in_basic_rate;

        frm.doc.taxes.forEach(row => {
            frappe.model.set_value(row.doctype, row.name, 'included_in_print_rate', checked);
        });
        frm.fields_dict['custom_finance_lender_payments'].grid.get_field('finance_lender').get_query = function (doc, cdt, cdn) {
            let child = locals[cdt][cdn];
            if (child.mode === "Account") {
                return {
                    filters: {
                        account_type: ['in', ['Bank', 'Cash']],
                        is_group: 0
                    }
                };
            }
            if (child.mode === "Customer") {
                return {
                    filters: {
                        customer_group: "Finance Lender"
                    }
                };
            }
        };
        if (frm.doc.custom_sales_ledger) {
            frm.doc.items.forEach(row => {
                frappe.model.set_value(row.doctype, row.name, 'income_account', frm.doc.custom_sales_ledger);
            });
        }
    },
    customer: function (frm) {
        if (frm.doc.customer) {
            frappe.db.get_value(
                "Customer",
                frm.doc.customer,
                "is_internal_customer"
            ).then(r => {
                const internal = r.message.is_internal_customer;

                frm.set_value(
                    'custom_is_this_tax_included_in_basic_rate',
                    internal ? 0 : 1
                );
                frm.toggle_reqd("sales_team", !internal);  

            }); 
        }
    },
    custom_credit_note: function (frm) {
        if (frm.doc.custom_credit_note) {
            frm.set_value('is_return', 1);
        }else {
            frm.set_value('is_return', 0);
        }
    },
    custom_sales_ledger: function (frm) {
        frm.doc.items.forEach(row => {
            frappe.model.set_value(row.doctype, row.name, 'income_account', frm.doc.custom_sales_ledger);
        });
    },
    before_save: function (frm) {
        let total_payment = 0;
        // Ensure the custom_balance is always calculated based on the latest rounded_total
        frm.refresh_field('custom_balance');
        frm.set_value('custom_balance', frm.doc.outstanding_amount);
        frm.set_value('custom_total_amount', frm.doc.outstanding_amount);
        (frm.doc.custom_finance_lender_payments || []).forEach(function (item) {
            total_payment += item.amount || 0;
        });
        // Calculate and set custom_balance again after payments are summed up
        const balance = (frm.doc.custom_balance || 0) - total_payment;
        frm.set_value('custom_balance', balance);
    }

});

frappe.ui.form.on('Sales Invoice Item', {
    item_code: function (frm, cdt, cdn) {
        calculate_grand_total1(frm);
    },
    qty: function (frm, cdt, cdn) {
        calculate_grand_total1(frm);
    },
    rate: function (frm, cdt, cdn) {
        calculate_grand_total1(frm);
    }
});

// Trigger recalculation of grand total when a new item is selected or updated in Custom Payment List
frappe.ui.form.on('Finance Lender Options', {

    finance_lender: function (frm, cdt, cdn) {
        calculate_grand_total(frm);
    },
    amount: function (frm, cdt, cdn) {
        calculate_grand_total(frm);
    }
});

frappe.ui.form.on('Sales Taxes and Charges', {
    rate: function (frm, cdt, cdn) {
        calculate_grand_total1(frm);
        calculate_grand_total(frm)
    }
});

function calculate_grand_total1(frm) {
    let total_payment = 0;
    // Ensure the custom_balance is always calculated based on the latest rounded_total
    setTimeout(() => {
        frm.refresh_field('custom_balance');
        frm.set_value('custom_balance', frm.doc.outstanding_amount);
        frm.set_value('custom_total_amount', frm.doc.outstanding_amount);
        (frm.doc.custom_finance_lender_payments || []).forEach(function (item) {
            total_payment += item.amount || 0;
        });

        // Clate and set custom_balance again after payments are summed up
        const balance = (frm.doc.custom_balance || 0) - total_payment;
        frm.set_value('custom_balance', balance);
    }, 1000);
}
function calculate_grand_total(frm) {
    let balance = frm.doc.outstanding_amount || 0;

    (frm.doc.custom_finance_lender_payments || []).forEach(function (row) {
        if (row.amount) {
            balance -= row.amount;
        }
    });

    // Update custom_balance
    frm.set_value('custom_balance', (balance));
}
