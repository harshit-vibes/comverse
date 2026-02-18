from __future__ import annotations
from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class OrderStatus(str, Enum):
    pending          = "pending"
    confirmed        = "confirmed"
    preparing        = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered        = "delivered"
    cancelled        = "cancelled"


class PaymentStatus(str, Enum):
    unpaid    = "unpaid"
    link_sent = "link_sent"
    paid      = "paid"
    refunded  = "refunded"


class OrderItem(BaseModel):
    catalog_item_id: str    # FK → CatalogItem.id
    name: str               # denormalized for receipts / display
    quantity: int
    unit_price_inr: int
    total_price_inr: int    # = quantity * unit_price_inr


class Order(BaseModel):
    id: str                             # "ord_20260218_merchant001_001"
    merchant_id: str
    customer_phone: str
    session_id: str                     # "{merchant_id}:{customer_phone}"
    items: list[OrderItem]
    subtotal_inr: int
    status: OrderStatus                 = OrderStatus.pending
    payment_status: PaymentStatus       = PaymentStatus.unpaid
    payment_link: str | None            = None   # Razorpay link
    delivery_address: str | None        = None
    notes: str | None                   = None
    created_at: datetime
    updated_at: datetime
