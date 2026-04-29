# Beyond Ratings: Understanding E-Commerce Customers with NLP & Clustering

## Project Overview

This project analyzes the Brazilian e-commerce dataset from Olist to better understand customer experience through two complementary perspectives:

1. **Customer Voice** — what customers say in their reviews  
2. **Customer Behavior** — how customers purchase over time  

The main goal is to move beyond star ratings and uncover deeper insights about satisfaction, frustration, delivery issues, and customer segments.

Our guiding question was:

> **Can we use NLP and clustering to uncover customer segments and improve the e-commerce experience?**

By combining review analysis, emotion detection, delivery performance, product category data, and RFM-based customer segmentation, we identified patterns that can help Olist improve customer satisfaction, prioritize operational improvements, and target customers more effectively.

---

## Business Problem

E-commerce platforms often rely heavily on review scores to understand customer satisfaction. However, star ratings alone do not always tell the full story.

A customer may leave a high rating but still mention problems in the review text. Another customer may express anger because of delivery delays, damaged products, or unmet expectations. At the same time, not all customers have the same value or behavior patterns.

This project addresses three key business questions:

1. **Do review scores align with the sentiment expressed in review text?**
2. **Are negative emotions, especially anger, connected to logistics issues such as late delivery?**
3. **Can customers be segmented into meaningful groups based on purchasing behavior?**

---

## Dataset

We used the **Olist Brazilian E-Commerce Public Dataset** from Kaggle.

Main datasets used:

```text
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_products_dataset.csv
product_category_name_translation.csv
olist_customers_dataset.csv
olist_order_payments_dataset.csv
````

These tables allowed us to connect:

* review scores
* review text
* delivery status
* product categories
* customer IDs
* payment value
* order dates

---

## Project Structure

```text
beyond-ratings-nlp-clustering/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 00_data_cleaning_shared.ipynb
│   ├── 01_nlp_sentiment_ratings.ipynb
│   ├── 02_emotion_categories_logistics.ipynb
│   ├── 03_customer_clustering_rfm.ipynb
│   └── 04_final_storytelling_and_dashboard_prep.ipynb
│
├── src/
│   └── data_utils.py
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── streamlit/
│
├── README.md
└── pyproject.toml
```

---

## Team Roles

### Gonçalo — Sentiment vs Ratings

Gonçalo focused on whether customer review scores matched the sentiment expressed in the review text.

His work answered:

* Do 1–5 star ratings align with positive or negative sentiment?
* Are there 5-star reviews with negative language?
* Where do ratings and review text disagree?

This helped reveal cases of **hidden dissatisfaction**, where the rating alone did not fully capture the customer experience.

---

### Rachel — Emotion Analysis, Logistics & Categories

Rachel focused on emotion analysis and connected customer emotions to delivery performance and product categories.

Her work answered:

* Are angry reviews mostly connected to logistics?
* Are joyful reviews tied to specific product categories?
* What does emotion analysis reveal that ratings alone do not?

A RoBERTa-based emotion classifier was used to label reviews with emotions such as anger and joy. Because the reviews are primarily in Portuguese and the RoBERTa model used was English-based, the results were interpreted as **directional signals** rather than exact emotion labels.

A keyword-based emotion system was also kept as a backup validation layer, although the final outputs used the RoBERTa-based results.

Key result:

```text
Total analyzed reviews: 50,055
Anger rate: 11.77%
Joy rate: 3.00%
```

The strongest finding was that anger was closely connected to late deliveries, making logistics one of the clearest drivers of negative customer emotion.

---

### Sarah — Customer Segmentation with RFM

Sarah focused on customer segmentation using RFM analysis.

Her work used:

* **Recency** — how recently a customer purchased
* **Frequency** — how often a customer purchased
* **Monetary value** — how much the customer spent

She applied both:

* K-Means clustering
* Hierarchical clustering

The goal was to identify meaningful customer groups such as:

* Loyal champions
* Bargain hunters
* At-risk customers
* One-time buyers
* High-value customers

This helped answer the question:

> Which customer groups should Olist prioritize?

---

## Methodology

## 1. Shared Data Cleaning

We first created a shared cleaning notebook to keep all team members aligned.

Main cleaning steps included:

* standardized column names using snake_case
* converted date columns with `pd.to_datetime()`
* created a combined `review_text` column
* created delivery-related features:

  * `delivery_time_days`
  * `estimated_delivery_days`
  * `delivery_delay_days`
  * `is_late`
* saved clean datasets to `data/processed/`

The shared cleaning logic was supported by reusable functions in:

```text
src/data_utils.py
```

This helped ensure consistency across all notebooks.

---

## 2. Sentiment vs Ratings

The first NLP task compared review scores with sentiment from review text.

The analysis explored whether:

* low ratings matched negative sentiment
* high ratings matched positive sentiment
* some reviews showed contradictions between rating and language

This was important because ratings can sometimes hide dissatisfaction.

Example business idea:

> A 5-star review with negative language may indicate that the customer was generally satisfied but still experienced a problem worth addressing.

---

## 3. Emotion Analysis

The second NLP task focused on emotion rather than simple positive/negative sentiment.

Rachel connected review text with:

* delivery performance
* late vs on-time orders
* product categories

The analysis focused especially on anger because it appeared more frequently than joy and acted as a stronger warning signal for customer experience problems.

Key questions:

* Are angry reviews more common when deliveries are late?
* Are joyful reviews concentrated in certain categories?

Main finding:

> Anger was not random. It was strongly associated with logistics and delivery delays.

Joyful reviews were less common overall, but they still helped identify categories where customer experiences were more positive.

---

## 4. Customer Segmentation

The clustering section used RFM features to segment customers based on behavior.

Features used:

```text
recency_days
frequency
monetary
```

The clustering process included:

* building an RFM customer-level table
* scaling features
* applying K-Means clustering
* using the elbow method and silhouette score
* applying hierarchical clustering
* interpreting and naming customer segments

This allowed us to move from general customer analysis to more targeted business recommendations.

---

## Key Insights

## 1. Ratings Do Not Tell the Full Story

Review scores are useful, but they do not always fully reflect what customers write.

Sentiment analysis helped identify mismatches between ratings and review language, including cases where customers gave high ratings but still used negative language.

This suggests that Olist should not rely only on star ratings to understand customer satisfaction.

---

## 2. Anger Is a Customer Experience Warning Signal

Across 50,055 analyzed reviews:

```text
Anger rate: 11.77%
Joy rate: 3.00%
```

Anger appeared more often than joy and became the most important emotional signal in the review text.

The strongest emotion insight was that anger was closely tied to delivery performance.

---

## 3. Logistics Are a Major Driver of Negative Emotion

When emotion labels were compared with delivery status, angry reviews were more common among late deliveries than among orders delivered on time or early.

This suggests that late delivery is one of the clearest operational causes of customer frustration.

Business interpretation:

> Improving delivery reliability and communication could directly reduce negative customer emotion.

---

## 4. Joyful Reviews Are Less Common but Still Useful

Joy represented around 3.00% of analyzed reviews.

Because joy was less common, we interpreted this result carefully. However, joyful reviews were still useful for identifying product categories where customer experiences were more positive.

This can help Olist understand where customer expectations are being met or exceeded.

---

## 5. Customer Segments Support Better Targeting

RFM clustering helped identify different types of customers based on purchasing behavior.

This matters because not all customers should receive the same strategy.

For example:

* loyal customers may respond well to rewards and personalized offers
* at-risk customers may need win-back campaigns
* bargain hunters may respond to discounts or free-shipping thresholds
* high-value customers may deserve premium support or retention campaigns

---

## Business Recommendations

## 1. Improve Delivery Reliability

Because anger is strongly associated with late deliveries, Olist should prioritize logistics improvements.

Recommended actions:

* improve delivery tracking
* reduce late deliveries
* monitor late-order patterns by seller, region, and category
* identify recurring logistics bottlenecks

---

## 2. Communicate Delays Proactively

Even when delays cannot be avoided, better communication can reduce frustration.

Recommended actions:

* send proactive delay notifications
* provide updated estimated delivery dates
* offer apology messages or small compensation for severe delays
* create recovery workflows for customers affected by late delivery

---

## 3. Use Review Text as an Early Warning System

Olist should not rely only on review scores.

Recommended actions:

* flag high-rating reviews with negative language
* monitor angry reviews for logistics problems
* track emotional patterns over time
* identify categories, sellers, or regions with rising negative emotion

---

## 4. Target Customers by Segment

Customer segmentation allows Olist to create more personalized strategies.

Examples:

| Segment              | Possible Strategy                             |
| -------------------- | --------------------------------------------- |
| Loyal Champions      | rewards, exclusive offers, early access       |
| At-Risk Customers    | win-back campaigns, apology coupons           |
| Bargain Hunters      | discounts, free shipping thresholds           |
| High-Value Customers | premium support, personalized recommendations |
| One-Time Buyers      | onboarding campaigns, follow-up offers        |

---

## 5. Learn from Positive Categories

Categories with joyful reviews can help Olist understand what is working well.

Recommended actions:

* investigate categories with positive emotional patterns
* identify whether positive reviews are linked to fast delivery, quality, or price
* replicate successful practices across weaker categories

---

## Limitations

This project has a few important limitations:

* The review dataset is primarily in Portuguese.
* The RoBERTa emotion model used was English-based, so emotion outputs were interpreted as directional rather than exact.
* The keyword-based emotion approach was used only as a backup validation layer, not as the final result.
* Some product categories naturally have more reviews, so raw category counts should not be interpreted as perfect rankings.
* Customer segmentation depends on historical behavior and may not capture all motivations behind customer decisions.

Future improvements could include:

* using a Portuguese-native or multilingual emotion model
* translating reviews before emotion classification
* normalizing emotion rates by category volume
* connecting customer segments with emotion labels
* building a Streamlit dashboard for interactive exploration

---

## Final Conclusion

This project shows that customer experience cannot be fully understood through ratings alone.

Ratings tell us **what score** the customer gave.
Review text tells us **why** the customer felt that way.
Customer segmentation tells us **who** Olist should prioritize.

By combining NLP, emotion analysis, logistics data, and RFM clustering, we identified clear opportunities for improving the e-commerce experience.

The strongest business takeaway is:

> **Delivery performance directly affects customer emotion, and angry reviews can serve as an early warning signal for operational problems.**

Improving logistics reliability, communicating delays proactively, and targeting customers based on behavior can help Olist create a better, more personalized e-commerce experience.
