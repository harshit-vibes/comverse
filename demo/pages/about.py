import streamlit as st

st.set_page_config(
    page_title="About — Comverse",
    page_icon="💬",
    layout="wide",
)

st.title("About Comverse")
st.caption("WhatsApp Commerce for Indian SMBs")

st.divider()

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("What is Comverse?")
    st.write(
        "Comverse lets Indian food businesses (cake shops, thali restaurants, cafes) "
        "accept orders directly on WhatsApp — at **10% commission** vs 25–35% on Zomato/Swiggy."
    )
    st.write("No app for customers. **WhatsApp IS the ordering interface.**")

    st.write("")
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
    st.markdown("Request body:")
    st.code(
        '{\n  "merchant_id": "string",\n  "sender": "string",\n  "message": "string"\n}',
        language="json",
    )
    st.markdown("Response:")
    st.code(
        '{\n  "session_id": "string",\n  "reply": "string"\n}',
        language="json",
    )
