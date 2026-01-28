frappe.ui.form.on('Purchase Order', {

    onload: function(frm) {
        frm._old_schedule_date = frm.doc.schedule_date;
        sync_schedule_date(frm);
    },

    refresh: function(frm) {
        frm._old_schedule_date = frm.doc.schedule_date;
    },

    transaction_date: function(frm) {
        sync_schedule_date(frm);
    },

    // When header "Required By" is changed manually
    schedule_date: function(frm) {
        update_items_schedule_date(frm);
        frm._old_schedule_date = frm.doc.schedule_date;
    },
    __newname(frm) {
		frm.set_value('bill_no', frm.doc.__newname);
	}
});

/**
 * Sync header schedule_date with transaction_date
 */
function sync_schedule_date(frm) {
    if (frm.doc.transaction_date) {
        frm.set_value('schedule_date', frm.doc.transaction_date);
    }
}

/**
 * Update item schedule_date ONLY if user has not manually changed it
 */
function update_items_schedule_date(frm) {
    const new_date = frm.doc.schedule_date;
    const old_date = frm._old_schedule_date;

    if (!new_date) return;

    (frm.doc.items || []).forEach(row => {

        // Update ONLY if:
        // 1. Empty
        // 2. Previously same as header (not user-modified)
        if (!row.schedule_date || row.schedule_date === old_date) {
            row.schedule_date = new_date;
        }
    });

    frm.refresh_field('items');
}
