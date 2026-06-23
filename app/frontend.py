import os

import httpx
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


st.set_page_config(page_title="Shopify Support AI", page_icon="AI", layout="centered")

st.title("Shopify Support AI")

customer_id = st.text_input("Customer ID", value="cust_001")
order_id = st.text_input("Order ID", value="1234")
message = st.text_area(
    "Customer message",
    value="My order #1234 is delayed. Can I get a refund?",
    height=140,
)
show_debug = st.checkbox("Show agent debug details", value=False)

if st.button("Submit ticket", type="primary"):
    payload = {
        "customer_id": customer_id,
        "message": message,
        "order_id": order_id or None,
    }

    try:
        with httpx.Client(timeout=30) as client:
            response = client.post(f"{API_BASE_URL}/api/tickets", json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as exc:
        st.error(f"Backend request failed: {exc}")
    else:
        st.subheader("AI Response")
        st.write(data["response"])

        if show_debug:
            col1, col2, col3 = st.columns(3)
            col1.metric("Ticket", data["ticket_id"])
            col2.metric("Confidence", data["confidence"])
            col3.metric("Escalated", "Yes" if data["escalated"] else "No")

            if data.get("escalation_reason"):
                st.warning(data["escalation_reason"])

            with st.expander("Agent trace"):
                st.json(data["trace"])
