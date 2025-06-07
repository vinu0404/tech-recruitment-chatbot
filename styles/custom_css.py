import streamlit as st

def apply_custom_css():
    """Apply custom CSS styles to the app"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@600&family=Inter:wght@500&family=Open+Sans:wght@400&display=swap');

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f2f5;
            color: #333;
        }

        /* Hide the sidebar */
        [data-testid="stSidebar"] {
            display: none;
        }
        /* Adjust main content to full width when sidebar is hidden */
        .main .block-container {
            max-width: 100%;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #4a90e2 0%, #6b48ff 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            font-family: 'Poppins', sans-serif;
        }

        .main-header h1 {
            font-size: 2.5rem;
            margin: 0;
        }

        .welcome-card {
            background: #e9ecef;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            margin: 2rem 0;
            border-left: 5px solid #4a90e2;
            color: #1a1a1a;
        }

        .welcome-card h2 {
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            font-size: 1.7rem;
            color: #2c3e50;
            margin-bottom: 1rem;
        }

        .welcome-card p {
            font-family: 'Open Sans', sans-serif;
            font-size: 1rem;
            color: #1a1a1a;
        }

        .form-card {
            background: #ffffff;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
        }

        .chat-message {
            padding: 1.5rem;
            margin: 0.8rem 0;
            border-radius: 12px;
            max-width: 85%;
            font-size: 1rem;
            line-height: 1.5;
        }

        .bot-message {
            background: #e6f0fa;
            border-left: 5px solid #4a90e2;
            margin-right: 15%;
            color: #1a1a1a;
            font-family: 'Roboto', sans-serif;
        }

        .bot-message strong {
            font-family: 'Poppins', sans-serif;
            font-size: 1.1rem;
            color: #2c3e50;
        }

        .user-message {
            background: #d9eaff;
            border-right: 5px solid #6b48ff;
            margin-left: 15%;
            text-align: right;
            color: #1a1a1a;
            font-family: 'Roboto', sans-serif;
        }

        .interview-header {
            background: linear-gradient(135deg, #ff4757 0%, #ff6b81 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
            font-family: 'Poppins', sans-serif;
        }

        .progress-bar {
            background: #d9dfe6;
            border-radius: 10px;
            padding: 4px;
            margin: 1rem 0;
        }

        .progress-fill {
            background: linear-gradient(90deg, #4a90e2, #6b48ff);
            height: 22px;
            border-radius: 8px;
            transition: width 0.4s ease;
        }

        .stButton > button {
            background: linear-gradient(90deg, #4a90e2, #6b48ff);
            color: white;
            border: none;
            padding: 0.6rem 2rem;
            border-radius: 25px;
            font-weight: 500;
            font-family: 'Roboto', sans-serif;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .stButton > button {
            background: linear-gradient(90deg, #4a90e2 #2, #6b48ff);
            color: white;
            padding-bottom: 0.6rem;
            border-radius: 25px;
            font-weight: 500;
        }

        .completion-message {
            background: #d4edda;
            padding: 2rem.5rem;
            border-radius: 10px;
            text-align: center;
            margin: 2px 0rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            border-left: 5px solid #28a745;
            font-family: 'Roboto', sans-serif;
            color: #1a1a1a;
        }

        .completion-message h2 {
            font-family: 'Poppins', sans-serif;
            color: #155724;
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }

        .completion-message ul {
            text-align: left;
            display: inline-block;
            font-size: 1rem;
            color: #1a1a1a;
        }

        .question-header {
            font-family: 'Poppins', sans-serif;
            font-size: 1.3rem;
            color: #2c3e50;
            background: #f5f7fa;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
    </style>
    """, unsafe_allow_html=True)