import streamlit as st

st.set_page_config(
    page_title="Olist Customer Intelligence",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Olist Customer Intelligence Dashboard")
st.markdown("---")

st.markdown("""
### Full-Day Challenge: *Can NLP + Clustering improve the e-commerce experience?*
This dashboard presents the findings from our team analysis of the **Olist Brazilian E-Commerce dataset** (99,000+ orders, 2016–2018).
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Sentiment vs Ratings")
    st.markdown("**Gonçalo**")
    st.info(
        "22% of reviews contradict their own star score. "
        "10.8% of 5-star reviews contain negative language. "
        "3-star is the most misleading score with a 78% mismatch rate."
    )
    st.markdown("*Ratings do not always tell the full story.*")

with col2:
    st.markdown("### 😤 Emotion Analysis")
    st.markdown("**Rachel**")
    st.info(
        "Emotion analysis reveals what customers actually feel. "
        "Angry reviews cluster around late deliveries. "
        "Joy links to specific product categories."
    )
    st.markdown("*Emotion shows what customers are frustrated or happy about.*")

with col3:
    st.markdown("### 👥 Customer Segmentation")
    st.markdown("**Sarah**")
    st.info(
        "Only 3% of customers are Loyal Champions — but they drive disproportionate value. "
        "28,868 Lost High Spenders spent R$320 on average and never came back."
    )
    st.markdown("*Clustering tells us which customer groups to prioritize.*")

st.markdown("---")
st.markdown("### 🔗 The Full Story")
st.success(
    "Customers may appear satisfied based on star ratings alone — "
    "but emotion analysis reveals hidden frustration, "
    "and clustering tells us exactly which customers are most critical to retain."
)

st.markdown("---")
st.markdown("### Dataset Overview")
st.markdown("""
| Dataset | Rows | Used for |
|---|---|---|
| olist_order_reviews | 99,224 | Sentiment + Emotion analysis |
| olist_orders | 99,441 | RFM recency + frequency |
| olist_customers | 99,441 | Customer unique IDs |
| olist_order_payments | 103,886 | RFM monetary value |
""")
