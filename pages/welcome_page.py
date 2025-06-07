import streamlit as st

def welcome_page():
    """Welcome page with introduction"""
    st.markdown("""
    <div class="main-header">
        <h1>Welcome to TalentScout</h1>
        <h3>AI-Powered Hiring Assistant</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="welcome-card">
            <h2>🤖 About Our AI Hiring Assistant</h2>
            <p><strong>Purpose:</strong> I'm here to conduct your initial technical screening for technology positions at TalentScout.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### What to Expect:")
        st.markdown("""
        - **Information Collection:** I'll gather your basic details and technical background
        - **Technical Assessment:** Based on your tech stack, I'll ask relevant technical questions  
        - **Interactive Interview:** Our conversation will flow naturally, with follow-up questions based on your responses
        - **Professional Evaluation:** Your responses will help us understand your technical proficiency
        """)
        
        st.markdown("### Process Overview:")
        st.markdown("""
        1. **Profile Setup** - Share your background and tech stack
        2. **Technical Interview** - Answer questions tailored to your skills  
        3. **Completion** - Receive next steps information
        """)
        
        st.info("💡 **Tip:** Be honest about your experience level and tech stack for the most relevant questions.")
        
        if st.button("Start Your Interview", key="start_btn"):
            st.session_state.page = 'form'
            st.rerun()