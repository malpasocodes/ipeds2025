# File: prep/prepare_financial_aid.py

import os
import pandas as pd
from financial_aid_helpers import load_raw_financial_aid, clean_column_names

def process_single_year(input_file, year, output_dir='processed'):
    """
    Process a single year's financial aid data file.
    
    Args:
        input_file (str): Path to input CSV file
        year (str): Academic year identifier
        output_dir (str): Directory for processed output
    """
    try:
        print(f"\nProcessing data for year {year}")
        print("-" * 50)
        
        # Load raw data
        raw_df = load_raw_financial_aid(input_file)
        
        # Clean column names
        df = clean_column_names(raw_df, year)
        
        # Debug: Print columns before saving
        print("\nColumns to be saved:")
        print(df.columns.tolist())
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Create output filename
        output_path = os.path.join(output_dir, f'financial_aid_{year}.parquet')
        
        # Save processed data
        df.to_parquet(output_path, index=False)
        print(f"Saved processed data to {output_path}")
        
        # Verify saved data
        df_verify = pd.read_parquet(output_path)
        print("\nVerification - columns in saved file:")
        print(df_verify.columns.tolist())
        
        if df.equals(df_verify):
            print("✓ Verification successful")
        else:
            print("❌ Verification failed")
        
    except Exception as e:
        print(f"Error processing {year} data: {str(e)}")
        raise

def main():
    """
    Process all financial aid data files in the raw directory.
    """
    years_files = {
        '2223': 'raw/finaid_2022_23.csv',
        '2122': 'raw/finaid_2021_22.csv',
        '2021': 'raw/finaid_2020_21.csv',
        '2020': 'raw/finaid_2019_20.csv',
        '2019': 'raw/finaid_2018_19.csv'
    }
    
    print("Starting financial aid data processing...")
    print(f"Current working directory: {os.getcwd()}")
    
    # Process each year
    for year, filepath in years_files.items():
        if os.path.exists(filepath):
            process_single_year(filepath, year)
        else:
            print(f"Warning: File not found - {filepath}")
    
    print("\nProcessing complete.")

if __name__ == "__main__":
    main()