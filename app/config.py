import streamlit as st
import pandas as pd
import os

# Constants
YEAR_OPTIONS = {
    "2022-23": "2223",
    "2021-22": "2122",
    "2020-21": "2021",
    "2019-20": "2020",
    "2018-19": "2019",
    "2017-18": "2018",
    "2016-17": "2017",
    "2015-16": "2016",
    "2014-15": "2015",
    "2013-14": "2014",
    "2012-13": "2013",
    "2011-12": "2012",
    "2010-11": "2011",
    "2009-10": "2010",
    "2008-09": "2009"
}

@st.cache_data
def load_data(year):
    """Load and cache the financial aid and institutions data"""
    try:
        # Going up from app directory to main directory
        current_dir = os.path.dirname(os.path.dirname(__file__))
        
        # Load financial aid data
        finaid_path = os.path.join(current_dir, 'processed', f'financial_aid_{year}.parquet')
        df_finaid = pd.read_parquet(finaid_path)
        
        # Drop institution_name from financial aid data if it exists
        if 'institution_name' in df_finaid.columns:
            df_finaid = df_finaid.drop('institution_name', axis=1)
        
        # Load institutions data
        inst_path = os.path.join(current_dir, 'processed', 'institutions.parquet')
        df_inst = pd.read_parquet(inst_path)
        
        # Load graduation rate data
        grad_path = os.path.join(current_dir, 'processed', 'grad_rate_2023.parquet')
        if os.path.exists(grad_path):
            df_grad = pd.read_parquet(grad_path)
            # Drop institution_name if it exists
            if 'institution_name' in df_grad.columns:
                df_grad = df_grad.drop('institution_name', axis=1)
        else:
            df_grad = None
        
        # Merge the datasets
        df = df_finaid.merge(
            df_inst[['unit_id', 'institution_name', 'state', 'sector', 
                     'degree_granting', 'control', 'level']], 
            on='unit_id', 
            how='left'
        )
        
        # Add graduation rate if available
        if df_grad is not None:
            df = df.merge(df_grad[['unit_id', 'grad_rate_2023']], 
                         on='unit_id', how='left')
        
        return df
        
    except Exception as e:
        print(f"Error loading data for year {year}:")
        print(f"Error message: {str(e)}")
        raise

def format_value(value, type='currency'):
    """Format values for display without decimals"""
    if pd.isnull(value):
        return ""
    
    if type == 'currency':
        return f"${int(value):,}"
    elif type == 'number':
        return f"{int(value):,}"
    elif type == 'percentage':
        return f"{int(value)}%" if pd.notnull(value) else ""
    return value

@st.cache_data
def get_sector_options(df):
    """Get unique sector values for filtering, excluding Administrative Unit"""
    sectors = sorted([sector for sector in df['sector'].unique() 
                     if sector != 'Administrative Unit'])
    return ['All Sectors'] + sectors