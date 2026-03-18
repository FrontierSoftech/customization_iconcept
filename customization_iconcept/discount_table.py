import frappe

def before_save(doc, method):
    total_net_amount = 0
    total_discount = 0

    # 1. Calculate total net amount from items
    for item in doc.items:
        total_net_amount += item.net_amount or 0

    # 2. Calculate total discount from custom discount table
    for d in doc.custom_discount_ledger:  # change fieldname
        total_discount += d.discount or 0

    # Avoid division by zero
    if total_net_amount == 0:
        return

    if total_discount == 0:
        return
    # 3. Distribute discount proportionally
    for item in doc.items:
        item_net = item.net_amount or 0

        item_discount = (item_net / total_net_amount) * total_discount

        # store in a custom field in item table
        item.discount_amount = item_discount