# 🐣 Mini GCP (Local Data Pipeline)

This project simulates a **modern data pipeline** architecture, entirely **locally**. It follows a modular design to extract, transform, load, validate, and analyze synthetic sales data using Python, Apache Beam, DuckDB, and PostgreSQL.

---

## 🧠 Why "Mini GCP"?

This repo mimics a GCP-like modular pipeline (with stages like Cloud Functions, Dataflow, BigQuery), but:

- 🆓 Works locally

- 🧪 Ideal for testing and learning

- 💸 No cloud cost involved

---

## 📁 Project Structure

```
.
├── dags/                # Pipeline where we run all the tasks
├── data/                # Data storage layer (raw, processed, validated, warehouse)
├── export/              # Optional: export to PostgreSQL
├── extract/             # Data extraction logic
├── functions/           # Trigger logic (e.g., on new file)
├── initial_validation/  # Initial quality validation
├── load/                # Load cleaned data into DuckDB
├── scripts/             # Automation scripts
├── transform/           # Data transformation using Apache Beam
├── validate/            # Schema and quality validation
├── README.md            # You are here!
└── requirements.txt     # Python dependencies
```

---

## 📊 Data Folder Overview

- **data/raw/:** Initial synthetic data (e.g., raw_sales_1.csv)

- **data/extract/:** Copied file ready for transformation

- **data/initial_validation/:** validation raw reports in .csv and .json

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

- [X] Add Airflow DAG for orchestration

- [ ] Create Looker Studio or local dashboards

- [ ] Extend validation rules with Great Expectations

---

## 📬 Feedback or Questions?

Feel free to open an issue or submit a PR!

---

## 👩‍💻 Author
Camila Muñoz – @CamilaJaviera91
💬 Happy to connect and discuss data pipelines or open source!

---