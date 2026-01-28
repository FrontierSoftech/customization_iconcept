import frappe

def set_apple_quarter_fields(doc, method=None):
    if not doc.posting_date:
        return

    aqd = frappe.db.get_value(
        "Apple Quarter",
        {"date": doc.posting_date},
        ["day", "month", "week", "quarter", "year"],
        as_dict=True
    )

    if aqd:
        doc.custom_day = aqd.day
        doc.custom_month = aqd.month
        doc.custom_week = aqd.week
        doc.custom_quarter = aqd.quarter
        doc.custom_year = aqd.year


# import frappe

# def set_apple_quarter_fields(doc, method=None):
#     if not doc.posting_date:
#         return

#     aqd = frappe.db.sql("""
#         SELECT day, month, week, quarter, year
#         FROM `tabApple Quarter`
#         WHERE %s BETWEEN from_date AND to_date
#         LIMIT 1
#     """, doc.posting_date, as_dict=True)

#     if aqd:
#         aqd = aqd[0]
#         doc.custom_day = aqd.day
#         doc.custom_month = aqd.month
#         doc.custom_week = aqd.week
#         doc.custom_quarter = aqd.quarter
#         doc.custom_year = aqd.year
