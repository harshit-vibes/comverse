from models.merchant import Merchant
from mocks.merchants import get_merchant


def test_get_known_merchant():
    merchant = get_merchant("merchant_001")
    assert isinstance(merchant, Merchant)
    assert merchant.name == "Amit's Cake Shop"
    assert merchant.catalog_summary is not None


def test_get_another_known_merchant():
    merchant = get_merchant("merchant_002")
    assert merchant.name == "Priya's Thali House"


def test_unknown_merchant_returns_none():
    assert get_merchant("unknown_merchant") is None
