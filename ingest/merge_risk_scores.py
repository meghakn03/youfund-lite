import pandas as pd
from pathlib import Path

data_dir = Path("/opt/airflow/data")

merchants = pd.read_csv(data_dir / "merchants.csv")
risk_scores = pd.read_csv(data_dir / "risk_scores.csv")

merged = merchants.merge(risk_scores, on="merchant_id", how="left")

merged.to_csv(data_dir / "merchants_with_scores.csv", index=False)
print(f"✅ Merged file saved to {data_dir / 'merchants_with_scores.csv'}")
