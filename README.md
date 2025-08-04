# 🐣 Mini GCP (Local Data Pipeline)

This project simulates a **modern data pipeline** architecture, entirely **locally** and **without requiring Google Cloud or paid services**. It follows a modular design to extract, transform, load, validate, and analyze synthetic sales data using Python, Apache Beam, DuckDB, and PostgreSQL (optional).

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