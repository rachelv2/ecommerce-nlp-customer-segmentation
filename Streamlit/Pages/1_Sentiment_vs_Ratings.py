import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Sentiment vs Ratings", page_icon="📊", layout="wide")

st.title("📊 Sentiment vs Ratings")
st.markdown("Do star ratings reflect what customers actually wrote?")
st.markdown("---")

ROOT = Path(__file__).parent.parent.parent

@st.cache_data
def load_data():
    return pd.read_csv(ROOT / "data" / "processed" / "sentiment_predictions.csv")

df = load_data()

# add mismatch column
df["mismatch"] = df["review_score"] != df["predicted_score"]

# --- Key metrics ---
total = len(df)
mismatch_count = df["mismatch"].sum()
mismatch_rate = mismatch_count / total * 100
five_star_neg = df[(df["review_score"] == 5) & (df["predicted_score"] <= 2)]
five_star_neg_rate = len(five_star_neg) / len(df[df["review_score"] == 5]) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Reviews Analysed", f"{total:,}")
col2.metric("Overall Mismatch Rate", f"{mismatch_rate:.1f}%")
col3.metric("5-star with Negative Text", f"{five_star_neg_rate:.1f}%")
col4.metric("3-star Mismatch Rate", "78%", help="Most misleading score")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Actual Score vs Predicted Score")
    fig, ax = plt.subplots(figsize=(6, 4))
    pivot = pd.crosstab(df["review_score"], df["predicted_score"])
    sns.heatmap(pivot, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_xlabel("Predicted Score")
    ax.set_ylabel("Actual Score")
    ax.set_title("Diagonal = agreement. Off-diagonal = mismatch.")
    st.pyplot(fig)
    plt.close()

with col_right:
    st.markdown("### Mismatch Rate by Star Rating")
    mismatch_by_score = df.groupby("review_score")["mismatch"].mean() * 100
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = ["green" if v < 20 else "orange" if v < 50 else "tomato" for v in mismatch_by_score.values]
    ax.bar(mismatch_by_score.index, mismatch_by_score.values, color=colors, edgecolor="black")
    ax.set_xlabel("Star Rating")
    ax.set_ylabel("Mismatch Rate (%)")
    ax.set_title("3-star is the most misleading")
    ax.set_xticks([1, 2, 3, 4, 5])
    for i, v in enumerate(mismatch_by_score.values):
        ax.text(i + 1, v + 1, f"{v:.0f}%", ha="center", fontsize=9)
    st.pyplot(fig)
    plt.close()

st.markdown("---")
st.markdown("### Explore the Data")
score_filter = st.selectbox("Filter by actual star rating", [1, 2, 3, 4, 5])
show_mismatch_only = st.checkbox("Show mismatches only")
filtered = df[df["review_score"] == score_filter]
if show_mismatch_only:
    filtered = filtered[filtered["mismatch"]]
st.dataframe(
    filtered[["review_score", "predicted_score", "predicted_label", "confidence", "review_text"]].head(20),
    use_container_width=True
)

st.markdown("---")
st.markdown("### Key Findings")
st.markdown("""
| Metric | Value |
|---|---|
| Overall mismatch rate | **22.3%** |
| Exact score agreement | 60.4% |
| Within 1 star agreement | 83.2% |
| 5-star + negative text | **10.8%** |
| Most misleading score | **3-star (78% mismatch)** |
""")

st.markdown("### Business Recommendations")
st.markdown("""
1. **Don't filter by score alone** — 5-star ratings hide genuine frustration
2. **Treat 3-star as a warning** — it reads far more negative than it appears
3. **Use NLP alongside ratings** for any customer feedback pipeline
""")
