# ecommerce-nlp-customer-segmentation
Ratings tell you what happened. Reviews tell you why. Segmentation tells you who to act on.

This project analyzes Brazilian e-commerce data from Olist to uncover customer insights using Natural Language Processing and RFM-based clustering.  We explore how review sentiment and emotions align with ratings, identify hidden dissatisfaction, and segment customers into actionable groups to improve the overall customer experience.
```
olist-nlp-clustering-project/
│
├── data/
│   ├── raw/
│   │   ├── olist_order_reviews_dataset.csv
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   └── product_category_name_translation.csv
│   │
│   └── processed/
│       ├── reviews_sentiment.csv
│       ├── reviews_emotions_categories.csv
│       └── customer_segments.csv
│
├── notebooks/
│   ├── 01_nlp_sentiment_ratings.ipynb
│   ├── 02_nlp_emotion_categories.ipynb
│   ├── 03_customer_clustering_rfm.ipynb
│   └── 04_final_storytelling_and_dashboard_prep.ipynb
│
├── src/
│   ├── data_cleaning.py
│   ├── nlp_utils.py
│   ├── clustering_utils.py
│   └── visualization_utils.py
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── app/
│   └── streamlit_app.py
│
├── README.md
└── requirements.txt
```