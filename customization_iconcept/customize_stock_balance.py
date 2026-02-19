from typing import Any, TypedDict
import erpnext.stock.report.stock_balance.stock_balance as sb

class StockBalanceFilter(TypedDict):
	company: str | None
	from_date: str
	to_date: str
	item_group: list[str] | None
	item: list[str] | None
	warehouse: list[str] | None
	warehouse_type: str | None
	include_uom: str | None  # include extra info in converted UOM
	show_stock_ageing_data: bool
	show_variant_attributes: bool

def apply_items_filters(self, query, item_table) -> str:
    # ---- Item Group ----
    if item_groups := self.filters.get("item_group"):
        if isinstance(item_groups, (list, tuple)):
            all_groups = []
            for group in item_groups:
                children = sb.get_descendants_of("Item Group", group, ignore_permissions=True)
                all_groups.extend(children)
                all_groups.append(group)
            query = query.where(item_table.item_group.isin(list(set(all_groups))))
        else:
            children = sb.get_descendants_of("Item Group", item_groups, ignore_permissions=True)
            query = query.where(item_table.item_group.isin([*children, item_groups]))

    # ---- Item Code ----
    if item_codes := self.filters.get("item_code"):
        if isinstance(item_codes, (list, tuple)):
            query = query.where(item_table.name.isin(item_codes))
        else:
            query = query.where(item_table.name == item_codes)

    # ---- Brand ----
    if brand := self.filters.get("brand"):
        query = query.where(item_table.brand == brand)

    return query