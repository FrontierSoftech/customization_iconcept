# __version__ = "0.0.1"

# def _apply_override():
#     try:
#         import erpnext.stock.report.stock_balance.stock_balance as sb
#         from customization_iconcept.customize_stock_balance import StockBalanceFilter
#         from customization_iconcept.customize_stock_balance import apply_items_filters
#         import erpnext.stock.report.stock_ageing.stock_ageing as sa
#         from customization_iconcept.customize_stock_ageings import (
#             patched_execute,
#             patched_format_report_data,
#             patched_get_chart_data,
#             get_columns,
#             FIFOSlotss
#         )
        
#         sb.StockBalanceFilter = StockBalanceFilter
#         sb.StockBalanceReport.apply_items_filters = apply_items_filters
#         sa.execute = patched_execute
#         sa.format_report_data = patched_format_report_data
#         sa.get_chart_data = patched_get_chart_data
#         sa.get_columns = get_columns
#         sa.FIFOSlots = FIFOSlotss
        
#     except Exception:
#         # Happens during bench get-app / pip install
#         pass


# _apply_override()