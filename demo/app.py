import streamlit as st
import requests
import json

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Comverse Demo",
    page_icon="💬",
    layout="wide",
)

# ── Mock merchant data ────────────────────────────────────────────────────────
MERCHANTS = {
    "merchant_001": {
        "id": "merchant_001",
        "catalog_id": "cat_mock_001",
        "name": "Amit's Cake Shop",
        "emoji": "🎂",
        "phone": "+911234567890",
        "delivery_area": "Pune",
        "min_order_inr": 300,
        "commission_pct": 10.0,
        "operating_hours": {
            "open_time": "09:00",
            "close_time": "21:00",
            "order_cutoff": "18:00",
            "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "catalog": [
            {
                "id": "cake_choc_001",
                "retailer_id": "cake_choc_001",
                "name": "Chocolate Cake",
                "description": "Rich dark chocolate sponge with ganache frosting",
                "price_inr": 500,
                "image_url": None,
                "category": "cake",
                "is_available": True,
            },
            {
                "id": "cake_van_001",
                "retailer_id": "cake_van_001",
                "name": "Vanilla Cake",
                "description": "Classic vanilla sponge with butter cream",
                "price_inr": 400,
                "image_url": None,
                "category": "cake",
                "is_available": True,
            },
            {
                "id": "cake_rv_001",
                "retailer_id": "cake_rv_001",
                "name": "Red Velvet Cake",
                "description": "Velvety red sponge with cream cheese frosting",
                "price_inr": 600,
                "image_url": None,
                "category": "cake",
                "is_available": True,
            },
        ],
    },
    "merchant_002": {
        "id": "merchant_002",
        "catalog_id": "cat_mock_002",
        "name": "Priya's Thali House",
        "emoji": "🍱",
        "phone": "+919876500001",
        "delivery_area": "Local delivery",
        "min_order_inr": 240,
        "commission_pct": 10.0,
        "operating_hours": {
            "open_time": "11:00",
            "close_time": "15:00",
            "order_cutoff": None,
            "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        },
        "catalog": [
            {
                "id": "thali_veg_001",
                "retailer_id": "thali_veg_001",
                "name": "Veg Thali",
                "description": "Seasonal sabzi, dal, roti, rice, salad & pickle",
                "price_inr": 120,
                "image_url": None,
                "category": "thali",
                "is_available": True,
            },
            {
                "id": "thali_nveg_001",
                "retailer_id": "thali_nveg_001",
                "name": "Non-veg Thali",
                "description": "Chicken curry, dal, roti, rice, salad & pickle",
                "price_inr": 150,
                "image_url": None,
                "category": "thali",
                "is_available": True,
            },
        ],
    },
}

DEMO_SENDER = "+919876543210"
API_BASE = "http://localhost:8000"

# ── Sidebar — settings + merchant switcher + catalog ─────────────────────────
with st.sidebar:
    st.header("💬 Comverse")
    st.divider()

    # ── Settings ──────────────────────────────────────────────────────────────
    with st.expander("⚙️ Settings", expanded=not st.session_state.get("lyzr_api_key")):
        lyzr_api_key = st.text_input(
            "Lyzr API Key",
            value=st.session_state.get("lyzr_api_key", ""),
            type="password",
            placeholder="lyzr-...",
            help="Get your API key from Lyzr Studio",
        )
        lyzr_agent_id = st.text_input(
            "Agent ID (optional)",
            value=st.session_state.get("lyzr_agent_id", ""),
            placeholder="Leave empty to auto-create",
            help="Reuse an existing Lyzr agent ID, or leave blank to create one on first use",
        )
        if st.button("Save", use_container_width=True):
            st.session_state.lyzr_api_key = lyzr_api_key
            st.session_state.lyzr_agent_id = lyzr_agent_id
            st.session_state.messages = []  # reset chat on credential change
            st.rerun()

    if not st.session_state.get("lyzr_api_key"):
        st.warning("Paste your Lyzr API key in Settings to start chatting.")

    st.divider()

    st.subheader("Merchant")
    merchant_labels = {k: f"{v['emoji']} {v['name']}" for k, v in MERCHANTS.items()}
    selected_id = st.selectbox(
        "Select merchant",
        options=list(merchant_labels.keys()),
        format_func=lambda k: merchant_labels[k],
        label_visibility="collapsed",
    )
    merchant = MERCHANTS[selected_id]

    # Reset chat when merchant changes
    if st.session_state.get("active_merchant") != selected_id:
        st.session_state.active_merchant = selected_id
        st.session_state.messages = []

    st.divider()

    # Catalog
    hours = merchant["operating_hours"]
    st.subheader(f"{merchant['emoji']} Catalog")
    st.caption(f"📍 {merchant['delivery_area']}  ·  🕐 {hours['open_time']}–{hours['close_time']}")
    st.write("")

    for item in merchant["catalog"]:
        col_item, col_price = st.columns([3, 1])
        col_item.write(item["name"])
        col_item.caption(item["description"])
        badge = "✅" if item["is_available"] else "❌"
        col_price.write(f"**₹{item['price_inr']}** {badge}")

    st.write("")
    st.info(f"Min order: ₹{merchant['min_order_inr']}")

# ── Main area — chat ──────────────────────────────────────────────────────────
st.title(f"Chat — {merchant['emoji']} {merchant['name']}")
st.caption(
    f"Simulating customer **{DEMO_SENDER}** ordering on WhatsApp. "
    "Powered by Lyzr + Claude Sonnet."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_container = st.container(height=480, border=True)
with chat_container:
    if not st.session_state.messages:
        st.caption("_Start the conversation below..._")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
        if msg.get("raw_response"):
            with st.expander("Raw API response", expanded=False):
                st.code(json.dumps(msg["raw_response"], indent=2), language="json")

user_input = st.chat_input("Type a message as the customer...")

if user_input:
    if not st.session_state.get("lyzr_api_key"):
        st.error("Please enter your Lyzr API key in Settings before chatting.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})

    headers = {"X-Lyzr-Api-Key": st.session_state.lyzr_api_key}
    if st.session_state.get("lyzr_agent_id"):
        headers["X-Lyzr-Agent-Id"] = st.session_state.lyzr_agent_id

    try:
        resp = requests.post(
            f"{API_BASE}/chat",
            json={
                "merchant_id": selected_id,
                "sender": DEMO_SENDER,
                "message": user_input,
            },
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        st.session_state.messages.append({
            "role": "assistant",
            "content": data["reply"],
            "raw_response": data,
        })
    except requests.exceptions.ConnectionError:
        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "⚠️ Cannot reach the Comverse service. "
                "Start it with `make dev` in `comverse/service/`."
            ),
        })
    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"⚠️ Error: {e}",
        })

    st.rerun()

if st.session_state.messages:
    if st.button("🗑️ Clear chat", use_container_width=False):
        st.session_state.messages = []
        st.rerun()
