import streamlit as st

def show():
    """Display the home page content"""
    st.title("IPEDS Financial Aid Analysis")
    
    st.markdown("""
    This dashboard provides comprehensive analysis of financial aid data from the Integrated 
    Postsecondary Education Data System (IPEDS) across U.S. higher education institutions.

    ### Available Analyses

    Use the sidebar to navigate to different analyses:

    * **Pell Grants**: Analyze distribution of Federal Pell Grants across institutions
    * **Federal Loans**: Examine Federal student loan patterns
    * **Total Financial Aid**: Compare total financial aid packages

    ### Data Coverage

    * Academic Years: 2020-21 to 2022-23
    * Metrics Include:
        * Total undergraduate enrollment
        * Number of aid recipients
        * Total and average aid amounts
        * Percentage of students receiving aid

    ### Getting Started

    1. Select an analysis type from the sidebar
    2. Choose the academic year of interest
    3. Adjust the number of institutions to display
    """)

    # Footer
    st.markdown("---")
    st.markdown("Data Source: IPEDS Student Financial Aid (SFA) component")