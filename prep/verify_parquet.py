import pandas as pd
import argparse
import os

def verify_parquet_file(filepath):
    """
    Verify a parquet file contains expected financial aid data structure.
    
    Args:
        filepath (str): Path to the parquet file to verify
    """
    try:
        print(f"\nVerifying parquet file: {filepath}")
        print("-" * 50)
        
        # Check file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Load the parquet file
        df = pd.read_parquet(filepath)
        
        # Check required columns
        required_columns = {
            'unit_id': 'Institution identifier',
            'total_undergrad': 'Total undergraduate enrollment',
            'total_pell_amount': 'Total Pell grant amount',
            'total_loan_amount': 'Total federal loan amount'
        }
        
        missing_columns = []
        for col, description in required_columns.items():
            if col not in df.columns:
                missing_columns.append(f"{col} ({description})")
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Print basic statistics
        print("\nFile Statistics:")
        print(f"Number of rows: {len(df):,}")
        print(f"Number of columns: {len(df.columns)}")
        
        # Check for null values in key columns
        print("\nNull Value Check:")
        for col in required_columns:
            null_count = df[col].isnull().sum()
            print(f"{col}: {null_count:,} null values ({(null_count/len(df)*100):.1f}%)")
        
        # Value range checks
        print("\nValue Range Checks:")
        if 'total_undergrad' in df.columns:
            print(f"Total undergraduate range: {df['total_undergrad'].min():,} to {df['total_undergrad'].max():,}")
        if 'total_pell_amount' in df.columns:
            print(f"Pell amount range: ${df['total_pell_amount'].min():,.2f} to ${df['total_pell_amount'].max():,.2f}")
        if 'total_loan_amount' in df.columns:
            print(f"Loan amount range: ${df['total_loan_amount'].min():,.2f} to ${df['total_loan_amount'].max():,.2f}")
        
        print("\nAll columns present:")
        for col in sorted(df.columns):
            print(f"- {col}")
        
        print("\n✓ Verification completed successfully")
        
    except Exception as e:
        print(f"\n❌ Verification failed: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Verify IPEDS financial aid parquet file.')
    parser.add_argument('filepath', help='Path to parquet file (e.g., processed/financial_aid_2018.parquet)')
    
    args = parser.parse_args()
    verify_parquet_file(args.filepath)

if __name__ == "__main__":
    main()