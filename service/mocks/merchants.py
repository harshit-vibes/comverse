from models.merchant import CatalogItem, Merchant, OperatingHours

_merchants_list: list[Merchant] = [
    Merchant(
        id="merchant_001",
        catalog_id="cat_mock_001",
        name="Amit's Cake Shop",
        emoji="🎂",
        phone="+911234567890",
        delivery_area="Pune",
        min_order_inr=300,
        commission_pct=10.0,
        operating_hours=OperatingHours(
            open_time="09:00",
            close_time="21:00",
            order_cutoff="18:00",
            days=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        ),
        catalog=[
            CatalogItem(
                id="cake_choc_001",
                retailer_id="cake_choc_001",
                name="Chocolate Cake",
                description="Rich dark chocolate sponge with ganache frosting",
                price_inr=500,
                image_url=None,
                category="cake",
                is_available=True,
            ),
            CatalogItem(
                id="cake_van_001",
                retailer_id="cake_van_001",
                name="Vanilla Cake",
                description="Classic vanilla sponge with butter cream",
                price_inr=400,
                image_url=None,
                category="cake",
                is_available=True,
            ),
            CatalogItem(
                id="cake_rv_001",
                retailer_id="cake_rv_001",
                name="Red Velvet Cake",
                description="Velvety red sponge with cream cheese frosting",
                price_inr=600,
                image_url=None,
                category="cake",
                is_available=True,
            ),
        ],
    ),
    Merchant(
        id="merchant_002",
        catalog_id="cat_mock_002",
        name="Priya's Thali House",
        emoji="🍱",
        phone="+919876500001",
        delivery_area="Local delivery",
        min_order_inr=240,
        commission_pct=10.0,
        operating_hours=OperatingHours(
            open_time="11:00",
            close_time="15:00",
            order_cutoff=None,
            days=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        ),
        catalog=[
            CatalogItem(
                id="thali_veg_001",
                retailer_id="thali_veg_001",
                name="Veg Thali",
                description="Seasonal sabzi, dal, roti, rice, salad & pickle",
                price_inr=120,
                image_url=None,
                category="thali",
                is_available=True,
            ),
            CatalogItem(
                id="thali_nveg_001",
                retailer_id="thali_nveg_001",
                name="Non-veg Thali",
                description="Chicken curry, dal, roti, rice, salad & pickle",
                price_inr=150,
                image_url=None,
                category="thali",
                is_available=True,
            ),
        ],
    ),
]

# Public registry — keyed by merchant id
MERCHANTS: dict[str, Merchant] = {m.id: m for m in _merchants_list}


def get_merchant(merchant_id: str) -> Merchant | None:
    return MERCHANTS.get(merchant_id)
