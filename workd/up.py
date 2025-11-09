from sqlalchemy import create_engine
import pandas as pd

# --- RDS CONFIGURATION ---
RDS_USERNAME = "admin"
RDS_PASSWORD = "Zvg3NRkRiLkX6qlub6Mc"
RDS_HOSTNAME = "database-1.cxkucyeociny.ap-south-1.rds.amazonaws.com"
RDS_PORT = 3306
RDS_DB_NAME = "healthcare"

# --- EXCEL CONFIGURATION ---
EXCEL_PATH = "/home/ec2-user/AWS_Cloud/data/patient_samples/patients_data.xlsx"  # change path if needed

# --- CREATE SQLALCHEMY ENGINE ---
engine = create_engine(
    "mysql+pymysql://uploader:UploadPass123!@database-1.cxkucyeociny.ap-south-1.rds.amazonaws.com:3306/healthcare"
)


# --- LOAD EXCEL ---
print("📂 Reading Excel file...")
all_sheets = pd.read_excel(EXCEL_PATH, sheet_name=None)
print(f"Found {len(all_sheets)} sheets → {list(all_sheets.keys())}")

# --- UPLOAD EACH SHEET TO RDS ---
for sheet_name, df in all_sheets.items():
    print(f"➡ Uploading sheet '{sheet_name}' ({len(df)} rows)...")
    # Clean column names for SQL compatibility
    df.columns = [str(c).strip().replace(" ", "_").replace("-", "_") for c in df.columns]

    try:
        df.to_sql(
            name=sheet_name.lower(),    # table name = sheet name (lowercased)
            con=engine,
            index=False,
            if_exists='replace',        # replace existing tables (use 'append' if needed)
            chunksize=1000
        )
        print(f"✅ Uploaded '{sheet_name}' successfully.")
    except Exception as e:
        print(f"❌ Failed on sheet '{sheet_name}': {e}")

print("\n🎯 All sheets uploaded successfully to RDS database 'healthcare'.")
