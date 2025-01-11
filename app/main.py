import streamlit as st
from views import home, pell_grants, federal_loans, total_aid, institution_profile, hist_trends

# Configure page settings
st.set_page_config(
    page_title="IPEDS Financial Aid Analysis",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Sidebar navigation
st.sidebar.title("Navigation")

# Navigation selectbox
pages = {
    'Home': 'home',
    'Institution Profile': 'institution_profile',
    'Pell Grant Analysis': 'pell_grants',
    'Federal Loan Analysis': 'federal_loans',
    'Total Aid Analysis': 'total_aid',
    'Historical Trends': 'hist_trends'
}

selected_page = st.sidebar.selectbox(
    "Select Analysis",
    list(pages.keys()),
    index=list(pages.values()).index(st.session_state.current_page),
    key='page_selection'
)

# Update current page based on selection
if pages[selected_page] != st.session_state.current_page:
    # Clear any cached data when changing pages
    for key in list(st.session_state.keys()):
        if key != 'page_selection':
            del st.session_state[key]
    st.session_state.current_page = pages[selected_page]
    st.rerun()

# Display the selected page
if st.session_state.current_page == 'home':
    home.show()
elif st.session_state.current_page == 'institution_profile':
    institution_profile.show()
elif st.session_state.current_page == 'pell_grants':
    pell_grants.show()
elif st.session_state.current_page == 'federal_loans':
    federal_loans.show()
elif st.session_state.current_page == 'total_aid':
    total_aid.show()
elif st.session_state.current_page == 'hist_trends':
    hist_trends.show()