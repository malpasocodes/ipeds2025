import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import load_data, YEAR_OPTIONS, format_value

def create_trend_plot(data_df, aid_type):
    """Create line plot showing historical trends"""
    
    title_mapping = {
        'Pell': 'Pell Grant',
        'Federal': 'Federal Loan',
        'Total': 'Total Financial Aid'
    }
    
    value_col = ('total_pell_amount' if aid_type == 'Pell' else 
                 'total_loan_amount' if aid_type == 'Federal' else 
                 'total_aid')
    
    # Create figure
    fig = go.Figure()

    # Add a trace for each institution
    for institution in data_df['institution_name'].unique():
        inst_data = data_df[data_df['institution_name'] == institution]
        
        # Ensure data is sorted by year
        inst_data = inst_data.sort_values('year')
        
        fig.add_trace(go.Scatter(
            x=inst_data['year'],
            y=inst_data[value_col],
            name=institution,
            mode='lines+markers'
        ))

    # Update layout
    fig.update_layout(
        title=f'Historical {title_mapping[aid_type]} Trends',
        xaxis_title='Academic Year',
        yaxis_title=f'Total {title_mapping[aid_type]} Amount ($)',
        height=600,
        yaxis_tickformat='$,.0f',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            itemsizing='constant'
        ),
        hovermode='x unified',
        xaxis=dict(
            type='category',
            categoryorder='array',
            categoryarray=sorted(data_df['year'].unique())
        )
    )

    return fig

def get_top_institutions(df, aid_type, n=10):
    """Get top N institutions based on aid type"""
    if aid_type == 'Pell':
        return df.nlargest(n, 'total_pell_amount')['institution_name'].unique()
    elif aid_type == 'Federal':
        return df.nlargest(n, 'total_loan_amount')['institution_name'].unique()
    else:  # Total
        df['total_aid'] = df['total_pell_amount'] + df['total_loan_amount']
        return df.nlargest(n, 'total_aid')['institution_name'].unique()

def show():
    """Display the Historical Trends analysis page"""
    st.title("Historical Trends Analysis")

    try:
        # Analysis type selector
        aid_type = st.selectbox(
            "Select Aid Type",
            ['Pell', 'Federal', 'Total']
        )
        
        # Number of institutions slider
        n_institutions = st.slider(
            "Number of Institutions",
            min_value=10,
            max_value=50,
            value=10,
            step=5
        )
        
        # Load data for all years
        all_years_data = []
        for display_year, year_code in reversed(YEAR_OPTIONS.items()):  # Reverse the order
            df = load_data(year_code)
            
            # Ensure numeric type for calculations
            df['total_pell_amount'] = pd.to_numeric(df['total_pell_amount'], errors='coerce')
            df['total_loan_amount'] = pd.to_numeric(df['total_loan_amount'], errors='coerce')
            
            # Calculate total aid if needed
            if aid_type == 'Total':
                df['total_aid'] = df['total_pell_amount'] + df['total_loan_amount']
            
            df['year'] = display_year
            all_years_data.append(df)
        
        # Combine all years
        combined_df = pd.concat(all_years_data)
        
        # Get top N institutions based on most recent year
        most_recent_df = all_years_data[-1]  # Last item now corresponds to most recent year
        top_institutions = get_top_institutions(most_recent_df, aid_type, n_institutions)
        
        # Filter data for top institutions
        trend_data = combined_df[combined_df['institution_name'].isin(top_institutions)].copy()
        
        # Create and display trend plot
        st.plotly_chart(create_trend_plot(trend_data, aid_type), use_container_width=True)
        
        # Display data table
        st.subheader("Historical Data")
        
        # Create aggregation for historical data table
        value_col = ('total_pell_amount' if aid_type == 'Pell' else 
                    'total_loan_amount' if aid_type == 'Federal' else 
                    'total_aid')
        
        # Group by institution and calculate aggregate
        agg_df = trend_data.groupby(['institution_name', 'state', 'sector'])[value_col].sum().reset_index()
        
        # Sort by aggregate amount descending
        display_df = agg_df.nlargest(n_institutions, value_col)
        
        # Format columns
        formatted_df = display_df.copy()
        formatted_df[value_col] = formatted_df[value_col].apply(
            lambda x: format_value(x, 'currency'))
        
        # Rename columns
        column_names = {
            'institution_name': 'Institution',
            'state': 'State',
            'sector': 'Sector',
            'total_pell_amount': 'Total Pell Amount (Aggregate)',
            'total_loan_amount': 'Total Loan Amount (Aggregate)',
            'total_aid': 'Total Aid Amount (Aggregate)'
        }
        formatted_df.columns = [column_names.get(col, col) for col in formatted_df.columns]
        
        # Display table
        st.dataframe(formatted_df, use_container_width=True)
        
        # Add download button for CSV
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name=f"historical_data_{aid_type.lower()}.csv",
            mime='text/csv'
        )
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        if 'combined_df' in locals():
            st.write("Available columns:", combined_df.columns.tolist())
            
        # For debugging data issues
        st.write("Debug Information:")
        st.write("Number of institutions:", len(trend_data['institution_name'].unique()) if 'trend_data' in locals() else "No trend data")
        if 'trend_data' in locals():
            st.write("Sample of trend data:")
            st.write(trend_data.head())