import json
import os
import streamlit as st
from datetime import datetime
from config import QUESTIONS_FILE

def save_questions_to_json(questions, candidate_info):
    """Save generated questions to JSON file"""
    data = {
        "candidate_id": f"{candidate_info['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "candidate_info": candidate_info,
        "questions": questions,
        "generated_at": datetime.now().isoformat(),
        "total_questions": len(questions),
        "current_question_index": 0
    }
    
    try:
        with open(QUESTIONS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving questions: {e}")
        return False

def load_questions_from_json():
    """Load questions from JSON file with validation"""
    try:
        if os.path.exists(QUESTIONS_FILE):
            with open(QUESTIONS_FILE, 'r') as f:
                data = json.load(f)
                # Validate data structure
                if not isinstance(data.get('questions'), list) or not data.get('total_questions'):
                    st.error("Invalid questions data structure.")
                    return None
                # Ensure current_question_index  within bounds
                if data.get('current_question_index', 0) >= len(data['questions']):
                    data['current_question_index'] = 0
                    with open(QUESTIONS_FILE, 'w') as f:
                        json.dump(data, f, indent=2)
                return data
        return None
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return None

def update_question_index(new_index):
    """Update current question index in JSON"""
    try:
        data = load_questions_from_json()
        if data:
            if 0 <= new_index <= len(data['questions']):
                data['current_question_index'] = new_index
                with open(QUESTIONS_FILE, 'w') as f:
                    json.dump(data, f, indent=2)
            else:
                st.warning("Invalid question index. Resetting to 0.")
                data['current_question_index'] = 0
                with open(QUESTIONS_FILE, 'w') as f:
                    json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error updating question index: {e}")

def delete_questions_file():
    """Delete questions file after interview completion"""
    try:
        if os.path.exists(QUESTIONS_FILE):
            os.remove(QUESTIONS_FILE)
    except Exception as e:
        st.error(f"Error deleting questions file: {e}")