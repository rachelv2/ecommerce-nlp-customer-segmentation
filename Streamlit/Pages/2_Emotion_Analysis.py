import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Emotion Analysis", page_icon="😤", layout="wide")

st.title("😤 Emotion Analysis")
st.markdown("What are customers actually feeling?")
st.markdown("---")

ROOT = Path(__file__).parent.parent.parent

@st.cache_data
def load_data():
    return pd.read_csv(ROOT / "data" / "processed" / "reviews_emotions_categories.csv")

df = load_data()

# --- Key metrics ---
total = len(df)
anger_pct = len(df[df["emotion_label"] == "anger"]) / total * 100
joy_pct = len(df[df["emotion_label"] == "joy"]) / total * 100
late_anger = df[(df["emotion_label"] == "anger") & (df["is_late"] == True)]
late_anger_pct = len(late_anger) / len(df[df["emotion_label"] == "anger"]) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Reviews Analysed", f"{total:,}")
col2.metric("Joy", f"{joy_pct:.1f}%")
col3.metric("Anger", f"{anger_pct:.1f}%")
col4.metric("Angry Reviews from Late Deliveries", f"{late_anger_pct:.1f}%")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Emotion Distribution")
    emotion_counts = df["emotion_label"].value_counts()
    colors = {"joy": "gold", "neutral": "steelblue", "anger": "tomato", "sadness": "mediumpurple"}
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(emotion_counts.index, emotion_counts.values,
           color=[colors.get(e, "gray") for e in emotion_counts.index], edgecolor="black")
    ax.set_xlabel("Emotion")
    ax.set_ylabel("Number of reviews")
    ax.set_title("Overall Emotion Distribution")
    for i, v in enumerate(emotion_counts.values):
        ax.text(i, v + 100, f"{v:,}", ha="center", fontsize=9)
    st.pyplot(fig)
    plt.close()

with col_right:
    st.markdown("### Emotion by Delivery Status")
    pivot = pd.crosstab(df["delivery_status"], df["emotion_label"], normalize="index") * 100
    fig, ax = plt.subplots(figsize=(6, 4))
    pivot.plot(kind="bar", ax=ax,
               color=[colors.get(c, "gray") for c in pivot.columns],
               edgecolor="black")
    ax.set_xlabel("Delivery Status")
    ax.set_ylabel("Percentage (%)")
    ax.set_title("Emotions split by delivery status")
    ax.legend(title="Emotion", bbox_to_anchor=(1, 1))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")
st.markdown("### Top Product Categories by Emotion")

emotion_filter = st.selectbox("Select emotion", ["anger", "joy", "sadness", "neutral"])
filtered = df[df["emotion_label"] == emotion_filter]
top_cats = filtered["product_category_name_english"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 4))
color = colors.get(emotion_filter, "steelblue")
ax.barh(top_cats.index[::-1], top_cats.values[::-1], color=color, edgecolor="black")
ax.set_xlabel("Number of reviews")
ax.set_title(f"Top 10 categories for '{emotion_filter}' reviews")
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")
st.markdown("### Key Findings")
st.markdown("""
- **Joy (37.9%)** is the dominant emotion — most customers are happy
- **Anger (7.4%)** is strongly linked to late deliveries
- **Neutral (54.3%)** reviews are the largest group — customers often don't express strong emotion
- Late deliveries consistently produce more anger than on-time ones
""")

st.markdown("### Business Recommendations")
st.markdown("""
1. **Fix logistics first** — late delivery is the single biggest driver of angry reviews
2. **Double down on top joy categories** — identify what makes customers happy and amplify it
3. **Don't ignore neutral reviews** — they are the silent majority and could go either way
""")
