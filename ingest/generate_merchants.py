# ingest/generate_merchants.py

import pandas as pd
import random
from faker import Faker
from pathlib import Path

fake = Faker()
output_path = Path("/opt/airflow/data/merchants.csv")  # Changed to absolute path in container
output_path.parent.mkdir(parents=True, exist_ok=True)

def generate_merchant(i):
    return {
        "merchant_id": f"M{i:05d}",
        "name": fake.company(),
        "monthly_revenue": round(random.uniform(5000, 100000), 2),
        "transaction_volume": random.randint(50, 5000),
        "tenure_months": random.randint(1, 60),
        "has_defaulted_before": random.choice([0, 1]),
        "industry": random.choice(["Retail", "Food", "Services", "E-commerce", "Health"]),
        "country": fake.country_code()
    }

def generate_merchants(n=1000):
    return pd.DataFrame([generate_merchant(i) for i in range(n)])

if __name__ == "__main__":
    df = generate_merchants(1000)
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} merchants to {output_path.resolve()}")