from __future__ import annotations
from pydantic import BaseModel


class OperatingHours(BaseModel):
    open_time: str              # "11:00"
    close_time: str             # "15:00"
    order_cutoff: str | None    # "18:00" — last order for same-day; None = no cutoff
    days: list[str]             # ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]


class CatalogItem(BaseModel):
    id: str                     # "cake_choc_001"
    retailer_id: str            # WhatsApp product_retailer_id (= id for now)
    name: str                   # "Chocolate Cake"
    description: str            # short description for WhatsApp product card
    price_inr: int              # whole rupees, no decimals
    image_url: str | None       # product image URL; None for mock
    category: str               # "cake" | "thali" | "drink" etc.
    is_available: bool          # False = out of stock / off-menu


class Merchant(BaseModel):
    id: str                     # "merchant_001"
    catalog_id: str             # WhatsApp catalog ID (mock value for now)
    name: str                   # "Amit's Cake Shop"
    emoji: str                  # "🎂" — display only
    phone: str                  # "+911234567890" WhatsApp business number
    delivery_area: str          # "Pune"
    min_order_inr: int          # 300
    commission_pct: float       # 10.0
    operating_hours: OperatingHours
    catalog: list[CatalogItem]

    @property
    def catalog_summary(self) -> str:
        """Auto-generated AI context string — always in sync with catalog."""
        available = [i for i in self.catalog if i.is_available]
        items_str = ", ".join(f"{i.name} (₹{i.price_inr})" for i in available)
        return (
            f"{self.name}. Items: {items_str}. "
            f"Min order ₹{self.min_order_inr}. Delivery: {self.delivery_area}. "
            f"Hours: {self.operating_hours.open_time}–{self.operating_hours.close_time}."
        )
