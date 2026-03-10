// Copyright (c) 2026, Frontier Softech and contributors
// For license information, please see license.txt

// frappe.query_reports["Batch Sales Invoice Report"] = {
// 	"filters": [

// 	]
// };

frappe.query_reports["Batch Sales Invoice Report"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company")
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "customer",
            "label": __("Party"),
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname": "set_warehouse",
            "label": __("Item Godown"),
            "fieldtype": "Link",
            "options": "Warehouse"
        }
    ],

    "formatter": function(value, row, column, data, default_formatter) {
        return default_formatter(value, row, column, data);
    }
};