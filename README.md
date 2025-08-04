# 🐣 Mini GCP (Local Data Pipeline)

This project simulates a **modern data pipeline** architecture, entirely **locally**. It follows a modular design to extract, transform, load, validate, and analyze synthetic sales data using Python, Apache Beam, DuckDB, and PostgreSQL.

---

## 📁 Project Structure

```
.
├── data/             # Data storage layer (raw, processed, validated, warehouse)
├── extract/          # Data extraction logic
├── transform/        # Data transformation using Apache Beam
├── load/             # Load cleaned data into DuckDB
├── validate/         # Schema and quality validation
├── export/           # Optional: export to PostgreSQL
├── functions/        # Trigger logic (e.g., on new file)
├── scripts/          # Automation scripts
├── requirements.txt  # Python dependencies
└── README.md         # You are here!
```

---

## 📊 Data Folder Overview

- **data/raw/:** Initial synthetic data (e.g., raw_sales_1.csv)

- **data/extract/:** Copied file ready for transformation

- **data/processed/:** Cleaned file after transformation

- **data/validation/:** Schema reports in .csv and .json

- **data/warehouse/:** Final data stored in DuckDB (sales.duckdb)

---

## ⚙️ Tools & Libraries

- 🐍 Python
- 🦆 [DuckDB](https://duckdb.org/)
- ⚙️ [Apache Beam](https://beam.apache.org/)
- 🧪 `pyspark`, `Faker`, `unidecode`, `watchdog`, `apache-beam[gcp]`, `pandas`, `python-dotenv`, `duckdb`, `sqlalchemy`, `psycopg2-binary`
- 🐘 PostgreSQL
- 📦 Local folders instead of cloud storage

---

## ✅ Requirements

Install dependencies:

```
pip install -r requirements.txt
```

---

## 🚧 Future Improvements

- [ ] Add Airflow DAG for orchestration

- [ ] Create Looker Studio or local dashboards

- [ ] Extend validation rules with Great Expectations

---
