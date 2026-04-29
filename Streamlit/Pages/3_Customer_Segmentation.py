import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Customer Segmentation", page_icon="👥", layout="wide")

st.title("👥 Customer Segmentation — RFM Clustering")
st.markdown("Who are our customers and which ones matter most?")
st.markdown("---")

ROOT = Path(__file__).parent.parent.parent

@st.cache_data
def load_data():
    return pd.read_csv(ROOT / "data" / "processed" / "customer_segments.csv")

df = load_data()

colors_map = {
    "Loyal Champions": "gold",
    "Recent One-timers": "steelblue",
    "Lost High Spenders": "tomato",
    "Lost Bargain Hunters": "lightgray"
}

# --- Key metrics ---
total = len(df)
champions = df[df["segment"] == "Loyal Champions"]
lost_high = df[df["segment"] == "Lost High Spenders"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{total:,}")
col2.metric("Loyal Champions", f"{len(champions):,}", f"{len(champions)/total*100:.1f}%")
col3.metric("Lost High Spenders", f"{len(lost_high):,}")
col4.metric("Avg Champion Spend", f"R${champions['monetary'].mean():.0f}")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Segment Distribution")
    counts = df["segment"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(counts.index, counts.values,
           color=[colors_map[s] for s in counts.index], edgecolor="black")
    ax.set_ylabel("Number of customers")
    ax.set_title("Customer Segments — K-Means (k=4)")
    ax.set_xticklabels(counts.index, rotation=15, ha="right")
    for i, v in enumerate(counts.values):
        ax.text(i, v + 200, f"{v:,}", ha="center", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_right:
    st.markdown("### Recency vs Monetary")
    fig, ax = plt.subplots(figsize=(6, 4))
    for segment, group in df.groupby("segment"):
        ax.scatter(group["recency"], group["monetary"],
                   label=segment, color=colors_map[segment], alpha=0.4, s=8)
    ax.set_xlabel("Recency (days since last order)")
    ax.set_ylabel("Monetary (total spent R$)")
    ax.set_title("Customer Segments — Recency vs Monetary")
    ax.legend(fontsize=7)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")
st.markdown("### Cluster Profiles")
profile = df.groupby("segment").agg(
    recency=("recency", "mean"),
    frequency=("frequency", "mean"),
    monetary=("monetary", "mean"),
    count=("customer_unique_id", "count")
).round(1).reset_index()
profile.columns = ["Segment", "Avg Recency (days)", "Avg Frequency", "Avg Monetary (R$)", "Count"]
st.dataframe(profile, use_container_width=True)

st.markdown("---")
st.markdown("### Explore a Segment")
segment_filter = st.selectbox("Select a segment", df["segment"].unique())
filtered = df[df["segment"] == segment_filter]

col1, col2, col3 = st.columns(3)
col1.metric("Customers", f"{len(filtered):,}")
col2.metric("Avg Days Since Last Order", f"{filtered['recency'].mean():.0f}")
col3.metric("Avg Total Spend", f"R${filtered['monetary'].mean():.0f}")

fig, axes = plt.subplots(1, 3, figsize=(12, 3))
color = colors_map[segment_filter]
axes[0].hist(filtered["recency"], bins=30, color=color, edgecolor="black")
axes[0].set_title("Recency Distribution")
axes[0].set_xlabel("Days")
axes[1].hist(filtered["frequency"], bins=10, color=color, edgecolor="black")
axes[1].set_title("Frequency Distribution")
axes[1].set_xlabel("Orders")
axes[2].hist(filtered["monetary"], bins=30, color=color, edgecolor="black")
axes[2].set_title("Monetary Distribution")
axes[2].set_xlabel("R$")
plt.suptitle(f"{segment_filter}", fontsize=13)
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")
st.markdown("### Business Recommendations")
st.markdown("""
1. **Protect Loyal Champions (2,997)** — loyalty rewards, early access, personalised offers
2. **Win back Lost High Spenders (28,868)** — a 10% win-back rate adds ~R$900k in revenue
3. **Convert Recent One-timers (25,277)** — follow-up email or second-purchase incentive while the relationship is fresh
4. **Deprioritize Lost Bargain Hunters (38,951)** — largest group, lowest ROI
""")
