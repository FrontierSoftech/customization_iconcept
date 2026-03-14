__version__ = "0.0.1"

def _apply_override():
    try:
        import erpnext.stock.report.stock_balance.stock_balance as sb
        from customization_iconcept.customize_stock_balance import StockBalanceFilter
        from customization_iconcept.customize_stock_balance import apply_items_filters
        
        sb.StockBalanceFilter = StockBalanceFilter
        sb.StockBalanceReport.apply_items_filters = apply_items_filters
    except Exception:
        # Happens during bench get-app / pip install
        pass


_apply_override()