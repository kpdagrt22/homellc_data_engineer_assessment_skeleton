import pandas as pd
import mysql.connector
import argparse

# --- CONFIG ---
CSV_PATH = "data/fake_data.csv"
FIELD_CONFIG_PATH = "data/Field Config.xlsx"

DB_CONFIG = {
    "host": "localhost",
    "user": "db_user",
    "password": "6equj5_db_user",
    "database": "home_db",
    "port": 3306
}

# --- SETUP ARGUMENT PARSER ---
parser = argparse.ArgumentParser()
parser.add_argument("--truncate", action="store_true", help="Truncate all target tables before insert")
args = parser.parse_args()

# --- LOAD DATA ---
df = pd.read_csv(CSV_PATH)
field_config = pd.read_excel(FIELD_CONFIG_PATH, sheet_name="Sheet1")

# --- CONNECT TO DB ---
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()
print("✅ Connected to DB")

# --- CLEAN COLUMN NAMES ---
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
field_config["Column Name"] = field_config["Column Name"].str.strip().str.lower().str.replace(" ", "_")
field_config["Target Table"] = field_config["Target Table"].str.strip().str.lower()

# Fix mismatches
df.rename(columns={
    'basementyesno': 'basement_yes_no'
}, inplace=True)

# --- BUILD TABLE MAP ---
table_map = field_config.groupby("Target Table")["Column Name"].apply(list).to_dict()
for table, cols in table_map.items():
    table_map[table] = [col for col in cols if col in df.columns]

# --- OPTIONAL TRUNCATION WITH FK CHECKS DISABLED ---
if args.truncate:
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    for tbl in ['leads', 'valuation', 'hoa', 'rehab', 'taxes', 'property']:
        cursor.execute(f"TRUNCATE TABLE {tbl};")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print("🧹 All target tables truncated (FK checks temporarily disabled).")

# --- INSERT HELPERS ---
def insert_and_get_ids(table_name, rows):
    ids = []
    for row in rows:
        # Deduplication for 'property'
        if table_name == "property":
            cursor.execute("SELECT id FROM property WHERE property_title = %s", (row['property_title'],))
            existing = cursor.fetchone()
            if existing:
                ids.append(existing[0])
                continue

        columns = ', '.join(row.keys())
        placeholders = ', '.join(['%s'] * len(row))
        values = list(row.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        try:
            cursor.execute(query, values)
            ids.append(cursor.lastrowid)
        except mysql.connector.Error as err:
            print(f"❌ Error inserting into {table_name}: {err}")
            print(f"Query: {query}")
            print(f"Values: {values}")
            exit(1)
    return ids

def insert_dependent(table, fk_name, ids):
    if table not in table_map:
        print(f"⚠️ Skipping '{table}' - no mapped columns found.")
        return
    subset = df[table_map[table]]
    subset = subset.where(pd.notnull(subset), None)
    records = subset.to_dict(orient='records')

    for i, row in enumerate(records):
        row[fk_name] = ids[i]
        columns = ', '.join(row.keys())
        placeholders = ', '.join(['%s'] * len(row))
        values = list(row.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        try:
            cursor.execute(query, values)
        except mysql.connector.Error as err:
            print(f"❌ Error inserting into {table}: {err}")
            print(f"Query: {query}")
            print(f"Values: {values}")
            exit(1)
    print(f"✅ Inserted {len(records)} rows into '{table}'")

# --- INSERT PROPERTY + CHILD TABLES ---
property_data = df[table_map['property']]
property_data = property_data.where(pd.notnull(property_data), None)
property_rows = property_data.to_dict(orient='records')
property_ids = insert_and_get_ids("property", property_rows)
print(f"✅ Inserted {len(property_ids)} unique rows into 'property'")

child_tables = ['leads', 'valuation', 'hoa', 'rehab', 'taxes']
for table in child_tables:
    insert_dependent(table, 'property_id', property_ids)

# --- COMMIT & CLOSE ---
conn.commit()
cursor.close()
conn.close()
print("✅ ETL completed and DB connection closed")
