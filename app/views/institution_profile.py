import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import load_data, YEAR_OPTIONS, format_value, get_sector_options

def create_trend_plot(df_list, years, institution):
    """Create a line plot showing financial aid trends"""
    # Create figure
    fig = go.Figure()

    # Prepare data for each type of aid
    pell_data = []
    loan_data = []
    aid_data = []
    years_list = []

    for year, year_data in zip(years, df_list):
        if len(year_data) > 0:
            inst_data = year_data.iloc[0]
            pell = pd.to_numeric(inst_data['total_pell_amount'], errors='coerce')
            loan = pd.to_numeric(inst_data['total_loan_amount'], errors='coerce')
            pell_data.append(pell)
            loan_data.append(loan)
            aid_data.append(pell + loan)
            years_list.append(year)

    # Add traces
    fig.add_trace(go.Scatter(
        x=years_list,
        y=pell_data,
        name='Pell Grants',
        line=dict(color='#2ecc71', width=2),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=years_list,
        y=loan_data,
        name='Federal Loans',
        line=dict(color='#e74c3c', width=2),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=years_list,
        y=aid_data,
        name='Total Aid',
        line=dict(color='#3498db', width=2),
        mode='lines+markers'
    ))

    # Update layout
    fig.update_layout(
        title=f'Financial Aid Trends: {institution}',
        xaxis_title='Academic Year',
        yaxis_title='Amount ($)',
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
            categoryarray=sorted(years_list)
        )
    )

    return fig

def show():
    """Display the Institution Profile page"""
    st.title("Institution Profile")

    try:
        # Load most recent year's data for institution selection
        most_recent_year = list(YEAR_OPTIONS.keys())[0]  # First year in the dict (2022-23)
        df = load_data(YEAR_OPTIONS[most_recent_year])
        
        # Sidebar filters
        st.sidebar.header("Select Institution")
        
        # Use get_sector_options for consistent sector filtering
        selected_sector = st.sidebar.selectbox(
            "Institution Sector",
            get_sector_options(df)
        )
        
        # Filter institutions based on selected sector
        if selected_sector == 'All Sectors':
            institutions_df = df[df['sector'] != 'Administrative Unit']
        else:
            institutions_df = df[df['sector'] == selected_sector]
        
        # Get sorted list of institutions for the selected sector
        institutions = sorted(institutions_df['institution_name'].unique())
        
        # Institution selector
        selected_institution = st.sidebar.selectbox(
            "Select Institution",
            institutions
        )
        
        # After institution is selected, load all years' data for this institution
        st.subheader(selected_institution)
        
        # Load data for all years
        years = list(YEAR_OPTIONS.keys())
        year_dfs = []
        
        for year in years:
            year_df = load_data(YEAR_OPTIONS[year])
            inst_data = year_df[year_df['institution_name'] == selected_institution]
            year_dfs.append(inst_data)
        
        # Create and display trend plot
        st.plotly_chart(create_trend_plot(year_dfs, years, selected_institution),
                       use_container_width=True)
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Institution Information", "Yearly Statistics", "Aggregate Totals"])
        
        with tab1:
            # Show institution information from most recent year
            most_recent_data = year_dfs[0]  # First in the list is most recent
            if len(most_recent_data) > 0:
                inst_data = most_recent_data.iloc[0]
                st.write(f"**State:** {inst_data['state']}")
                st.write(f"**Sector:** {inst_data['sector']}")
                st.write(f"**Control:** {inst_data['control']}")
                st.write(f"**Level:** {inst_data['level']}")
                st.write(f"**Degree-Granting Status:** {inst_data['degree_granting']}")
            else:
                st.write("No data available")
        
        with tab2:
            # Create a dataframe for yearly statistics
            yearly_data = []
            for year, year_data in zip(years, year_dfs):
                if len(year_data) > 0:
                    inst_data = year_data.iloc[0]
                    total_aid = inst_data['total_pell_amount'] + inst_data['total_loan_amount']
                    yearly_data.append({
                        'Academic Year': year,
                        'Total Pell Grant': inst_data['total_pell_amount'],
                        'Total Federal Loan': inst_data['total_loan_amount'],
                        'Total Financial Aid': total_aid
                    })
            
            if yearly_data:
                # Create DataFrame
                df_yearly = pd.DataFrame(yearly_data)
                
                # Create formatted version for display
                df_display = df_yearly.copy()
                df_display['Total Pell Grant'] = df_display['Total Pell Grant'].apply(
                    lambda x: format_value(x, 'currency'))
                df_display['Total Federal Loan'] = df_display['Total Federal Loan'].apply(
                    lambda x: format_value(x, 'currency'))
                df_display['Total Financial Aid'] = df_display['Total Financial Aid'].apply(
                    lambda x: format_value(x, 'currency'))
                
                # Display table
                st.dataframe(df_display, use_container_width=True)
                
                # Add download button for CSV
                csv = df_yearly.to_csv(index=False)
                st.download_button(
                    label="Download Data as CSV",
                    data=csv,
                    file_name=f"{selected_institution.replace('/', '_')}_yearly_statistics.csv",
                    mime='text/csv'
                )
            else:
                st.write("No data available")
        
        with tab3:
            # Create aggregation using the same yearly_data we used in tab2
            yearly_data = []
            for year, year_data in zip(years, year_dfs):
                if len(year_data) > 0:
                    inst_data = year_data.iloc[0]
                    yearly_data.append({
                        'Academic Year': year,
                        'total_pell_amount': inst_data['total_pell_amount'],
                        'total_loan_amount': inst_data['total_loan_amount']
                    })
            
            if yearly_data:
                df_agg = pd.DataFrame(yearly_data)
                total_pell = df_agg['total_pell_amount'].sum()
                total_loan = df_agg['total_loan_amount'].sum()
                total_aid = total_pell + total_loan
                
                st.markdown("### Aggregate Totals Across All Years")
                st.write(f"**Total Pell Grant Amount:** {format_value(total_pell, 'currency')}")
                st.write(f"**Total Federal Loan Amount:** {format_value(total_loan, 'currency')}")
                st.write(f"**Total Financial Aid:** {format_value(total_aid, 'currency')}")
            else:
                st.write("No data available")
                
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        if 'df' in locals():
            st.write("Available columns:", df.columns.tolist())