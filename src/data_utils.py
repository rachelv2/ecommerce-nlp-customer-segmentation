import pandas as pd


def snake_columns(df):
    """
    Standardize column names to lowercase snake_case.
    """
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df


def convert_to_datetime(df, date_columns):
    """
    Convert selected columns to datetime.
    """
    df = df.copy()

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def create_review_text(df):
    """
    Combine review title and review message into one review_text column.
    """
    df = df.copy()

    df["review_comment_title"] = df["review_comment_title"].fillna("")
    df["review_comment_message"] = df["review_comment_message"].fillna("")

    df["review_text"] = (
        df["review_comment_title"] + " " + df["review_comment_message"]
    ).str.strip()

    df["has_review_text"] = df["review_text"].str.len() > 0

    return df


def add_delivery_features(df):
    """
    Add delivery timing features to the orders dataset.
    """
    df = df.copy()

    df["delivery_time_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days

    df["estimated_delivery_days"] = (
        df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]
    ).dt.days

    df["delivery_delay_days"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.days

    df["is_late"] = df["delivery_delay_days"] > 0

    return df