# Data Engineering Assessment

Welcome! This exercise is designed to evaluate your core skills in **data engineering**:

- **SQL databases**: Data modeling, normalization, and scripting
- **Python and ETL**: Data cleaning, transformation, and loading workflows

---

## 📚 How This Document Works

Each section is structured with:

- **Problem:** Background and context for the task
- **Task:** What you are required to do (including any bonus “extra” tasks)
- **Solution:** Where you must document your approach, decisions, and provide instructions for reviewers

> **Tech Stack:**  
> Please use only Python (for ETL/data processing) and SQL/MySQL (for database).  
> Only use extra libraries if they do not replace core logic, and clearly explain your choices in your solution.

---

## 0. Setup

1. **Fork and clone this repository:**
    ```bash
    git clone https://github.com/<your-username>/homellc_data_engineer_assessment_skeleton.git
    ```
2. **Start the MySQL database in Docker:**
    ```bash
    docker-compose -f docker-compose.initial.yml up --build -d
    ```
    - Database is available on `localhost:3306`
    - Credentials/configuration are in the Docker Compose file
    - **Do not change** database name or credentials

3. For MySQL Docker image reference:  
   [MySQL Docker Hub](https://hub.docker.com/_/mysql)

---

### Problem

You are provided with property-related data in a CSV file.
- Each row relates to a property.
- There are multiple Columns related to this property.
- The database is not normalized and lacks relational structure.


### Task

- **Normalize the data:**
  - Develop a Python ETL script to read, clean, transform, and load   data into your normalized MySQL tables.
  - Refer the field config document for the relation of business logic
  - Use primary keys and foreign keys to properly capture relationships

- **Deliverable:**
  - Write necessary python and sql scripts
  - Place the scripts inside the `sql/` directory)
  - The scripts should take the initial csv to your final, normalized schema when executed
  - Clearly document how to run your script, dependencies, and how it integrates with your database.

**Tech Stack:**  
- Python (include a `requirements.txt`)
Use **MySQL** and SQL for all database work  
- You may use any CLI or GUI for development, but the final changes must be submitted as python/ SQL scripts 
- **Do not** use ORM migrations—write all SQL by hand

### Solution

# 🏗️ HomeLLC Data Engineering Assessment

This project demonstrates end-to-end data engineering skills, including data modeling, schema normalization, ETL development, and Docker-based MySQL integration. The goal is to take raw property data in CSV format and load it into a fully normalized relational schema using a Python ETL pipeline.

---

## 📦 Project Structure
├── data/
│ ├── fake_data.csv # Input dataset
│ └── Field Config.xlsx # Mapping of columns to target tables
├── docker-compose.initial.yml # Docker configuration for MySQL container
├── Dockerfile.initial_db # Dockerfile to initialize MySQL schema
├── requirements.txt # Python package requirements
├── scripts/
│ └── run_etl.py # Main ETL script
├── sql/
│ └── 00_init_db_dump.sql # SQL schema definition (normalized)
└── README.md # You're here

---

## 🧩 Problem Statement

Each row in the input CSV represents a property and contains many fields — a mixture of ownership, valuation, tax, and lead status data. The dataset lacks normalization and relational integrity.

---

## ✅ Objectives

- Normalize the flat data into separate, relational tables
- Apply business logic mappings provided in `Field Config.xlsx`
- Load data into a MySQL database via a custom ETL pipeline
- Implement deduplication and optional truncate-and-load functionality

---

## ⚙️ Tech Stack

- **Language**: Python 3.10+
- **Database**: MySQL 8 (Dockerized)
- **Packages**: `pandas`, `openpyxl`, `mysql-connector-python`
- **Environment**: Docker, Docker Compose

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

bash
git clone https://github.com/kpdagrt22/homellc_data_engineer_assessment_skeleton.git
cd homellc_data_engineer_assessment_skeleton
docker-compose -f docker-compose.initial.yml up --build -d


###2. Start MySQL via Docker
This starts MySQL with the schema initialized from sql/00_init_db_dump.sql.
MySQL is accessible at localhost:3306.

Credentials are defined in docker-compose.initial.yml:

user: db_user

password: 6equj5_db_user

database: home_db

This starts MySQL with the schema initialized from sql/00_init_db_dump.sql.
MySQL is accessible at localhost:3306.

Credentials are defined in docker-compose.initial.yml:

user: db_user

password: 6equj5_db_user

database: home_db
###3. Install Python Dependencies

pip install -r requirements.txt

Run the ETL Pipeline
Option A: Truncate all tables and reload (Fresh Load)
python scripts/run_etl.py --truncate
This mode:

Temporarily disables foreign key checks

Truncates all normalized tables

Loads the full dataset


Option B: Load new records only (Deduplication Mode)
bash
Copy
Edit
python scripts/run_etl.py
This mode:

Inserts only unique property records (based on property_title)

Links dependent data correctly via foreign keys


🗃️ Schema Overview
The data is normalized into six relational tables:

Table	Description	Foreign Keys
property	Core property details	id (PK)
leads	Sales/lead-related information	property_id (FK)
valuation	Price, rent, zestimate, etc.	property_id (FK)
hoa	HOA-related flags	property_id (FK)
rehab	Repairs, condition, and rehab costs	property_id (FK)
taxes	Tax and assessment data	property_id (FK)

🔍 How to Verify the Load
Login to MySQL shell:

bash
Copy
Edit
docker exec -it mysql_ctn mysql -u root -p
Enter password: 6equj5_root

Then run:

sql
Copy
Edit
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
You should see 10000 rows per table if run after a fresh load.

✅ Features Implemented
✅ End-to-end ETL pipeline using pandas and mysql-connector-python

✅ Schema normalization using SQL DDL with primary and foreign key constraints

✅ Deduplication of property table to avoid duplicate loads

✅ Support for truncate-and-reload with --truncate CLI flag

✅ Clean and documented project structure

👨‍💻 Author
Prakash Kantumutchu


📄 License
This project is proprietary to HomeLLC for assessment purposes.

yaml
Copy
Edit


## Submission Guidelines

- Edit this README with your solutions and instructions for each section
- Place all scripts/code in their respective folders (`sql/`, `scripts/`, etc.)
- Ensure all steps are fully **reproducible** using your documentation

---

**Good luck! We look forward to your submission.**
