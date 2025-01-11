import streamlit as st
import pandas as pd
import plotly.express as px
from config import load_data, YEAR_OPTIONS, format_value, get_sector_options

def create_scatter_plot(df):
    """Create scatter plot of graduation rate vs total loan amount"""
    fig = px.scatter(
        df,
        x='grad_rate_2023',
        y='total_loan_amount',
        color='sector',
        size='total_undergrad',
        hover_name='institution_name',
        hover_data={
            'grad_rate_2023': ':.1f',
            'total_loan_amount': ':$,.0f',
            'total_undergrad': ':,',
            'sector': True
        },
        title='Graduation Rate vs Total Federal Loan Amount by Institution',
        labels={
            'grad_rate_2023': 'Graduation Rate (%)',
            'total_loan_amount': 'Total Federal Loan Amount ($)',
            'sector': 'Sector',
            'total_undergrad': 'Total Undergraduate'
        }
    )

    # Update layout
    fig.update_layout(
        height=600,
        yaxis_tickformat='$,.0f',
        xaxis_tickformat='.0f',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )

    return fig

def show():
    """Display the Federal Loans analysis page"""
    st.title("Federal Loan Analysis")

    try:
        # Analysis controls
        st.sidebar.header("Analysis Options")
        
        # Year selector
        selected_year = st.sidebar.selectbox(
            "Select Academic Year",
            list(YEAR_OPTIONS.keys())
        )
        
        # Load data first to get filter options
        df = load_data(YEAR_OPTIONS[selected_year])
        
        # Institution type filter
        selected_sector = st.sidebar.selectbox(
            "Institution Sector",
            get_sector_options(df)
        )
        
        # Number of institutions slider
        n_institutions = st.sidebar.slider(
            "Number of Institutions",
            min_value=10,
            max_value=250,
            value=10,
            step=10
        )
        
        # Apply filters
        if selected_sector != 'All Sectors':
            df = df[df['sector'] == selected_sector]
        
        # Ensure numeric types
        df['total_loan_amount'] = pd.to_numeric(df['total_loan_amount'], errors='coerce')
        df['grad_rate_2023'] = pd.to_numeric(df['grad_rate_2023'], errors='coerce')
        df['total_undergrad'] = pd.to_numeric(df['total_undergrad'], errors='coerce')
        
        # Sort by total loan amount in descending order
        sorted_df = df.nlargest(n_institutions, 'total_loan_amount')
        
        # Create scatter plot with top N institutions
        plot_df = sorted_df.dropna(subset=['grad_rate_2023', 'total_loan_amount', 'total_undergrad'])
        st.plotly_chart(create_scatter_plot(plot_df), use_container_width=True)
        
        # Prepare display dataframe
        display_df = sorted_df[['institution_name', 'sector', 'state', 
                               'total_undergrad', 'total_loan_amount', 'grad_rate_2023']]
        
        # Format columns
        formatted_df = display_df.copy()
        formatted_df['total_loan_amount'] = formatted_df['total_loan_amount'].apply(
            lambda x: format_value(x, 'currency'))
        formatted_df['total_undergrad'] = formatted_df['total_undergrad'].apply(
            lambda x: format_value(x, 'number'))
        formatted_df['grad_rate_2023'] = formatted_df['grad_rate_2023'].apply(
            lambda x: format_value(x, 'percentage'))
        
        # Rename columns for display
        formatted_df.columns = ['Institution', 'Sector', 'State', 
                              'Total Undergraduate', 'Total Loan Amount', 'Grad Rate 2023']
        
        # Display results
        st.write(f"Showing Federal Loan data for Academic Year {selected_year}")
        st.dataframe(formatted_df, use_container_width=True)
        
        # Show summary statistics
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Summary Statistics")
        st.sidebar.markdown(f"Total Institutions: {len(formatted_df)}")
        total_loans = df['total_loan_amount'].sum()
        st.sidebar.markdown(f"Total Loan Amount: {format_value(total_loans, 'currency')}")
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        if 'df' in locals():
            st.write("Available columns:", df.columns.tolist())