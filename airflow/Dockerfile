FROM apache/airflow:2.7.1

# Install system dependencies as root first
USER root

RUN apt-get update && \
    apt-get install -y sqlite3 git && \
    rm -rf /var/lib/apt/lists/*

# Switch back to airflow user for Python packages
USER airflow
RUN mkdir -p /home/airflow/.dbt
COPY profiles.yml /home/airflow/.dbt/profiles.yml

RUN pip install --no-cache-dir \
    pandas \
    sqlalchemy \
    faker \
    scikit-learn \
    xgboost \
    boto3 \
    psycopg2-binary \
    dbt-postgres