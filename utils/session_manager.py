import streamlit as st

def initialize_session_state():
    """Initialize session state variable"""
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'interview_started' not in st.session_state:
        st.session_state.interview_started = False
    if 'interview_completed' not in st.session_state:
        st.session_state.interview_completed = False
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'waiting_for_answer' not in st.session_state:
        st.session_state.waiting_for_answer = False
    if 'questions_generated' not in st.session_state:
        st.session_state.questions_generated = False