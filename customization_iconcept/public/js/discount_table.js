frappe.ui.form.on('Sales Invoice', {
    refresh: function (frm) {
        update_total_discount(frm);
    }
});

frappe.ui.form.on('Sales Invoice Item', {
    rate: function (frm) {
        update_total_discount(frm);
    },
    items_add: function (frm) {
        update_total_discount(frm);
    },
    items_remove: function (frm) {
        update_total_discount(frm);
    }
});

frappe.ui.form.on('Discounts', {
    disc_: function (frm, cdt, cdn) {
        update_total_discount(frm);
    },
    discount: function (frm, cdt, cdn) {
        update_total_discount(frm);
    },
    custom_discount_ledger_add: function (frm) {
        update_total_discount(frm);
    },
    custom_discount_ledger_remove: function (frm) {
        update_total_discount(frm);
    }
});

function update_total_discount(frm) {
    let total_discount = 0;

    let base_amount = flt(
        frm.doc[frappe.scrub(frm.doc.apply_discount_on)] || 0
    );

    if (frm.doc.custom_discount_ledger && frm.doc.custom_discount_ledger.length) {
        frm.doc.custom_discount_ledger.forEach(function (row) {
            if (row.disc_) {
                row.discount = flt(frm.doc.base_total * row.disc_ / 100);
            }
        });
    }

    frm.doc.custom_discount_ledger.forEach(function (row) {
        total_discount += row.discount || 0;
    });
    
    frm.set_value('custom_total_discount', total_discount);
    frm.set_value('discount_amount', total_discount);
    frm.refresh_field('custom_discount_ledger');
}

// frappe.ui.form.on('Sales Invoice', {
//     refresh: function(frm) {
//         update_total_discount(frm);
//     }
// });

// frappe.ui.form.on('Discounts', {
//     discount: function(frm, cdt, cdn) {
//         update_total_discount(frm);
//     },
//     custom_discount_ledger_remove: function(frm, cdt, cdn) {
//         update_total_discount(frm);
//     },
//     custom_discount_ledger_add: function(frm, cdt, cdn) {
//         update_total_discount(frm);
//     }
// });

// function update_total_discount(frm) {
//     let total_discount = 0;
//     frm.doc.custom_discount_ledger.forEach(function(row) {

//         total_discount += row.discount || 0;
//     });
//     frm.set_value('custom_total_discount', total_discount);
//     frm.set_value('discount_amount', total_discount);
//     frm.refresh_field('custom_discount_ledger');
// }