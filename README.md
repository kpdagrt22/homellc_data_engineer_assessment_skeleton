# 🏗️ HomeLLC Data Engineering Assessment

Welcome! This project demonstrates end-to-end data engineering skills, including:

- ✅ **SQL databases**: Data modeling, normalization, and scripting
- ✅ **Python & ETL**: Data cleaning, transformation, and loading workflows

---

## 📚 Assessment Overview

Each section is structured with:

- **Problem:** Background and context for the task  
- **Task:** Your requirements  
- **Solution:** My design approach and implementation details  

> **Tech Stack Constraints:**  
> - Only use **Python** for ETL logic  
> - Only use **SQL/MySQL** (via Docker) for schema creation  
> - Avoid ORMs; write SQL by hand  
> - You may use `pandas`, `openpyxl`, and `mysql-connector-python` for processing

---

## 🚩 Problem

The input data (a CSV file) contains multiple flattened fields related to real estate properties. These include valuation, rehab, tax info, and sales status.

- Each row corresponds to a property
- The dataset is not normalized
- The business logic mapping of fields to tables is defined in `Field Config.xlsx`

---

## 🎯 Task

1. Normalize and design a relational schema in MySQL
2. Write SQL scripts to create the tables with appropriate constraints
3. Write a Python-based ETL pipeline to:
   - Ingest, clean, and validate the data
   - Map fields to respective tables using the config file
   - Insert data into MySQL with **primary** and **foreign key** integrity
   - Implement deduplication and truncate-and-reload support
4. Package your work for reproducible execution

---

## 📦 Project Structure
├── data/
│ ├── fake_data.csv # Raw input dataset
│ └── Field Config.xlsx # Field-to-table mapping
├── sql/
│ └── 00_init_db_dump.sql # Normalized SQL schema
├── scripts/
│ └── run_etl.py # Main ETL pipeline
├── Dockerfile.initial_db # MySQL init Dockerfile
├── docker-compose.initial.yml # Compose config to start DB
├── requirements.txt # Python dependencies
└── README.md # You are here

---

## 🧠 Database Design

The database is normalized into the following structure:

| Table      | Description                         | FK Relationships     |
|------------|-------------------------------------|----------------------|
| `property` | Core property attributes            | `id` (PK)            |
| `leads`    | Sales or lead generation info       | `property_id` (FK)   |
| `valuation`| Zestimate, ARV, rent, pricing       | `property_id` (FK)   |
| `hoa`      | Homeowner association details       | `property_id` (FK)   |
| `rehab`    | Rehab estimates & flags             | `property_id` (FK)   |
| `taxes`    | Property taxes and assessment       | `property_id` (FK)   |

Each table is linked to `property.id` via foreign keys to maintain referential integrity.

---

## 🧮 Python ETL Logic

### ✔ Key Features

- Dynamically reads field mapping from `Field Config.xlsx`
- Cleans and standardizes all column names
- Automatically builds a table-to-column map using the config
- Supports two modes:
  - **`--truncate`**: wipes all tables and reloads from scratch
  - **Default**: skips already inserted `property` rows (via `property_title` deduplication)
- Handles FK dependencies by inserting into `property` first, then dependent tables
- Uses raw `mysql-connector-python` (no ORM)

### ⚙ Logic Flow (`run_etl.py`)

```text
1. Load config + CSV
2. Normalize column names (snake_case)
3. Build `table_map` = {table: [columns]} using Field Config
4. Optionally TRUNCATE all tables (with FK checks disabled)
5. Insert into `property` (with deduplication)
6. For each child table:
   a. Pull relevant columns
   b. Add FK (property_id)
   c. Insert row-by-row
7. Commit and close connection
```

🚀 How to Run the Project
Step 1: Clone the Repository
bash
Copy
Edit
git clone https://github.com/kpdagrt22/homellc_data_engineer_assessment_skeleton.git
cd homellc_data_engineer_assessment_skeleton



Step 2: Start MySQL with Docker
bash
Copy
Edit
docker-compose -f docker-compose.initial.yml up --build -d
MySQL starts at localhost:3306

Credentials are:
user:     db_user
password: 6equj5_db_user
database: home_db


Step 3: Install Python Requirements

pip install -r requirements.txt
🧪 Run ETL
Option A: Fresh Load (Truncate All)
bash
Copy
Edit
python scripts/run_etl.py --truncate
Disables FK checks

Truncates all normalized tables

Reloads full dataset

Option B: Deduplicated Load (Default)
bash
Copy
Edit
python scripts/run_etl.py
Inserts only new property rows (based on property_title)

Preserves existing data

📊 Validate Results in MySQL
bash
Copy
Edit
docker exec -it mysql_ctn mysql -u root -p
# Enter password: 6equj5_root

USE home_db;

SELECT 'property', COUNT(*) FROM property
UNION
SELECT 'leads', COUNT(*) FROM leads
UNION
SELECT 'valuation', COUNT(*) FROM valuation
UNION
SELECT 'hoa', COUNT(*) FROM hoa
UNION
SELECT 'rehab', COUNT(*) FROM rehab
UNION
SELECT 'taxes', COUNT(*) FROM taxes;
Expected output (after full run):


+------------+----------+
| table_name | COUNT(*) |
+------------+----------+
| property   |    10000 |
| leads      |    10000 |
| valuation  |    10000 |
| hoa        |    10000 |
| rehab      |    10000 |
| taxes      |    10000 |
+------------+----------+



✅ Features Implemented
✔ Clean and reproducible ETL process

✔ Schema-first, normalized DB design

✔ Deduplication based on property_title

✔ Truncate-and-load support

✔ Error-handling and safe inserts

✔ Documentation with complete setup instructions

👨‍💻 Author
Prakash Kantumutchu
Data & AI Engineer | Python & MLOps Enthusiast


📄 License
This project is proprietary and confidential.
All rights reserved by HomeLLC for assessment and evaluation purposes.

📬 Submission Checklist
✅ Edited this README.md with all required instructions
✅ Organized code into scripts/, sql/, data/ folders
✅ ETL script works end-to-end via command line
✅ All steps are reproducible by the reviewer
✅ Schema and logic clearly documented
✅ Project pushed to GitHub for submission

Thank you! Looking forward to your feedback.
