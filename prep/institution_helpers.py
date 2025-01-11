# File: prep/institution_helpers.py

import pandas as pd
import numpy as np

def load_raw_institutions(filepath):
    """
    Load the raw institutions data from CSV file.
    """
    print("Attempting to load file from:", filepath)  # Debug print
    try:
        # Specify dtype for ope_id to prevent numeric conversion
        dtype_specs = {
            'Office of Postsecondary Education (OPE) ID Number (HD2023)': str
        }
        df = pd.read_csv(filepath, dtype=dtype_specs)
        print("Successfully loaded dataframe")  # Debug print
        print("Shape:", df.shape)  # Debug print
        return df
    except Exception as e:
        print(f"Error loading file: {str(e)}")  # Debug print
        raise

def clean_column_names(df):
    """
    Clean and standardize column names.
    
    Args:
        df (pd.DataFrame): Raw DataFrame with original column names
        
    Returns:
        pd.DataFrame: DataFrame with cleaned column names
    """
    column_mapping = {
        'UnitID': 'unit_id',
        'Institution Name': 'institution_name',
        'State abbreviation (HD2023)': 'state',
        'City location of institution (HD2023)': 'city',
        'Control of institution (HD2023)': 'control',
        'Sector of institution (HD2023)': 'sector',
        'Level of institution (HD2023)': 'level',
        'Degree-granting status (HD2023)': 'degree_granting',
        'Postsecondary and Title IV institution indicator (HD2023)': 'title_iv',
        'Office of Postsecondary Education (OPE) ID Number (HD2023)': 'ope_id'
    }
    
    return df[column_mapping.keys()].rename(columns=column_mapping)

def clean_string_columns(df):
    """
    Clean string columns by removing whitespace.
    
    Args:
        df (pd.DataFrame): DataFrame with string columns
        
    Returns:
        pd.DataFrame: DataFrame with cleaned string columns
    """
    string_columns = ['institution_name', 'state', 'city']
    for col in string_columns:
        df[col] = df[col].str.strip()
    return df

def map_control(df):
    """
    Map the control of institution values to their corresponding categories.
    
    Source: IPEDS Data Dictionary
    Control of institution (HD2023)
    Values represent:
    1 = Public
    2 = Private not-for-profit
    3 = Private for-profit
    -3 = Not available
    
    Args:
        df (pd.DataFrame): DataFrame containing 'control' column
        
    Returns:
        pd.DataFrame: DataFrame with mapped control values
    """
    control_mapping = {
        1: 'Public',
        2: 'Private not-for-profit',
        3: 'Private for-profit',
        -3: 'Not available'
    }
    
    df['control'] = df['control'].map(control_mapping)
    
    # Log the distribution of values
    print("\nDistribution of institution control types:")
    print(df['control'].value_counts(dropna=False))
    
    return df

def map_sector(df):
    """
    Map the sector of institution values to their corresponding categories.
    
    Source: IPEDS Data Dictionary
    Sector of institution (HD2023)
    Values represent:
    0 = Administrative Unit
    1 = Public, 4-year or above
    2 = Private not-for-profit, 4-year or above
    3 = Private for-profit, 4-year or above
    4 = Public, 2-year
    5 = Private not-for-profit, 2-year
    6 = Private for-profit, 2-year
    7 = Public, less-than 2-year
    8 = Private not-for-profit, less-than 2-year
    9 = Private for-profit, less-than 2-year
    99 = Sector unknown (not active)
    
    Args:
        df (pd.DataFrame): DataFrame containing 'sector' column
        
    Returns:
        pd.DataFrame: DataFrame with mapped sector values
    """
    sector_mapping = {
        0: 'Administrative Unit',
        1: 'Public, 4-year or above',
        2: 'Private not-for-profit, 4-year or above',
        3: 'Private for-profit, 4-year or above',
        4: 'Public, 2-year',
        5: 'Private not-for-profit, 2-year',
        6: 'Private for-profit, 2-year',
        7: 'Public, less-than 2-year',
        8: 'Private not-for-profit, less-than 2-year',
        9: 'Private for-profit, less-than 2-year',
        99: 'Sector unknown (not active)'
    }
    
    df['sector'] = df['sector'].map(sector_mapping)
    
    # Log the distribution of values
    print("\nDistribution of institution sectors:")
    print(df['sector'].value_counts(dropna=False))
    
    return df

def map_level(df):
    """
    Map the level of institution values to their corresponding categories.
    
    Source: IPEDS Data Dictionary
    Level of institution (HD2023)
    Values represent:
    1 = Four or more years
    2 = At least 2 but less than 4 years
    3 = Less than 2 years (below associate)
    -3 = Not available
    
    Args:
        df (pd.DataFrame): DataFrame containing 'level' column
        
    Returns:
        pd.DataFrame: DataFrame with mapped level values
    """
    level_mapping = {
        1: 'Four or more years',
        2: 'At least 2 but less than 4 years',
        3: 'Less than 2 years',
        -3: 'Not available'
    }
    
    df['level'] = df['level'].map(level_mapping)
    
    # Log the distribution of values
    print("\nDistribution of institution levels:")
    print(df['level'].value_counts(dropna=False))
    
    return df

def map_degree_granting(df):
    """
    Map the degree-granting status values to their corresponding categories.
    
    Source: IPEDS Data Dictionary
    Degree-granting status (HD2023)
    Values represent:
    1 = Degree-granting
    2 = Nondegree-granting, primarily postsecondary
    -3 = Not available
    
    Args:
        df (pd.DataFrame): DataFrame containing 'degree_granting' column
        
    Returns:
        pd.DataFrame: DataFrame with mapped degree-granting status values
    """
    degree_mapping = {
        1: 'Degree-granting',
        2: 'Nondegree-granting',
        -3: 'Not available'
    }
    
    df['degree_granting'] = df['degree_granting'].map(degree_mapping)
    
    # Log the distribution of values
    print("\nDistribution of degree-granting status:")
    print(df['degree_granting'].value_counts(dropna=False))
    
    return df

def map_title_iv(df):
    """
    Map the Title IV institution indicator values to their corresponding categories.
    
    Source: IPEDS Data Dictionary
    Postsecondary and Title IV institution indicator (HD2023)
    Values represent:
    1 = Title IV postsecondary institution
    2 = Non-Title IV postsecondary institution
    3 = Title IV NOT primarily postsecondary institution
    4 = Non-Title IV NOT primarily postsecondary institution
    5 = Title IV postsecondary institution that is NOT open to the public
    6 = Non-Title IV postsecondary institution that is NOT open to the public
    9 = Institution is not active in current universe
    
    Args:
        df (pd.DataFrame): DataFrame containing 'title_iv' column
        
    Returns:
        pd.DataFrame: DataFrame with mapped Title IV status values
    """
    title_iv_mapping = {
        1: 'Title IV postsecondary',
        2: 'Non-Title IV postsecondary',
        3: 'Title IV not primarily postsecondary',
        4: 'Non-Title IV not primarily postsecondary',
        5: 'Title IV postsecondary (not public)',
        6: 'Non-Title IV postsecondary (not public)',
        9: 'Not active'
    }
    
    df['title_iv'] = df['title_iv'].map(title_iv_mapping)
    
    # Log the distribution of values
    print("\nDistribution of Title IV status:")
    print(df['title_iv'].value_counts(dropna=False))
    
    return df

def validate_ope_id(df):
    """
    Validate and clean the OPE ID field.
    
    Source: IPEDS Data Dictionary
    Office of Postsecondary Education (OPE) ID Number (HD2023)
    Format: 6-digit number followed by a 2-digit suffix
    Used by the U.S. Department of Education's Office of Postsecondary Education (OPE)
    to identify schools with Program Participation Agreements (PPA)
    
    Args:
        df (pd.DataFrame): DataFrame containing 'ope_id' column
        
    Returns:
        pd.DataFrame: DataFrame with validated OPE ID
    """
    # Convert to string if not already
    df['ope_id'] = df['ope_id'].astype(str)
    
    # Check format
    valid_format = df['ope_id'].str.match(r'^\d{7,8}$')
    
    # Log validation results
    print("\nOPE ID Validation:")
    print(f"Total records: {len(df)}")
    print(f"Valid format: {valid_format.sum()}")
    print(f"Invalid format: {(~valid_format).sum()}")
    
    if (~valid_format).any():
        print("\nSample of invalid OPE IDs:")
        print(df[~valid_format]['ope_id'].head())
    
    return df