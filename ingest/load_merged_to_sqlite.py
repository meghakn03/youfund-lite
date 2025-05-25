import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

data_dir = Path("/opt/airflow/data")
db_path = data_dir / "youfund.db"
merged_csv = data_dir / "merchants_with_scores.csv"

try:
    if not merged_csv.exists():
        raise FileNotFoundError(f"Missing input file: {merged_csv}")

    df = pd.read_csv(merged_csv)
    data_dir.mkdir(parents=True, exist_ok=True)

    # Use SQLAlchemy engine instead of direct sqlite3 connection
    engine = create_engine(f'sqlite:///{db_path}')
    
    # if_exists='replace' will now work properly
    df.to_sql('merchants', engine, if_exists='replace', index=False)
    print(f"✅ Merged data loaded into SQLite database at {db_path}")

except Exception as e:
    print(f"❌ Error loading data to SQLite: {str(e)}")
    raise