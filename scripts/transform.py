import pandas as pd
from typing import Tuple

BOOLEAN_MAP = {"Yes": True, "No": False, "Y": True, "N": False}

def _boolify(series: pd.Series) -> pd.Series:
    """Convert Yes/No or Y/N strings to boolean."""
    return series.map(BOOLEAN_MAP).astype("boolean")


def transform(df_raw: pd.DataFrame, field_config_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split raw DataFrame into cleaned DataFrames for each target table.

    Returns (property_df, reviewer_df, leads_df)
    """
    # Load field config mapping
    config_df = pd.read_excel(field_config_path, sheet_name=0)
    table_map = config_df.groupby("Target Table")[["Column Name"]].agg(list)["Column Name"].to_dict()

    # ---------------- Property ---------------- #
    property_cols = table_map.get("property", [])
    property_df = df_raw[property_cols].copy()

    # Rename to DB column names
    property_rename = {
        "Property_Title": "title",
        "Address": "address",
        "Street_Address": "street_address",
        "City": "city",
        "State": "state",
        "Zip": "zip_code",
        "Market": "market",
        "Flood": "flood",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Subdivision": "subdivision",
        "Taxes": "taxes",
        "Redfin_Value": "redfin_value",
        "HOA_Flag": "hoa_flag",
    }
    property_df = property_df.rename(columns=property_rename)
    # Clean types
    if "hoa_flag" in property_df.columns:
        property_df["hoa_flag"] = _boolify(property_df["hoa_flag"])
    property_df = property_df.drop_duplicates().reset_index(drop=True)

    # ---------------- Reviewers ---------------- #
    reviewer_cols = ["Final_Reviewer", "School_Average"]
    reviewer_df = (
        df_raw[reviewer_cols]
        .rename(columns={"Final_Reviewer": "name", "School_Average": "school_average"})
        .drop_duplicates()
        .reset_index(drop=True)
    )

    # ---------------- Leads ---------------- #
    leads_cols = table_map.get("Leads", [])
    leads_df = df_raw[leads_cols + reviewer_cols].copy()
    leads_rename = {
        "Reviewed_Status": "reviewed_status",
        "Most_Recent_Status": "most_recent_status",
        "Source": "source",
        "Occupancy": "occupancy",
        "Selling_Reason": "selling_reason",
        "Seller_Retained_Broker": "seller_retained_broker",
        "Final_Reviewer": "reviewer_name",  # will be resolved to reviewer_id in load.py
    }
    leads_df = leads_df.rename(columns=leads_rename)
    leads_df["occupancy"] = _boolify(leads_df["occupancy"])
    leads_df = leads_df.reset_index(drop=True)

    return property_df, reviewer_df, leads_df


if __name__ == "__main__":
    raw = pd.read_csv("../data/fake_data.csv")
    p_df, r_df, l_df = transform(raw, "../data/Field Config.xlsx")
    print("Property rows:", len(p_df))
    print("Reviewer rows:", len(r_df))
    print("Lead rows:", len(l_df))
