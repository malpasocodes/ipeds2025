import os
import pandas as pd
import argparse
from financial_aid_helpers import load_raw_financial_aid, clean_column_names

def process_single_year(input_file, year, output_dir='processed'):
    """
    Process a single historical year's financial aid data file.
    
    Args:
        input_file (str): Path to input CSV file
        year (str): Academic year identifier (e.g., '2018' for 2017-18)
        output_dir (str): Directory for processed output
    """
    try:
        print(f"\nProcessing data for year {year}")
        print("-" * 50)
        
        # Check if output file already exists
        output_path = os.path.join(output_dir, f'financial_aid_{year}.parquet')
        if os.path.exists(output_path):
            raise ValueError(f"Output file already exists: {output_path}")
        
        # Load and process the data
        print(f"Loading file: {input_file}")
        raw_df = load_raw_financial_aid(input_file)
        
        # Clean column names
        df = clean_column_names(raw_df, year)
        
        # Debug: Print columns before saving
        print("\nColumns to be saved:")
        print(df.columns.tolist())
        
        # Create output filename
        os.makedirs(output_dir, exist_ok=True)
        
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
            raise ValueError("Verification failed: saved data does not match processed data")
            
    except Exception as e:
        print(f"Error processing {year} data: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Process a single historical year of IPEDS data.')
    parser.add_argument('filename', help='Input CSV filename (e.g., finaid_2017_18.csv)')
    parser.add_argument('year', help='Year identifier (e.g., 2018 for 2017-18)')
    
    args = parser.parse_args()
    
    # Ensure input file exists
    if not os.path.exists(args.filename):
        print(f"Error: Input file not found: {args.filename}")
        return
    
    process_single_year(args.filename, args.year)

if __name__ == "__main__":
    main()