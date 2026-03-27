const GST_STATES = {
    "01": "Jammu and Kashmir",
    "02": "Himachal Pradesh",
    "03": "Punjab",
    "04": "Chandigarh",
    "05": "Uttarakhand",
    "06": "Haryana",
    "07": "Delhi",
    "08": "Rajasthan",
    "09": "Uttar Pradesh",
    "10": "Bihar",
    "11": "Sikkim",
    "12": "Arunachal Pradesh",
    "13": "Nagaland",
    "14": "Manipur",
    "15": "Mizoram",
    "16": "Tripura",
    "17": "Meghalaya",
    "18": "Assam",
    "19": "West Bengal",
    "20": "Jharkhand",
    "21": "Odisha",
    "22": "Chhattisgarh",
    "23": "Madhya Pradesh",
    "24": "Gujarat",
    "26": "Dadra and Nagar Haveli and Daman and Diu",
    "27": "Maharashtra",
    "29": "Karnataka",
    "30": "Goa",
    "31": "Lakshadweep Islands",
    "32": "Kerala",
    "33": "Tamil Nadu",
    "34": "Puducherry",
    "35": "Andaman and Nicobar Islands",
    "36": "Telangana",
    "37": "Andhra Pradesh",
    "38": "Ladakh",
    "96": "Other Countries",
    "97": "Other Territory"
};

frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        if (frm.doc.docstatus !== 0) return;
        set_place_of_supply(frm);
    }
});

frappe.ui.form.on('Sales Invoice Item', {
    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        apply_inclusive_gst(frm);
        frm.refresh_field('place_of_supply');
        frappe.model.set_value(cdt, cdn, 'branch', frm.doc.branch);
        frappe.model.set_value(cdt, cdn, 'cost_center', frm.doc.cost_center);
    }
});

function apply_inclusive_gst(frm) {
    if (!frm.doc.custom_is_this_tax_included_in_basic_rate) return;

    (frm.doc.taxes || []).forEach(row => {
        row.included_in_print_rate = frm.doc.custom_is_this_tax_included_in_basic_rate;
    });

    frm.refresh_field('taxes');
}

function set_place_of_supply(frm) {
    // Ensure customer and branch are set
    if (!frm.doc.customer || !frm.doc.branch) {
        return;
    }
    // Get customer details
    frappe.db.get_value('Customer', frm.doc.customer, ['customer_type', 'gstin'])
        .then(r => {
            if (!r.message) return;

            let customer = r.message;

            // Check if customer is Individual
            if (customer.customer_type === "Individual") {

                // If GSTIN exists
                if (customer.gstin) {
                    let state_code = customer.gstin.substring(0, 2);
                    let state_name = GST_STATES[state_code];

                    // Get state from Address
                    if (state_name) {
                        frm.set_value(
                            'place_of_supply',
                            `${state_code}-${state_name}`
                        );
                        return;
                    }

                } else {
                    // Fallback to Branch custom_place_of_supply
                    frappe.db.get_value('Branch', frm.doc.branch, 'custom_place_of_supply')
                        .then(res => {
                            if (res.message && res.message.custom_place_of_supply) {
                                frm.set_value(
                                    'place_of_supply',
                                    res.message.custom_place_of_supply
                                );
                            }
                    });
                }
            }
        });
}