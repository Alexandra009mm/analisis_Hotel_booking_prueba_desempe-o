import pandas as pd


def get_data(path: str):
    """Read the CSV file and return it as a DataFrame."""
    try:
        df = pd.read_csv(path, encoding="utf-8-sig") 
        print(f"[EXTRACT] read file: {path}")
        print(f"  - rows: {len(df):,}")
        print(f"  - columns: {len(df.columns)}")
        return df
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}")
        raise
    except Exception as e:
        print(f"[ERROR] problems reading {path}: {e}")
        raise