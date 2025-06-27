import mysql.connector
import pandas as pd
from typing import Tuple

# --- DB CONFIG --- #
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",  # match Docker creds
    "database": "homellc"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def insert_property_data(conn, property_df: pd.DataFrame) -> pd.DataFrame:
    cur = conn.cursor()
    insert_sql = """
    INSERT INTO property (title, address, street_address, city, state, zip_code, market, flood,
                          latitude, longitude, subdivision, taxes, redfin_value, hoa_flag)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for _, row in property_df.iterrows():
        cur.execute(insert_sql, tuple(row))
    conn.commit()
    cur.close()

    # Fetch back property_ids
    return pd.read_sql("SELECT * FROM property", conn)

def insert_reviewer_data(conn, reviewer_df: pd.DataFrame) -> pd.DataFrame:
    cur = conn.cursor()
    insert_sql = """
    INSERT INTO reviewers (name, school_average)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE school_average = VALUES(school_average)
    """
    for _, row in reviewer_df.iterrows():
        cur.execute(insert_sql, tuple(row))
    conn.commit()
    cur.close()

    return pd.read_sql("SELECT * FROM reviewers", conn)

def insert_leads_data(conn, leads_df: pd.DataFrame,
                      prop_ref: pd.DataFrame, reviewer_ref: pd.DataFrame):
    cur = conn.cursor()

    # Map property and reviewer
    leads_df = leads_df.merge(reviewer_ref, left_on="reviewer_name", right_on="name", how="left")
    leads_df = leads_df.merge(prop_ref, on=["title", "address"], how="left")

    insert_sql = """
    INSERT INTO leads (property_id, reviewer_id, reviewed_status, most_recent_status,
                       source, occupancy, selling_reason, seller_retained_broker)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    for _, row in leads_df.iterrows():
        cur.execute(insert_sql, (
            row["property_id"], row["reviewer_id"], row["reviewed_status"], row["most_recent_status"],
            row["source"], row["occupancy"], row["selling_reason"], row["seller_retained_broker"]
        ))
    conn.commit()
    cur.close()

if __name__ == "__main__":
    print("Use this module via run_etl.py")
