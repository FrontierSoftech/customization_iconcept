// Copyright (c) 2026, Frontier Softech and contributors
// For license information, please see license.txt

// frappe.query_reports["Sales Invoice Report"] = {
// 	"filters": [

// 	]
// };
frappe.query_reports["Sales Invoice Report"] = {
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
            "fieldname": "customer_name",
            "label": __("Party"),
            "fieldtype": "MultiSelectList",
            "get_data": function(txt) {
                return frappe.db.get_link_options("Customer", txt);
            }
        },
        {
            "fieldname": "customer_group",
            "label": __("Party Group"),
            "fieldtype": "MultiSelectList",
            "get_data": function(txt) {
                return frappe.db.get_link_options("Customer Group", txt);
            }
        },
                {
            fieldname: "item_group",
            label: "Item Group",
            fieldtype: "MultiSelectList",
            get_data: function (txt) {
                return frappe.db.get_link_options("Item Group", txt);
            }
        },
               {
            fieldname: "item_category",
            label: "Item Category",
            fieldtype: "MultiSelectList",
            get_data: function (txt) {
                return frappe.db.get_link_options("Item Category", txt);
            }
        },
        {
            fieldname: "sub_lob",
            label: "Sub LOB",
            fieldtype: "MultiSelectList",
            get_data: function (txt) {
                return frappe.db.get_link_options("Item Sub Lob", txt);
            }
        },
        {
            "fieldname": "set_warehouse",
            "label": __("Item Godown"),
            "fieldtype": "MultiSelectList",
            "get_data": function(txt) {
                return frappe.db.get_link_options("Warehouse", txt);
            }
        }
        // {
        //     "fieldname": "customer_name",
        //     "label": __("Party"),
        //     "fieldtype": "Link",
        //     "options": "Customer"
        // },
        // {
        //     "fieldname": "customer_group",
        //     "label": __("Party Group"),
        //     "fieldtype": "Link",
        //     "options": "Customer Group"
        // },
        // {
        //     "fieldname": "set_warehouse",
        //     "label": __("Item Godown"),
        //     "fieldtype": "Link",
        //     "options": "Warehouse"
        // }
    ],

    "formatter": function(value, row, column, data, default_formatter) {
        return default_formatter(value, row, column, data);
    }
};