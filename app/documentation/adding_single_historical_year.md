# Adding a Single Historical Year to IPEDS Analysis

This document outlines the process for adding one historical year at a time to the IPEDS financial aid analysis application.

## Current State
Existing processed files (DO NOT MODIFY):
```
processed/
    ├── financial_aid_2223.parquet
    ├── financial_aid_2122.parquet
    ├── financial_aid_2021.parquet
    ├── financial_aid_2020.parquet
    └── financial_aid_2019.parquet
```

## Process Overview
1. Start with the most recent historical year first (2017-18)
2. Process one file at a time
3. Test thoroughly before proceeding to the next year

## Adding a Single Year

### 1. Place Raw Data File
Put the new CSV file in the raw directory using the consistent naming pattern:
```
raw/finaid_2017_18.csv    # Example for 2017-18 academic year
```

### 2. Create Single-Year Processing Script
Create a new file `prep/process_single_historical_year.py`:
```python
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
```

### 3. Process the File
Run the script for a single year:
```bash
python prep/process_single_historical_year.py raw/finaid_2017_18.csv 2018
```

### 4. Update config.py
After successful processing, add the new year to YEAR_OPTIONS in `app/config.py`:
```python
YEAR_OPTIONS = {
    "2022-23": "2223",
    "2021-22": "2122",
    "2020-21": "2021",
    "2019-20": "2020",
    "2018-19": "2019",
    "2017-18": "2018"  # newly added year
}
```

## Testing After Adding Year

1. Verify the new parquet file:
   - Check file exists in processed directory
   - Confirm file size is reasonable
   - Verify column names match expected format

2. Test in Streamlit app:
   - Start the app
   - Confirm new year appears in dropdown
   - Test data loading for new year
   - Verify visualizations work
   - Check all filters and calculations

3. Compare with existing years:
   - Check for data consistency
   - Verify column names match
   - Confirm calculations produce expected results

## Troubleshooting

If errors occur:
1. Check raw CSV file:
   - Column names match expected pattern
   - Data types are consistent
   - No unexpected formatting issues

2. Review error messages:
   - Note specific column causing issues
   - Check for data type mismatches
   - Verify year format is correct

3. If processing fails:
   - The script will not create a partial parquet file
   - Existing data remains untouched
   - Fix issues and retry processing

## Next Steps

After successful processing and testing:
1. Document any special handling required for the year
2. Note any column name variations
3. Update documentation with successful processing
4. Proceed to next historical year if needed

## Safety Features

The script includes several safety measures:
- Checks for existing parquet file before processing
- Verifies input file exists
- Validates processed data before saving
- Preserves existing parquet files
- Provides detailed error messages
- Allows easy rollback by not modifying existing files