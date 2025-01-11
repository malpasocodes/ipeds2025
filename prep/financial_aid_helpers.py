import pandas as pd
import numpy as np

def load_raw_financial_aid(filepath):
    """
    Load raw financial aid data from CSV file.
    """
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

def clean_column_names(df, year):
    """
    Clean and standardize column names using column positions.
    
    Args:
        df (pd.DataFrame): Raw DataFrame
        year (str): Academic year identifier (not used in this approach but kept for compatibility)
    """
    # Drop any unnamed columns
    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
    if unnamed_cols:
        df = df.drop(unnamed_cols, axis=1)
    
    # Define new column names based on position
    new_columns = {
        0: 'unit_id',                  # UnitID
        1: 'institution_name',         # Institution Name
        2: 'total_undergrad',          # Total undergraduates
        3: 'num_pell_grant',          # Number awarded Pell grants
        4: 'pct_pell_grant',          # Percent awarded Pell grants
        5: 'total_pell_amount',       # Total Pell grant amount
        6: 'avg_pell_amount',         # Average Pell grant amount
        7: 'num_fed_loan',            # Number awarded federal loans
        8: 'pct_fed_loan',            # Percent awarded federal loans
        9: 'total_loan_amount',       # Total federal loan amount
        10: 'avg_loan_amount'         # Average federal loan amount
    }
    
    # Create list of column names in order
    columns = [new_columns[i] for i in range(len(df.columns)) if i in new_columns]
    
    # Rename columns
    df.columns = columns
    
    print("\nMapped columns:")
    for old, new in zip(df.columns, columns):
        print(f"{old} -> {new}")
    
    return df