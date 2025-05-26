from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import random
from faker import Faker
import pandas as pd
from ingest.s3_utils import upload_df, download_df
from sqlalchemy import create_engine

BUCKET = "youfund-data"

default_args = {
    "owner": "megha",
    "start_date": datetime(2025, 5, 25),
    "retries": 1,
}

def generate_merchants_s3(**ctx):
    fake = Faker()
    def gen(i):
        return {
            "merchant_id": f"M{i:05d}",
            "name": fake.company(),
            "monthly_revenue": round(random.uniform(5000, 100000), 2),
            "transaction_volume": random.randint(50, 5000),
            "tenure_months": random.randint(1, 60),
            "has_defaulted_before": random.choice([0, 1]),
            "industry": random.choice(["Retail", "Food", "Services", "E-commerce", "Health"]),
            "country": fake.country_code(),
        }
    df = pd.DataFrame([gen(i) for i in range(1000)])
    upload_df(df, BUCKET, "merchants.csv")

def train_model_s3(**ctx):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer
    from xgboost import XGBClassifier
    from sklearn.metrics import classification_report

    df = download_df(BUCKET, "merchants.csv")
    X = df.drop(columns=["merchant_id", "name", "has_defaulted_before"])
    y = df["has_defaulted_before"]
    pre = ColumnTransformer([
        ("num", "passthrough", ["monthly_revenue", "transaction_volume", "tenure_months"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["industry", "country"]),
    ])
    pipe = Pipeline([
        ("pre", pre),
        ("clf", XGBClassifier(use_label_encoder=False, eval_metric="logloss")),
    ])
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    print(classification_report(y_test, preds))
    # write scores
    df_scores = df.copy()
    df_scores["risk_score"] = pipe.predict_proba(df.drop(columns=["merchant_id", "name", "has_defaulted_before"]))[:,1]
    upload_df(df_scores[["merchant_id", "risk_score"]], BUCKET, "risk_scores.csv")

def merge_scores_s3(**ctx):
    m = download_df(BUCKET, "merchants.csv")
    r = download_df(BUCKET, "risk_scores.csv")
    merged = m.merge(r, on="merchant_id", how="left")
    upload_df(merged, BUCKET, "merchants_with_scores.csv")

def load_to_postgres(**ctx):
    # Download merged
    merged = download_df(BUCKET, "merchants_with_scores.csv")
    # Connect to Postgres (Docker Compose service)
    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/airflow")
    merged.to_sql("merchants", engine, if_exists="replace", index=False)
    print("✅ Loaded merged data into Postgres")

with DAG("youfund_etl_pipeline", default_args=default_args, schedule_interval=None, catchup=False) as dag:
    t1 = PythonOperator(task_id="generate_merchants", python_callable=generate_merchants_s3)
    t2 = PythonOperator(task_id="train_model", python_callable=train_model_s3)
    t3 = PythonOperator(task_id="merge_scores", python_callable=merge_scores_s3)
    t4 = PythonOperator(task_id="load_to_postgres", python_callable=load_to_postgres)
    t1 >> t2 >> t3 >> t4
