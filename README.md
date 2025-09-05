[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/) 
[![DuckDB](https://img.shields.io/badge/DuckDB-Ready-yellow?logo=duckdb&logoColor=white&style=for-the-badge)](https://duckdb.org/) 
[![Apache Beam](https://img.shields.io/badge/Apache%20Beam-Ready-orange?logo=apache&logoColor=white&style=for-the-badge)](https://beam.apache.org/) 
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-Orchestration-brightgreen?logo=apacheairflow&logoColor=white&style=for-the-badge)](https://airflow.apache.org/) 
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql&logoColor=white&style=for-the-badge)](https://www.postgresql.org/)

# 🐣 Mini GCP (Local Data Pipeline)

A **local modern data pipeline** that mimics GCP services. It uses **Python, Apache Beam, Airflow, DuckDB, and PostgreSQL** to extract, transform, load, validate, and analyze synthetic sales data.  

---

## 📑 Table of Contents
- [🧠 Why "Mini GCP"?](#-why-mini-gcp)
- [⚡ Quickstart](#-quickstart)
- [🔄 Pipeline Flow](#-pipeline-flow)
- [📁 Project Structure](#-project-structure)
- [⚙️ Tools & Libraries](#-tools--libraries)
- [📜 License](#-license)

---

## 🧠 Why "Mini GCP"?
This repo mimics GCP-like services (Cloud Functions, Dataflow, BigQuery) but runs **entirely local**:  
- 🆓 No cloud costs  
- 🧪 Great for testing & learning  
- 💻 Works offline 

---

## ⚡ Quickstart

- Clone the repository and set up the environment:

```
git clone https://github.com/your-repo/mini-gcp.git
cd mini-gcp
```

### ⚙️ Create a `.env` file

- You could also show an example of what the `.env` should look like:

```
# PostgreSQL
POSTGRES_HOST=...
POSTGRES_PORT=...
POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...

# Airflow
AIRFLOW__CORE__EXECUTOR=...
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=...

# BigQuery
GOOGLE_CREDENTIALS_PATH=...
BQ_PROJECT_ID=...
BQ_DATASET=...

# Sheets
SPREADSHEET_ID=...
```

> 💡 **Important:** Create a `.env` file before running the pipeline.  
> 💡 See [🛠️ Environment & Docker Notes](#️-environment--docker-notes)
---

## 🔄 Pipeline Flow

```
generate data 
   └──> test data
         └──> extract data  
               └──> initial validation 
                     └──> transform data 
                           └──> load data
                                 └──> log metadata
                                       └──> export to BigQuery
                                             └──> final validation
                                                   └──> export to Google Sheets
```

---

## 📁 Project Structure

```
.
.
├── dags/                 # Airflow DAGs
├── data/                 # Data storage (raw, transformed, validations, etc.)
├── extract/              # Data extraction logic
├── transform/            # Data transformation (Apache Beam)
├── load/                 # Load into DuckDB/PostgreSQL
├── initial_validation/   # First quality checks
├── final_validation/     # Final quality checks
├── log_metadata/         # Metadata logging
├── functions/            # Triggers
├── scripts/              # Helper scripts
├── docker-compose.yml    # Local environment
├── Dockerfile            # Container image
└── requirements.txt      # Dependencies
```

---

## ⚙️ Tools & Libraries

- 🐍 [Python](https://www.python.org/)
- 🦆 [DuckDB](https://duckdb.org/)
- ⚙️ [Apache Beam](https://beam.apache.org/)
- ✈️ [Apache Airflow](https://airflow.apache.org/)
- 🐘 [PostgreSQL](https://www.postgresql.org/)
- 🐋 [Docker / Docker Compose](https://docs.docker.com/compose/)
- 🧪 `pyspark`, `Faker`, `unidecode`, `watchdog`, `apache-beam[gcp]`, `pandas`, `python-dotenv`, `duckdb`, `sqlalchemy`, `psycopg2-binary`
- 📦 Local folders instead of cloud storage.

---

## ✅ Requirements

- Python 3.8+ (In this case we're using 3.10)
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
2. Open the integrated terminal (“Ctrl + ` (backtick)”) or via menu: Terminal > New Terminal.
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

---

### 🛠️ Project Setup & Maintenance Scripts

This project includes a set of helper scripts to simplify initial setup, resetting the environment, and fixing file permissions when working with Airflow and Docker locally.

1. `1_init.sh` — Initialize Airflow ✈️
This script builds the Airflow images and runs the Airflow initialization process inside Docker.

Usage:

```
chmod +x 1_init.sh
./1_init.sh
```

What it does:

- 🏗️ Builds the `airflow-init` image without using Docker BuildKit (for better compatibility).

- 🗄️ Runs the `airflow-init` container to set up Airflow’s metadata database and initial configuration.

2. `2_fix_permissions.sh` — Fix Project Folder Permissions 🔐
This script adjusts file and folder permissions so that the Airflow user inside the container (UID `50000`) can access and modify project files without permission errors.

Usage:

```
chmod +x 2_fix_permissions.sh
./2_fix_permissions.sh
```

What it does:

- 📂 Iterates over key project folders (`dags`, `data`, `extract`, `transform`, etc.).

- 👤 Changes the owner to UID `50000` (Airflow user) and GID `0` (root group).

- 🔒 Sets secure folder (`755`) and file (`644`) permissions.

Use this when:

- ⚠️ You see permission denied errors when Airflow tries to read/write files.

3. `3_reset_docker.sh` — Reset Docker Environment 🔄🐳
This script completely cleans and rebuilds your local Docker setup for the project.

Usage:

```
chmod +x 3_reset_docker.sh
./3_reset_docker.sh
```

What it does:

- 🛑 Stops all running containers and removes volumes/orphan containers.

- 🧹 Prunes unused volumes and containers.

- 🏗️ Rebuilds the project’s Docker image from scratch.

- 🚀 Starts services again with `docker compose up -d`.

Use this when:

- 🌱 You want a fresh start.

- ⚠️ There are issues with containers not working as expected.

#### 💡 Tip:
If you’re setting up the project for the first time, run the scripts in this order:

1. `1_init.sh` → ✈️ Initialize Airflow.

2. `2_fix_permissions.sh` → 🔐 Ensure correct file permissions.

3. (Optional) `3_reset_docker.sh` 🔄🐳 if you need a clean rebuild later.

---

## 🛠️ Environment & Docker Notes  

💡 **Important:**  
Every time you add a new variable in the `.env` file or edit the `docker-compose.yml` file, you need to **restart Docker** using the script:  

```
./3_reset_docker.sh
```

- This script stops and removes running containers, rebuilds the images, and restarts everything from scratch.

---

## 🚧 Future Improvements

- [X] Add Airflow DAG for orchestration.

- [X] Create Looker Studio or local dashboards.

- [X] Extend validation rules with Great Expectations.

---

## 📊 LookerStudio & GoogleSheets:

- [GoogleSheets](https://docs.google.com/spreadsheets/d/178xzlNCJKyK7dmkyRhnoA7vkdypbRnbK14glFOHEODI/edit?gid=0#gid=0)

- [LookerStudio](https://lookerstudio.google.com/u/0/reporting/1ebab84e-02b6-4370-9691-83375c31a4cd/page/tEnnC)

---

## 📬 Feedback or Questions?

Feel free to open an issue or submit a PR! <3

---

## 🤝 Contributing

1. Fork the repo and create your branch:
```
git checkout -b feature/my-feature
```
2. Run tests and format code before pushing.
3. Submit a Pull Request 🚀.

---

## 👩‍💻 Author
Camila Muñoz – [@CamilaJaviera91](https://github.com/CamilaJaviera91)
💬 Happy to connect and discuss data pipelines or open source!

---

## 📜 License
This project is licensed under the MIT License. See LICENSE for details.

---
