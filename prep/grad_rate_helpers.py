import pandas as pd

def load_raw_grad_rate(filepath):
    """Load raw graduation rate data from CSV file."""
    print(f"Attempting to load file from: {filepath}")
    try:
        df = pd.read_csv(filepath)
        print("Successfully loaded dataframe")
        print(f"Shape: {df.shape}")
        print("\nActual columns in file:")
        for i, col in enumerate(df.columns):
            print(f"{i}: {col}")
        return df
    except Exception as e:
        print(f"Error loading file: {str(e)}")
        raise

def clean_column_names(df):
    """Clean and standardize column names for graduation rate data."""
    column_mapping = {
        'UnitID': 'unit_id',
        'Institution Name': 'institution_name',
        'Graduation rate  total cohort (DRVGR2023)': 'grad_rate_2023'
    }
    
    # Drop any unnamed columns
    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
    if unnamed_cols:
        df = df.drop(unnamed_cols, axis=1)
    
    return df.rename(columns=column_mapping)