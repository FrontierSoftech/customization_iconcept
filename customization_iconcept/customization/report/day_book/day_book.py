import frappe
from frappe.utils import format_datetime


def execute(filters=None):
    if filters is None:
        filters = {}

    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Time", "fieldname": "time", "fieldtype": "Data", "width": 90},
        {"label": "Voucher Type", "fieldname": "voucher_type", "fieldtype": "Data", "width": 150},
        {"label": "Voucher No", "fieldname": "voucher_no", "fieldtype": "Data", "width": 180},
        {"label": "Sub Entry Type", "fieldname": "sub_entry_type", "fieldtype": "Data", "width": 150},
        {"label": "Party / Title", "fieldname": "title", "fieldtype": "Data", "width": 200},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]

    data = get_day_book_data(
        from_date=filters.get("from_date"),
        to_date=filters.get("to_date"),
        voucher_type_filter=filters.get("voucher_type"),
        party_filter=filters.get("party"),
        cost_center_filter=filters.get("cost_center"),
        branch_filter=filters.get("branch"),
        status_filter=filters.get("status"),
        hide_cancelled=filters.get("hide_cancelled")
    )

    return columns, data


def get_day_book_data(
    from_date,
    to_date,
    voucher_type_filter=None,
    party_filter=None,
    cost_center_filter=None,
    branch_filter=None,
    status_filter=None,
    hide_cancelled=0
):

    all_entries = []

    status_map = {
        0: "Draft",
        1: "Submitted",
        2: "Cancelled"
    }

    def collect_entries(
        doctype,
        date_field=None,
        party_field=None,
        amount_field=None,
        cost_center_field=None,
        branch_field=None
    ):
        meta = frappe.get_meta(doctype)

        # Auto detect date field
        if not date_field:
            for df in ["posting_date", "transaction_date"]:
                if meta.has_field(df):
                    date_field = df
                    break

        if not date_field or not meta.has_field(date_field):
            return

        fields = ["name", "creation", date_field, "docstatus"]

        if party_field and meta.has_field(party_field):
            fields.append(party_field)

        if amount_field and meta.has_field(amount_field):
            fields.append(amount_field)

        if cost_center_field and meta.has_field(cost_center_field):
            fields.append(cost_center_field)

        if branch_field and meta.has_field(branch_field):
            fields.append(branch_field)

        if doctype == "Payment Entry" and meta.has_field("payment_type"):
            fields.append("payment_type")

        if doctype == "Journal Entry" and meta.has_field("voucher_type"):
            fields.append("voucher_type")

        filters_dict = {
            date_field: ["between", [from_date, to_date]]
        }

        records = frappe.get_all(
            doctype,
            filters=filters_dict,
            fields=fields,
            order_by="creation asc"
        )

        for doc in records:

            # Voucher Type filter
            if voucher_type_filter and doctype != voucher_type_filter:
                continue

            # Party filter
            if party_filter and party_field and doc.get(party_field) != party_filter:
                continue

            # Cost center filter
            if cost_center_filter and cost_center_field and doc.get(cost_center_field) != cost_center_filter:
                continue

            # Branch filter
            if branch_filter and branch_field and doc.get(branch_field) != branch_filter:
                continue

            doc_status = status_map.get(doc.docstatus, "")

            # Status filter
            if status_filter and doc_status != status_filter:
                continue

            # Hide cancelled
            if hide_cancelled and doc.docstatus == 2:
                continue

            sub_entry_type = ""

            if doctype == "Payment Entry":
                sub_entry_type = doc.get("payment_type") or ""

            elif doctype == "Journal Entry":
                sub_entry_type = doc.get("voucher_type") or ""

            title = ""

            if party_field and meta.has_field(party_field):
                title = doc.get(party_field)

            if not title:
                title = doc.get("title", "")

            amount = 0
            if amount_field and meta.has_field(amount_field):
                amount = doc.get(amount_field)

            all_entries.append({
                "date": doc.get(date_field),
                "time": format_datetime(doc.creation, "HH:mm:ss"),
                "creation": doc.creation,
                "voucher_type": doctype,
                "voucher_no": doc.name,
                "sub_entry_type": sub_entry_type,
                "title": title,
                "amount": amount,
                "status": doc_status
            })

    # Collect data from multiple doctypes

    collect_entries("Sales Invoice", "posting_date", "customer", "grand_total", "cost_center", "branch")

    collect_entries("Purchase Invoice", "posting_date", "supplier", "grand_total", "cost_center", "branch")

    collect_entries("Sales Order", "transaction_date", "customer", "grand_total", "cost_center", "branch")

    collect_entries("Purchase Order", "transaction_date", "supplier", "grand_total", "cost_center", "branch")

    collect_entries("Payment Entry", "posting_date", "party", "paid_amount", "cost_center", "branch")

    collect_entries("Journal Entry", "posting_date", "title", "total_debit", "cost_center", "branch")

    collect_entries("Purchase Receipt", "posting_date", "supplier", "grand_total", "cost_center", "branch")

    collect_entries("Delivery Note", "posting_date", "customer", "grand_total", "cost_center", "branch")

    collect_entries("Stock Entry", "posting_date", None, "total_outgoing_value", "cost_center", "branch")

    collect_entries("Stock Reconciliation")

    collect_entries("Material Request", "transaction_date", "requested_by", None, "cost_center", "branch")

    # Final chronological sorting
    all_entries.sort(key=lambda x: (x["date"], x["creation"]))

    return all_entries

    # import frappe
# from frappe.utils import today, format_datetime

# def execute(filters=None):
#     if filters is None:
#         filters = {}

#     columns = [
#         {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
#         # {"label": "Time", "fieldname": "time", "fieldtype": "Data", "width": 90},
#         {"label": "Voucher Type", "fieldname": "voucher_type", "fieldtype": "Data", "width": 150},
#         {"label": "Voucher No", "fieldname": "voucher_no", "fieldtype": "Data", "width": 180},
#         {"label": "Sub Entry Type", "fieldname": "sub_entry_type", "fieldtype": "Data", "width": 150},
#         {"label": "Party / Title", "fieldname": "title", "fieldtype": "Data", "width": 200},
#         {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
#         {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
#     ]

#     data = get_day_book_data(
#         from_date=filters.get("from_date"),
#         to_date=filters.get("to_date"),
#         voucher_type_filter=filters.get("voucher_type"),
#         party_filter=filters.get("party"),
#         cost_center_filter=filters.get("cost_center"),
#         branch_filter=filters.get("branch"),
#         status_filter=filters.get("status"),
#         hide_cancelled=filters.get("hide_cancelled")
#     )

#     return columns, data


# def get_day_book_data(from_date, to_date, voucher_type_filter=None, party_filter=None, 
#                       cost_center_filter=None, branch_filter=None, status_filter=None, hide_cancelled=0):

#     all_entries = []
#     status_map = {0: "Draft", 1: "Submitted", 2: "Cancelled"}

#     def collect_entries(doctype, date_field=None, party_field=None, amount_field=None, cost_center_field=None, branch_field=None):
#         meta = frappe.get_meta(doctype)

#         # Auto-detect date field if not provided
#         if not date_field:
#             for df in ["posting_date", "transaction_date"]:
#                 if meta.has_field(df):
#                     date_field = df
#                     break
#         if not date_field or not meta.has_field(date_field):
#             return

#         fields = ["name", "creation", date_field, "docstatus"]
#         if party_field and meta.has_field(party_field):
#             fields.append(party_field)
#         if amount_field and meta.has_field(amount_field):
#             fields.append(amount_field)
#         if cost_center_field and meta.has_field(cost_center_field):
#             fields.append(cost_center_field)
#         if branch_field and meta.has_field(branch_field):
#             fields.append(branch_field)

#         if doctype == "Payment Entry" and meta.has_field("payment_type"):
#             fields.append("payment_type")
#         if doctype == "Journal Entry" and meta.has_field("voucher_type"):
#             fields.append("voucher_type")

#         # Date range filter
#         filters_dict = {date_field: ["between", [from_date, to_date]]}
#         records = frappe.get_all(doctype, filters=filters_dict, fields=fields, order_by="creation asc")

#         for doc in records:
#             # Filter by voucher type
#             if voucher_type_filter and doctype != voucher_type_filter:
#                 continue
#             # Filter by party
#             if party_filter and party_field and doc.get(party_field) != party_filter:
#                 continue
#             # Filter by cost center
#             if cost_center_filter and cost_center_field and doc.get(cost_center_field) != cost_center_filter:
#                 continue
#             # Filter by branch
#             if branch_filter and branch_field and doc.get(branch_field) != branch_filter:
#                 continue

#             # Map status
#             doc_status = status_map.get(doc.docstatus, "")

#             # Filter by status
#             if status_filter and doc_status != status_filter:
#                 continue
#             # Hide cancelled if checkbox checked
#             if hide_cancelled and doc.docstatus == 2:
#                 continue

#             sub_entry_type = ""
#             if doctype == "Payment Entry":
#                 sub_entry_type = doc.get("payment_type") or ""
#             elif doctype == "Journal Entry":
#                 sub_entry_type = doc.get("voucher_type") or ""

#             all_entries.append({
#                 "date": doc.get(date_field),
#                 "time": format_datetime(doc.creation, "HH:mm:ss"),
#                 "voucher_type": doctype,
#                 "voucher_no": doc.name,
#                 "title": doc.get(party_field) if party_field and meta.has_field(party_field) else "" or doc.get("title"),
#                 "amount": doc.get(amount_field) if amount_field and meta.has_field(amount_field) else 0,
#                 "status": doc_status,
#                 "sub_entry_type": sub_entry_type
#             })

#     # ==============================
#     # COLLECT DATA FROM DOCTYPES
#     # ==============================
#     collect_entries("Sales Invoice", "posting_date", "customer", "grand_total", "cost_center", "branch")
#     collect_entries("Purchase Invoice", "posting_date", "supplier", "grand_total", "cost_center", "branch")
#     collect_entries("Sales Order", "transaction_date", "customer", "grand_total", "cost_center", "branch")
#     collect_entries("Purchase Order", "transaction_date", "supplier", "grand_total", "cost_center", "branch")
#     collect_entries("Payment Entry", "posting_date", "party", "paid_amount", "cost_center", "branch")
#     collect_entries("Journal Entry", "posting_date", "title", "total_debit", "cost_center", "branch")
#     collect_entries("Purchase Receipt", "posting_date", "supplier", "grand_total", "cost_center", "branch")
#     collect_entries("Delivery Note", "posting_date", "customer", "grand_total", "cost_center", "branch")
#     collect_entries("Stock Entry", "posting_date", None, "total_outgoing_value", "cost_center", "branch")
#     collect_entries("Stock Reconciliation")
#     collect_entries("Material Request", "transaction_date", "requested_by", None, "cost_center", "branch")

#     # Sort by time
#     all_entries.sort(key=lambda x: x["time"])
#     return all_entries