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


# ── API key dialog gate ────────────────────────────────────────────────────────
@st.dialog("Welcome to Comverse 💬")
def api_key_dialog():
    st.write(
        "Enter your **Lyzr API key** and **Agent ID** to start the demo. "
        "Find both at [studio.lyzr.ai](https://studio.lyzr.ai)."
    )
    st.write("")
    key = st.text_input("Lyzr API Key", type="password", placeholder="lyzr-...")
    agent_id = st.text_input(
        "Agent ID",
        placeholder="agent_...",
        help="The ID of your Comverse agent in Lyzr Studio",
    )
    st.write("")
    if st.button("Continue →", use_container_width=True, type="primary"):
        if not key:
            st.error("Please enter your Lyzr API key.")
        elif not agent_id:
            st.error("Please enter your Agent ID.")
        else:
            with st.spinner("Validating..."):
                try:
                    resp = requests.get(
                        f"{API_BASE}/validate",
                        headers={
                            "X-Lyzr-Api-Key": key,
                            "X-Lyzr-Agent-Id": agent_id,
                        },
                        timeout=8,
                    )
                    if resp.status_code == 200:
                        st.session_state.lyzr_api_key = key
                        st.session_state.lyzr_agent_id = agent_id
                        st.rerun()
                    else:
                        st.error(resp.json().get("detail", "Invalid credentials."))
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Cannot reach the Comverse service at localhost:8000. "
                        "Make sure it's running (`make dev` in `service/`)."
                    )
                except requests.exceptions.ReadTimeout:
                    st.error("Lyzr API did not respond. Check your credentials and try again.")


if not st.session_state.get("lyzr_api_key"):
    api_key_dialog()
    st.stop()


# ── Main app ───────────────────────────────────────────────────────────────────
st.title("💬 Comverse Demo")

tab_chat, tab_about, tab_settings = st.tabs(["Chat", "About", "Settings"])

# ── Chat tab ──────────────────────────────────────────────────────────────────
with tab_chat:
    # Merchant selector
    merchant_labels = {k: f"{v['emoji']} {v['name']}" for k, v in MERCHANTS.items()}
    col_sel, col_info = st.columns([2, 3])
    with col_sel:
        selected_id = st.selectbox(
            "Merchant",
            options=list(merchant_labels.keys()),
            format_func=lambda k: merchant_labels[k],
        )
    merchant = MERCHANTS[selected_id]

    # Reset chat when merchant changes
    if st.session_state.get("active_merchant") != selected_id:
        st.session_state.active_merchant = selected_id
        st.session_state.messages = []

    hours = merchant["operating_hours"]
    with col_info:
        st.write("")
        st.caption(
            f"📍 {merchant['delivery_area']}  ·  "
            f"🕐 {hours['open_time']}–{hours['close_time']}  ·  "
            f"Min order ₹{merchant['min_order_inr']}"
        )

    with st.expander(f"{merchant['emoji']} Catalog", expanded=False):
        for item in merchant["catalog"]:
            col_item, col_price = st.columns([3, 1])
            col_item.write(item["name"])
            col_item.caption(item["description"])
            badge = "✅" if item["is_available"] else "❌"
            col_price.write(f"**₹{item['price_inr']}** {badge}")

    st.caption(
        f"Simulating customer **{DEMO_SENDER}** ordering on WhatsApp. "
        "Powered by Lyzr + Claude Sonnet."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container(height=440, border=True)
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
        # Show user message immediately inside the container
        with chat_container:
            with st.chat_message("user"):
                st.write(user_input)
            # Show loader while waiting for the response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
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
                            timeout=120,
                        )
                        resp.raise_for_status()
                        data = resp.json()
                        assistant_msg = {
                            "role": "assistant",
                            "content": data["reply"],
                            "raw_response": data,
                        }
                    except requests.exceptions.ConnectionError:
                        assistant_msg = {
                            "role": "assistant",
                            "content": (
                                "⚠️ Cannot reach the Comverse service. "
                                "Start it with `make dev` in `comverse/service/`."
                            ),
                        }
                    except Exception as e:
                        assistant_msg = {
                            "role": "assistant",
                            "content": f"⚠️ Error: {e}",
                        }

        # Persist both messages and rerender cleanly
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append(assistant_msg)
        st.rerun()

    if st.session_state.messages:
        if st.button("🗑️ Clear chat", use_container_width=False):
            st.session_state.messages = []
            st.rerun()

# ── About tab ─────────────────────────────────────────────────────────────────
with tab_about:
    st.subheader("What is Comverse?")
    st.write(
        "Comverse lets Indian food businesses (cake shops, thali restaurants, cafes) "
        "accept orders directly on WhatsApp — at **10% commission** vs 25–35% on Zomato/Swiggy."
    )
    st.write("No app for customers. **WhatsApp IS the ordering interface.**")

    st.divider()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("How it works")
        st.code(
            "Customer (WhatsApp)\n"
            "     │  sends message\n"
            "     ▼\n"
            "WhatsApp Cloud API\n"
            "     │  webhook\n"
            "     ▼\n"
            "Comverse Middleware  ◄─── this demo\n"
            "     │  calls\n"
            "     ▼\n"
            "Lyzr Agent (Claude Sonnet)\n"
            "     │  returns reply\n"
            "     ▼\n"
            "Customer gets response",
            language=None,
        )

    with col2:
        st.subheader("Tech Stack")
        st.markdown(
            "| Layer | Technology |\n"
            "|-------|------------|\n"
            "| Channel | WhatsApp Cloud API |\n"
            "| AI Agent | Lyzr + Claude Sonnet 4.5 |\n"
            "| Middleware | FastAPI → AWS Lambda |\n"
            "| Database | Supabase Postgres |\n"
            "| Payments | Razorpay Route |\n"
            "| Frontend | Next.js + shadcn/ui |"
        )

        st.write("")
        st.subheader("API Reference")

        st.markdown("**`GET /health`**")
        st.code('{"status": "ok"}', language="json")

        st.markdown("**`POST /chat`**")
        st.markdown("Request:")
        st.code(
            '{\n  "merchant_id": "string",\n  "sender": "string",\n  "message": "string"\n}',
            language="json",
        )
        st.markdown("Response:")
        st.code(
            '{\n  "session_id": "string",\n  "reply": "string"\n}',
            language="json",
        )

# ── Settings tab ──────────────────────────────────────────────────────────────
with tab_settings:
    st.subheader("Lyzr Configuration")
    lyzr_api_key = st.text_input(
        "Lyzr API Key",
        value=st.session_state.get("lyzr_api_key", ""),
        type="password",
        placeholder="lyzr-...",
        help="Get your API key from Lyzr Studio",
    )
    lyzr_agent_id = st.text_input(
        "Agent ID",
        value=st.session_state.get("lyzr_agent_id", ""),
        placeholder="agent_...",
        help="The ID of your Comverse agent in Lyzr Studio",
    )
    if st.button("Save", use_container_width=False):
        st.session_state.lyzr_api_key = lyzr_api_key
        st.session_state.lyzr_agent_id = lyzr_agent_id
        st.session_state.messages = []
        st.success("Settings saved.")

    st.divider()
    if st.button("Sign out", type="secondary"):
        for key in ["lyzr_api_key", "lyzr_agent_id", "messages", "active_merchant"]:
            st.session_state.pop(key, None)
        st.rerun()
