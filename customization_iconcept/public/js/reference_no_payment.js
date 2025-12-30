frappe.ui.form.on('Payment Entry', {
    
    'custom_get_references': function(frm) {
        fetch_outstanding_invoices(frm);
    },
        
    refresh: function(frm) {
        // Triggered when changes happen in the references child table (any field)
        frm.doc.references.forEach(function(row) {
            // Reset the custom_customer_name field before updating
            row.custom_customer_name = "";

            if (row.reference_name && row.reference_doctype) {
                let reference_doctype = row.reference_doctype;
                let reference_name = row.reference_name;

                // Make a frappe call to get the reference document details
                frappe.call({
                    method: 'frappe.client.get',
                    args: {
                        doctype: reference_doctype,  // Use dynamic reference doctype
                        name: reference_name         // reference_name should contain the document name
                    },
                    callback: function(response) {
                        if (response.message) {
                            // Handle different document types
                            if (reference_doctype === 'Journal Entry') {
                                // Populate custom_customer_name with cheque_no from Journal Entry
                                row.custom_reference_number = response.message.cheque_no;
                            } else  {
                                // Populate custom_customer_name with the customer from Sales Invoice
                                // row.custom_customer_name = response.message.customer;
                                row.custom_reference_number = '';
                            }

                            // Refresh the references field to display updated data
                            frm.refresh_field('references');
                        }
                    }
                });
            }
        });
    }
});

function fetch_outstanding_invoices(frm){
    frm.doc.references.forEach(function(row) {
            // Reset the custom_customer_name field before updating
            row.custom_customer_name = "";

            if (row.reference_name && row.reference_doctype) {
                let reference_doctype = row.reference_doctype;
                let reference_name = row.reference_name;

                // Make a frappe call to get the reference document details
                frappe.call({
                    method: 'frappe.client.get',
                    args: {
                        doctype: reference_doctype,  // Use dynamic reference doctype
                        name: reference_name         // reference_name should contain the document name
                    },
                    callback: function(response) {
                        if (response.message) {
                            // Handle different document types
                            if (reference_doctype === 'Journal Entry') {
                                // Populate custom_customer_name with cheque_no from Journal Entry
                                row.custom_reference_number = response.message.cheque_no;
                            } else  {
                                // Populate custom_customer_name with the customer from Sales Invoice
                                // row.custom_customer_name = response.message.customer;
                                row.custom_reference_number = '';
                            }

                            // Refresh the references field to display updated data
                            frm.refresh_field('references');
                        }
                    }
                });
            }
        });
}

