frappe.ui.form.on("POS Invoice", {
    before_submit: async function(frm) {
        let payment_rows_needing_reference = [];

        // Step 1: Check each payment row
        for (let row of (frm.doc.payments || [])) {
            let r = await frappe.db.get_value(
                "Mode of Payment",
                row.mode_of_payment,
                "custom_customer_name"
            );

            // Check if the row needs a reference
            if (r.message && r.message.custom_customer_name && !row.reference_number) {
                payment_rows_needing_reference.push({
                    row: row,
                    default: r.message.custom_customer_name
                });
            }
        }

        // Step 2: If none need reference, allow submit
        if (!payment_rows_needing_reference.length) return;

        // Step 3: Build prompt fields dynamically
        let fields = payment_rows_needing_reference.map((item, i) => ({
            fieldname: `reference_${i}`,
            fieldtype: "Data",
            label: `Reference for ${item.row.mode_of_payment}`,
            default: item.default
        }));

        // Stop automatic submit
        frappe.validated = false;

        // Step 4: Show prompt
        frappe.prompt(
            fields,
            async function(values) {
                // Step 5: Fill references in child table
                payment_rows_needing_reference.forEach((item, i) => {
                    item.row.reference_number = values[`reference_${i}`];

                    // If your child table field is actually `reference_no`, set it as well
                    if (item.row.hasOwnProperty('reference_no')) {
                        item.row.reference_no = values[`reference_${i}`];
                    }
                });

                // Refresh the child table to reflect changes
                frm.refresh_field("payments");

                // Step 6: Allow submit and submit automatically
                frappe.validated = true;

                // Optionally, submit automatically
                // await frm.submit();
            },
            __("Reference Required"),
            "Save"
        );
    }
});
