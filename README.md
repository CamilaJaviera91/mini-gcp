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

- Python 3.8+ (In this case we're usin 3.10)
- VS Code (Visual Studio Code)
- PostgreSQL
- DuckDB
- Apache Beam
- Git
- Docker
- DBeaver

### 🐍 Creating a Python Virtual Environment in VS Code

To keep dependencies isolated and avoid conflicts, it’s a good practice to use a virtual environment for this project. Here’s how you can set it up in VS Code:

1. Open your project folder in VS Code.
2. Open the integrated terminal (Ctrl + ) or via menu: Terminal > New Terminal.
3. Create a virtual environment (only once):

- On Linux/macOS:

```
python3 -m venv .venv
```

- On Windows (PowerShell):

```
python -m venv .venv
```

- This creates a .venv folder inside your project with an isolated Python environment.

4. Activate the virtual environment:

- On Linux/macOS:

```
source .venv/bin/activate
```

- On Windows (PowerShell):

```
.venv\Scripts\Activate.ps1
```

- After activation, your terminal prompt will show the environment name, e.g., (.venv).

5. Install project dependencies inside the virtual environment:

```
pip install -r requirements.txt
```

6. (Optional) Select the interpreter in VS Code:

- Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS)

- Type and select Python: Select Interpreter

- Choose the interpreter from your `.venv` folder (it will show something like `.venv/bin/python` or `.venv\Scripts\python.exe`)

Now VS Code will use the virtual environment’s Python for running and debugging.

### ⚙️ Project Setup & Maintenance Scripts

This project includes a set of helper scripts to simplify initial setup, resetting the environment, and fixing file permissions when working with Airflow and Docker locally.

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