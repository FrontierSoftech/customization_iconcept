// Copyright (c) 2026, Frontier Softech and contributors
// For license information, please see license.txt

// frappe.query_reports["Goods In Transit Report"] = {
// 	"filters": [

// 	]
// };
frappe.query_reports["Goods In Transit Report"] = {
    filters: [

        {
            fieldname: "company",
            label: "Company",
            fieldtype: "MultiSelectList",
            options: "Company",
            get_data: txt => frappe.db.get_link_options("Company", txt)
        },
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            default: frappe.datetime.month_start()
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            default: frappe.datetime.get_today()
        },
        {
            fieldname: "custom_branch_warehouse",
            label: "Branch Warehouse",
            fieldtype: "MultiSelectList",
            options: "Warehouse",
            get_data: txt => frappe.db.get_link_options("Warehouse", txt)
        },
        {
            fieldname: "item_code",
            label: "Item Code",
            fieldtype: "MultiSelectList",
            options: "Item",
            get_data: txt => frappe.db.get_link_options("Item", txt)
        },

        {
            fieldname: "item_group",
            label: "Item Group",
            fieldtype: "MultiSelectList",
            options: "Item Group",
            get_data: txt => frappe.db.get_link_options("Item Group", txt)
        },

        {
            fieldname: "custom_item_category",
            label: "Item Category",
            fieldtype: "MultiSelectList",
            options: "Item Category",
            get_data: txt => frappe.db.get_link_options("Item Category", txt)
        },

        {
            fieldname: "custom_item_sub_lob",
            label: "Sub LOB",
            fieldtype: "MultiSelectList",
            options: "Item Sub Lob",
            get_data: txt => frappe.db.get_link_options("Item Sub Lob", txt)
        },

        // {
        //     fieldname: "voucher_type",
        //     label: "Voucher Type",
        //     fieldtype: "MultiSelectList",
        //     get_data: function(txt) {
        //         return [
        //             { value: "Stock Entry", description: "Stock Entry" },
        //             { value: "Sales Invoice", description: "Sales Invoice" },
        //             { value: "Purchase Receipt", description: "Purchase Receipt" },
        //             { value: "Delivery Note", description: "Delivery Note" }
        //         ];
        //     }
        // },

        // {
        //     fieldname: "voucher_no",
        //     label: "Voucher No",
        //     fieldtype: "MultiSelectList",
        //     get_data: function(txt) {
        //         return frappe.db.get_list("Stock Ledger Entry", {
        //             fields: ["voucher_no"],
        //             filters: {
        //                 voucher_no: ["like", `%${txt}%`]
        //             },
        //             distinct: true,
        //             limit: 20
        //         }).then(r => {
        //             return r.map(d => ({
        //                 value: d.voucher_no,
        //                 description: d.voucher_no
        //             }));
        //         });
        //     }
        // }
    ]
};