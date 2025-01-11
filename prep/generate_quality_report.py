# File: prep/generate_quality_report.py

import pandas as pd
import numpy as np
from datetime import datetime

def generate_quality_report(input_file):
    """
    Generate a data quality report for the institutions dataset
    """
    # Read the processed data
    df = pd.read_parquet(input_file)
    
    # Basic dimensions
    dimensions = {
        'rows': len(df),
        'columns': len(df.columns)
    }
    
    # Categorical distributions
    categorical_cols = ['control', 'sector', 'level', 'degree_granting', 'title_iv']
    distributions = {}
    for col in categorical_cols:
        distributions[col] = df[col].value_counts().to_dict()
    
    # Missing values
    missing = df.isnull().sum()
    missing = missing[missing > 0].to_dict()
    
    # State distribution
    state_dist = df['state'].value_counts().head().to_dict()
    
    # Generate the report
    print(f"# IPEDS Institutions Data Quality Report")
    print(f"Generated: {datetime.now().strftime('%B %d, %Y')}\n")
    
    print("## Data Dimensions")
    print(f"- Rows: {dimensions['rows']:,}")
    print(f"- Columns: {dimensions['columns']}\n")
    
    print("## Categorical Distributions\n")
    for col, dist in distributions.items():
        print(f"### {col.replace('_', ' ').title()}")
        for val, count in dist.items():
            print(f"- {val}: {count:,}")
        print()
    
    if missing:
        print("## Missing Values")
        for col, count in missing.items():
            print(f"- {col}: {count:,}")
        print()
    
    print("## Top 5 States by Number of Institutions")
    for state, count in state_dist.items():
        print(f"- {state}: {count:,}")

if __name__ == "__main__":
    generate_quality_report('processed/institutions.parquet')