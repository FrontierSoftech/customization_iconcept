frappe.ui.form.on('Purchase Receipt', {
    validate: function(frm) {
        // Loop through all the items in the Purchase Receipt Item child table
        $.each(frm.doc.items || [], function(i, item) {
            // If the item has a linked purchase_order
            if (item.purchase_order) {
                // Fetch the Purchase Order data using frappe.call
                frappe.call({
                    method: 'frappe.client.get',
                    args: {
                        doctype: 'Purchase Order',
                        name: item.purchase_order
                    },
                    callback: function(response) {
                        if (response.message) {
                            // Get the items from the Purchase Order document
                            let po_doc = response.message;
                            
                            // Find the corresponding Purchase Order Item by matching item_code
                            let po_item = po_doc.items.find(po_item => po_item.item_code === item.item_code);
                            
                            if (po_item) {
                                // Check if the quantity in the Purchase Receipt Item matches the quantity in the Purchase Order Item
                                if (item.qty !== po_item.qty) {
                                    frappe.msgprint(__('The quantity in Purchase Receipt Item does not match the quantity in the Purchase Order for item: {0}. {1} (Purchase Order) vs {2} (Purchase Receipt)', 
                                        [item.item_code, po_item.qty, item.qty]));
                                    frappe.validated = false;
                                    return false;  // Exit the loop
                                }
                            } else {
                                frappe.msgprint(__('No corresponding Purchase Order item found for item: {0}', [item.item_code]));
                                frappe.validated = false;
                                return false;  // Exit the loop
                            }
                        }
                    }
                });
            }
        });
    }
});
