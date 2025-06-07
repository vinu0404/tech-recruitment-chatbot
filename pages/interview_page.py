import streamlit as st
from utils.file_handler import load_questions_from_json, update_question_index, delete_questions_file
from utils.llm_handler import get_llm_response, initialize_groq_client
from utils.session_manager import initialize_session_state
from prompts import get_evaluation_prompt, get_evaluation_system_prompt
from datetime import datetime

def evaluate_answer(client, question, answer, tech_stack,position):
    """Evaluate candidate's answer and provide feedback"""
    system_prompt = get_evaluation_system_prompt()
    prompt = get_evaluation_prompt(question, answer, tech_stack,position)
    return get_llm_response(client, prompt, system_prompt)

def interview_page():
    """Interactive interview page"""
    client = initialize_groq_client()
    candidate = st.session_state.candidate_info
    
    questions_data = load_questions_from_json()
    if not questions_data:
        st.error("❌ No questions found. Please restart the interview process.")
        if st.button("🏠 Return to Welcome"):
            st.session_state.page = 'welcome'
            st.rerun()
        return
    
    questions = questions_data['questions']
    total_questions = len(questions)
    current_index = questions_data['current_question_index']
    
    # Validate index and questions
    if not questions or current_index >= total_questions:
        st.error("❌ Invalid question data or index out of range. Resetting interview.")
        st.session_state.page = 'welcome'
        if st.button("🏠 Return to Welcome"):
            delete_questions_file()
            st.session_state.page = 'welcome'
            st.rerun()
        return
    
    st.markdown(f"""
    <div class="interview-header">
        <h1>🎤 Technical Interview - {candidate['name']}</h1>
        <p>Position: {candidate['position']} | Experience: {candidate['experience']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    progress_percentage = (current_index / total_questions) * 100 if total_questions > 0 else 0
    
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_percentage}%"></div>
    </div>
    <p style="text-align: center; margin: 0.5rem 0;">
        Progress: {current_index}/{total_questions} questions completed
    </p>
    """, unsafe_allow_html=True)
    
    if not st.session_state.interview_started:
        welcome_msg = f"""
        Hello {candidate['name']}! 👋 
        
        I'm excited to begin your technical interview for the {candidate['position']} position. 
        
        Based on your tech stack ({', '.join(candidate['tech_stack'][:3])}) and {candidate['position']} as your Desired Position, I've prepared {total_questions} questions to assess your technical knowledge and problem-solving skills.
        
        Please answer to the best of your ability. Don't worry if you're unsure - honesty is valued!
        
        Let's begin! 🚀
        """
        
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': welcome_msg,
            'timestamp': datetime.now()
        })
        st.session_state.interview_started = True
        st.session_state.current_question_index = 0
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'assistant':
                content_formatted = message['content'].replace('\n', '<br>')
                if content_formatted.startswith('**Question'):
                    question_number = content_formatted.split('of')[0].replace('**Question ', '').strip()
                    question_text = content_formatted.split(':**<br><br>')[1] if ':**<br><br>' in content_formatted else content_formatted
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <div class="question-header">🤖 AI Interviewer: Question {question_number}</div>
                        {question_text}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <strong>🤖 AI Interviewer:</strong><br>
                        {content_formatted}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                content_formatted = message['content'].replace('\n', '<br>')
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong><br>
                    {content_formatted}
                </div>
                """, unsafe_allow_html=True)
    
    if st.session_state.interview_completed:
        st.markdown("""
        <div class="completion-message">
            <h2>🎉 Interview Completed!</h2>
            <p>Thank you for taking the time to complete our technical assessment.</p>
            <p><strong>Next Steps:</strong></p>
            <ul>
                <li>Our technical team will review your responses.</li>
                <li>You'll hear from us within 2-3 business days.</li>
                <li>If selected, we'll schedule a follow-up interview.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Return to Welcome"):
            delete_questions_file()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            initialize_session_state()
            st.rerun()
        return
    
    if current_index < total_questions and not st.session_state.waiting_for_answer:
        current_question = questions[current_index]
        question_msg = f"**Question {current_index + 1} of {total_questions}:**\n\n{current_question}"
        
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': question_msg,
            'timestamp': datetime.now()
        })
        st.session_state.waiting_for_answer = True
        st.rerun()
    
    if not st.session_state.interview_completed and st.session_state.waiting_for_answer:
        st.markdown("---")
        user_input = st.text_area(
            "✍️ Your Answer:",
            placeholder="Type your answer here... Be specific and provide examples where possible.",
            height=150,
            key=f"answer_{current_index}"
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⏭️ Skip Question", help="Skip this question if you're unsure"):
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': "I'd like to skip this question.",
                    'timestamp': datetime.now()
                })
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': "No problem! Let's move on to the next question. 👍",
                    'timestamp': datetime.now()
                })
                
                new_index = current_index + 1
                update_question_index(new_index)
                st.session_state.current_question_index = new_index
                st.session_state.waiting_for_answer = False
                
                if new_index >= total_questions:
                    st.session_state.interview_completed = True
                
                st.rerun()
        
        with col3:
            if st.button("📤 Submit", type="primary", disabled=not user_input.strip()):
                if user_input.strip().lower() in ['exit', 'quit', 'end', 'stop']:
                    st.session_state.interview_completed = True
                    st.rerun()
                
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input,
                    'timestamp': datetime.now()
                })
                
                with st.spinner("🤔 Analyzing your answer..."):
                    feedback = evaluate_answer(
                        client,
                        questions[current_index],
                        user_input,
                        candidate['tech_stack']
                    )
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': f"Thank you for your answer! {feedback}",
                        'timestamp': datetime.now()
                    })
                
                new_index = current_index + 1
                update_question_index(new_index)
                st.session_state.current_question_index = new_index
                st.session_state.waiting_for_answer = False
                
                if new_index >= total_questions:
                    st.session_state.interview_completed = True
                
                st.rerun()