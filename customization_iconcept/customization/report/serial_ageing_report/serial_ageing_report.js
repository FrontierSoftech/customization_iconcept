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
            fieldname: "brand",
            label: "Brand",
            fieldtype: "MultiSelectList",
            get_data: function (txt) {
                return frappe.db.get_link_options("Brand", txt);
            }
        },
    ]
};