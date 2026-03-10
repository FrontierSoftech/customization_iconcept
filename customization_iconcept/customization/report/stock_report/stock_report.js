// Copyright (c) 2026, Frontier Softech and contributors
// For license information, please see license.txt

// frappe.query_reports["Stock Report"] = {
// 	"filters": [

// 	]
// };
frappe.query_reports["Stock Report"] = {
    "filters": [

        {
            "fieldname": "company",
            "label": "Company Name",
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1,
            "default": frappe.defaults.get_user_default("Company")
        },

        {
            "fieldname": "warehouse",
            "label": "Godown",
            "fieldtype": "Link",
            "options": "Warehouse"
        },

        {
            "fieldname": "item_group",
            "label": "Item Group",
            "fieldtype": "Link",
            "options": "Item Group"
        },

        {
            "fieldname": "item_code",
            "label": "Item Name",
            "fieldtype": "Link",
            "options": "Item"
        },

        {
            "fieldname": "item_category",
            "label": "Item Category",
            "fieldtype": "Data"
        },

        {
            "fieldname": "sub_lob",
            "label": "Sub LOB",
            "fieldtype": "Data"
        },

        {
            "fieldname": "stock_status",
            "label": "Stock Status",
            "fieldtype": "Select",
            "options": "\nActual Qty\nPending Qty"
        }

    ]
};