// Copyright (c) 2026, Frontier Softech and contributors
// For license information, please see license.txt

// frappe.query_reports["Customize Stock Ageing"] = {
// 	"filters": [

// 	]
// };
frappe.query_reports["Customize Stock Ageing"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("As On Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "warehouse_type",
			label: __("Warehouse Type"),
			fieldtype: "Link",
			options: "Warehouse Type",
		},

		// MULTI WAREHOUSE
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options("Warehouse", txt, {
					company: frappe.query_report.get_filter_value("company"),
				});
			},
		},

		// MULTI ITEM
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options("Item", txt);
			},
		},

		// MULTI BRAND
		{
			fieldname: "brand",
			label: __("Brand"),
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options("Brand", txt);
			},
		},

		// MULTI ITEM GROUP
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options("Item Group", txt);
			},
		},

		// MULTI ITEM CATEGORY
		{
			fieldname: "item_category",
			label: __("Item Category"),
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options("Item Category", txt);
			},
		},

		// MULTI ITEM SUB LOB
		{
			fieldname: "item_sub_lob",
			label: __("Item Sub Lob"),
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options("Item Sub Lob", txt);
			},
		},

		{
			fieldname: "range",
			label: __("Ageing Range"),
			fieldtype: "Data",
			default: "30, 60, 90",
		},
		{
			fieldname: "show_warehouse_wise_stock",
			label: __("Show Warehouse-wise Stock"),
			fieldtype: "Check",
			default: 0,
		},
	],
};