// Copyright (c) 2026, Frontier Softech and contributors
// For license information, please see license.txt

// frappe.query_reports["Serial Ageing Report"] = {
// 	"filters": [

// 	]
// };
frappe.query_reports["Serial Ageing Report"] = {
    filters: [
		{
            "fieldname":"company",
            "label":"Company",
            "fieldtype":"Link",
            "options":"Company"
        },
        {
            fieldname: "warehouse",
            label: "Warehouse",
            fieldtype: "MultiSelectList",
            options: "Warehouse",
            get_data: function(txt) {
                return frappe.db.get_link_options("Warehouse", txt);
            }
        },
        {
            fieldname: "item_code",
            label: "Item Code",
            fieldtype: "MultiSelectList",
            options: "Item",
            get_data: function(txt) {
                return frappe.db.get_link_options("Item", txt);
            }
        }
    ]
};