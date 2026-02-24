frappe.query_reports["Day Book"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today()),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "voucher_type",
            "label": __("Voucher Type"),
            "fieldtype": "Select",
            "options": "\nSales Invoice\nPurchase Invoice\nSales Order\nPurchase Order\nPayment Entry\nJournal Entry\nPurchase Receipt\nDelivery Note\nStock Entry\nStock Reconciliation\nMaterial Request",
            "default": ""
        },
        // New Party Type filter
        {
            "fieldname": "party_type",
            "label": __("Party Type"),
            "fieldtype": "Select",
            "options": "\nCustomer\nSupplier",
            "default": "Customer",
            "on_change": function() {
                const party_type = frappe.query_report.get_filter_value('party_type');
                const party_field = frappe.query_report.get_filter('party');
                party_field.df.options = party_type;
                party_field.refresh();
                party_field.set_value('');
            }
        },
        {
            "fieldname": "party",
            "label": __("Party"),
            "fieldtype": "Link",
            "options": "Customer"  // Default, will change dynamically based on Party Type
        },
        {
            "fieldname": "branch",
            "label": __("Branch"),
            "fieldtype": "Link",
            "options": "Branch"
        },
        // {
        //     "fieldname": "title",
        //     "label": __("Title"),
        //     "fieldtype": "Data",
        //     // "options": "Account"
        // },
        {
            "fieldname": "cost_center",
            "label": __("Cost Center"),
            "fieldtype": "Link",
            "options": "Cost Center"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nDraft\nSubmitted\nCancelled",
            "default": ""
        },
        {
            "fieldname": "hide_cancelled",
            "label": __("Hide Cancelled Vouchers"),
            "fieldtype": "Check",
            "default": 0
        },
    ],

    // Formatter to make voucher clickable
    "formatter": function (value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname === "voucher_no" && data.voucher_type) {
            let route = frappe.router.slug(data.voucher_type);
            value = `<a href="/app/${route}/${data.voucher_no}" target="_blank">${value}</a>`;
        }

        return value;
    }
};