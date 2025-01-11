# File: prep/prepare_institutions.py

import os
import pandas as pd
from institution_helpers import (
    load_raw_institutions, 
    clean_column_names, 
    clean_string_columns,
    map_control,
    map_sector,
    map_level,
    map_degree_granting,
    map_title_iv,
    validate_ope_id
)

def main():
    """
    Main function to execute the preparation process.
    """
    print("Starting main function")  # Debug print
    try:
        # Print current working directory
        print("Current working directory:", os.getcwd())
        
        # Check if file exists
        file_path = 'raw/institutions.csv'
        if os.path.exists(file_path):
            print(f"Found file at: {file_path}")
            print(f"File size: {os.path.getsize(file_path)} bytes")
        else:
            print(f"File not found at: {file_path}")
            print("Absolute path would be:", os.path.abspath(file_path))
            print("Please ensure institutions.csv is in the 'raw' directory")
            return
            
        print("About to load raw data")  # Debug print
        # Step 1: Load raw data
        raw_df = load_raw_institutions('raw/institutions.csv')
        print(f"Loaded {len(raw_df)} raw records")
        print("\nInitial columns:")
        print(raw_df.columns.tolist())
        
        # Step 2: Clean column names
        df = clean_column_names(raw_df)
        
        # Step 3: Clean string columns
        df = clean_string_columns(df)
        
        # Step 4: Map categorical values
        df = map_control(df)
        df = map_sector(df)
        df = map_level(df)
        df = map_degree_granting(df)
        df = map_title_iv(df)
        
        # Step 5: Validate OPE ID
        df = validate_ope_id(df)
        
        # Basic info about the current state of dataset
        print("\nCurrent Dataset Info:")
        print("-" * 50)
        print(df.info())

        output_path = 'processed/institutions.parquet'
        df.to_parquet(output_path, index=False)
        print(f"\nSaved data to {output_path}")

         # Verification step
        print("\nVerifying saved file...")
        df_verify = pd.read_parquet(output_path)
        print("\nVerification Info:")
        print("-" * 50)
        print(f"Number of rows: {len(df_verify)}")
        print(f"Number of columns: {len(df_verify.columns)}")
        print("\nColumn names:")
        for col in df_verify.columns:
            print(f"- {col}")
            
        # Verify the data matches
        if df.equals(df_verify):
            print("\n✓ Verification successful: Saved data matches original")
        else:
            print("\n❌ Warning: Saved data differs from original")
            
        # Show sample of verified data
        print("\nFirst few rows of verified data:")
        print("-" * 50)
        print(df_verify.head())

        
    except Exception as e:
        print(f"Error in main: {str(e)}")  # Debug print
        raise

if __name__ == "__main__":
    print("Script starting")  # Debug print
    main()
    print("Script finished")  # Debug print