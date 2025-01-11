import os
import pandas as pd
from grad_rate_helpers import load_raw_grad_rate, clean_column_names

def main():
    """Process graduation rate data file."""
    try:
        print("Starting graduation rate data processing...")
        
        # Load raw data
        raw_df = load_raw_grad_rate('raw/gradrate_2022_23.csv')
        
        # Clean column names
        df = clean_column_names(raw_df)
        
        # Convert grad rate to numeric, handling any non-numeric values
        df['grad_rate_2023'] = pd.to_numeric(df['grad_rate_2023'], errors='coerce')
        
        # Debug: Print columns before saving
        print("\nColumns to be saved:")
        print(df.columns.tolist())
        
        # Create output directory if it doesn't exist
        os.makedirs('processed', exist_ok=True)
        
        # Save to parquet
        output_path = 'processed/grad_rate_2023.parquet'
        df.to_parquet(output_path, index=False)
        print(f"\nSaved processed data to {output_path}")
        
        # Verify saved data
        df_verify = pd.read_parquet(output_path)
        print("\nVerification - columns in saved file:")
        print(df_verify.columns.tolist())
        
        if df.equals(df_verify):
            print("✓ Verification successful")
        else:
            print("❌ Verification failed")
            
    except Exception as e:
        print(f"Error in processing: {str(e)}")
        raise

if __name__ == "__main__":
    main()