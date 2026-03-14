__version__ = "0.0.1"

def _apply_override():
    try:
        import erpnext.stock.report.stock_balance.stock_balance as sb
        from customization_iconcept.customize_stock_balance import StockBalanceFilter
        from customization_iconcept.customize_stock_balance import apply_items_filters
        from erpnext.stock.report.stock_ageing import stock_ageing as original_report
        from customization_iconcept.customize_stock_ageings import patched_execute
        from customization_iconcept.customize_stock_ageings import __get_item_query
        from customization_iconcept.customize_stock_ageings import __get_stock_ledger_entries
        from customization_iconcept.customize_stock_ageings import __get_warehouse_conditions
        from customization_iconcept.customize_stock_ageings import __get_bundle_wise_serial_nos
        
        sb.StockBalanceFilter = StockBalanceFilter
        sb.StockBalanceReport.apply_items_filters = apply_items_filters
        original_report.execute = patched_execute
        original_report.FIFOSlots.__get_item_query = __get_item_query
        original_report.FIFOSlots.__get_stock_ledger_entries = __get_stock_ledger_entries
        original_report.FIFOSlots.__get_warehouse_conditions = __get_warehouse_conditions
        original_report.FIFOSlots.__get_bundle_wise_serial_nos = __get_bundle_wise_serial_nos
    except Exception:
        # Happens during bench get-app / pip install
        pass


_apply_override()