import streamlit as st
from dotenv import load_dotenv
from pages.welcome_page import welcome_page
from pages.form_page import candidate_form_page
from pages.interview_page import interview_page
from styles.custom_css import apply_custom_css
from utils.session_manager import initialize_session_state
from config import APP_TITLE, APP_ICON, LAYOUT, INITIAL_SIDEBAR_STATE

def main():
    """Main application function"""
    load_dotenv()
    
    # Page configuration
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR_STATE
    )
    
    initialize_session_state()
    apply_custom_css()
  


    # Navigation based on current page
    if st.session_state.page == 'welcome':
        welcome_page()
    elif st.session_state.page == 'form':
        candidate_form_page()
    elif st.session_state.page == 'interview':
        interview_page()

if __name__ == "__main__":
    main()