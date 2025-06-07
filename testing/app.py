import streamlit as st
import json
from groq import Groq
from datetime import datetime
import re
import os

# Configuration
GROQ_API_KEY = "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"
MODEL_ID = "meta-llama/llama-4-scout-17b-16e-instruct"
NUM_QUESTIONS = 5

# Initialize Groq client
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    client = None

# Page configuration
st.set_page_config(
    page_title="TalentScout - AI Hiring Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI/UX with improved fonts and contras
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Poppins:wght@600&family=Inter:wght@500&family=Open+Sans:wght@400&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f2f5;
        color: #333;
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
        background: linear-gradient(135deg, #4a90e2 0%, #6b48ff 100%);
        color: white;
        border: none;
        padding: 0.6rem 2.5rem;
        border-radius: 25px;
        font-weight: 500;
        font-family: 'Roboto', sans-serif;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(74, 144, 226, 0.4);
    }

    .completion-message {
        background: #d4edda;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border-left: 5px solid #28a745;
        font-family: 'Roboto', sans-serif;
        color: #1a1a1a;
    }

    .completion-message h2 {
        font-family: 'Poppins', sans-serif;
        color: #155724;
        font-size: 1.8rem;
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

# File paths for JSON storage
QUESTIONS_FILE = "generated_questions.json"
INTERVIEW_DATA_FILE = "interview_data.json"

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
    """Load questions from JSON file"""
    try:
        if os.path.exists(QUESTIONS_FILE):
            with open(QUESTIONS_FILE, 'r') as f:
                return json.load(f)
        return None
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return None

def update_question_index(new_index):
    """Update current question index in JSON"""
    try:
        data = load_questions_from_json()
        if data:
            data['current_question_index'] = new_index
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

# Initialize session state
def initialize_session_state():
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

def get_llm_response(prompt, system_prompt="You are a helpful AI assistant."):
    """Get response from Groq LLM"""
    if client is None:
        return "I apologize, but I'm experiencing technical difficulties with the AI service. Please try again later."
    
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error getting LLM response: {str(e)}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again."

def generate_technical_questions(tech_stack, experience_level):
    """Generate technical questions based on tech stack and experience"""
    system_prompt = """You are an expert technical interviewer for a recruitment agency. 
    Generate exactly 5 technical interview questions based on the candidate's tech stack and experience level.
    Questions should be appropriate for the experience level and cover practical knowledge.
    Return ONLY the questions, numbered 1-5, without any additional text."""
    
    prompt = f"""
    Generate exactly {NUM_QUESTIONS} technical interview questions for a candidate with:
    - Experience Level: {experience_level}
    - Tech Stack: {', '.join(tech_stack)}
    
    Requirements:
    - Questions should be appropriate for {experience_level} level
    - Cover different aspects of the technologies mentioned
    - Include both theoretical and practical questions
    - Make questions progressive in difficulty
    - Format as a simple numbered list (1. 2. 3. 4. 5.)
    - Focus on the main technologies: {', '.join(tech_stack[:3])}
    
    Return ONLY the 5 questions, nothing else.
    """
    
    response = get_llm_response(prompt, system_prompt)
    
    # Parse questions from response
    questions = []
    lines = response.split('\n')
    for line in lines:
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
            # Clean up the question
            question = re.sub(r'^\d+\.?\s*', '', line)
            question = re.sub(r'^[-•]\s*', '', question)
            if question and len(question) > 10:  # Ensure it's a substantial question
                questions.append(question.strip())
    
    # If parsing failed, try to extract questions differently
    if len(questions) < NUM_QUESTIONS:
        # Fallback: split by common question indicators
        fallback_questions = []
        text = response.replace('\n', ' ')
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and ('?' in sentence or any(word in sentence.lower() for word in ['what', 'how', 'why', 'explain', 'describe', 'implement'])):
                fallback_questions.append(sentence)
        
        if fallback_questions:
            questions = fallback_questions[:NUM_QUESTIONS]
    
    # Ensure we have exactly NUM_QUESTIONS questions
    if len(questions) < NUM_QUESTIONS:
        # Add generic questions if needed
        generic_questions = [
            f"Explain the key features of {tech_stack[0] if tech_stack else 'your main technology'}.",
            f"How would you handle error handling in {tech_stack[0] if tech_stack else 'your projects'}?",
            "Describe a challenging project you've worked on and how you solved it.",
            f"What are the best practices you follow when working with {tech_stack[0] if tech_stack else 'your technology stack'}?",
            "How do you stay updated with the latest developments in your field?"
        ]
        
        while len(questions) < NUM_QUESTIONS:
            questions.append(generic_questions[len(questions)])
    
    return questions[:NUM_QUESTIONS]

def evaluate_answer(question, answer, tech_stack):
    """Evaluate candidate's answer and provide feedback"""
    system_prompt = """You are an expert technical interviewer. 
    Provide brief, encouraging feedback on the candidate's answer. 
    Keep it professional and constructive. Maximum 2-3 sentences."""
    
    prompt = f"""
    Question: {question}
    Candidate's Answer: {answer}
    Tech Stack: {', '.join(tech_stack)}
    
    Provide brief feedback on their answer. Be encouraging and professional.Dont make any statement like "Let's explore this further and see if we can work together to find a solution"
    """
    
    return get_llm_response(prompt, system_prompt)

def validate_email(email):
    """Validate email format"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def validate_phone(phone):
    """Validate phone number format"""
    phone_pattern = r'^\+?1?\d{9,15}$|^(\+\d{1,3}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$'
    return bool(re.match(phone_pattern, phone.strip().replace(' ', '')))

def welcome_page():
    """Welcome page with introduction"""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Welcome to TalentScout</h1>
        <h3>AI-Powered Hiring Assistant</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="welcome-card">
            <h2>🤖 About Our AI Hiring Assistant</h2>
            <p><strong></strong> I'm here to conduct your initial technical screening for technology positions at TalentScout.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 What to Expect:")
        st.markdown("""
        - **Information Collection:** I'll gather your basic details and technical background
        - **Technical Assessment:** Based on your tech stack, I'll ask relevant technical questions  
        - **Interactive Interview:** Our conversation will flow naturally, with follow-up questions based on your responses
        - **Professional Evaluation:** Your responses will help us understand your technical proficiency
        """)
        
        st.markdown("### ⚡ Process Overview:")
        st.markdown("""
        1. **Profile Setup** - Share your background and tech stack
        2. **Technical Interview** - Answer questions tailored to your skills  
        3. **Completion** - Receive next steps information
        """)
        
        st.info("💡 **Tip:** Be honest about your experience level and tech stack for the most relevant questions.")
        
        if st.button("🚀 Start Your Interview", key="start_btn"):
            st.session_state.page = 'form'
            st.rerun()

def candidate_form_page():
    """Candidate information form page"""
    st.markdown("""
    <div class="main-header">
        <h1>📝 Candidate Information</h1>
        <p>Please fill out your details to begin the technical assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("🧑‍💼 Full Name *", placeholder="Enter your full name")
            email = st.text_input("📧 Email Address *", placeholder="your.email@example.com")
            phone = st.text_input("📱 Phone Number *", placeholder="+1 (555) 123-4567 or +919876543210")
        
        with col2:
            experience = st.selectbox(
                "⏱️ Years of Experience *",
                ["Fresher", "Intern", "1 Year", "2 Years", "3-5 Years", "5+ Years"]
            )
            position = st.text_input("💼 Desired Position *", placeholder="e.g., Full Stack Developer")
            location = st.text_input("📍 Current Location *", placeholder="City, Country")
        
        st.markdown("### 🔧 Technical Skills")
        
        col1, col2 = st.columns(2)
        with col1:
            languages = st.text_area(
                "Programming Languages *",
                placeholder="e.g., Python, JavaScript, Java, C++",
                help="List programming languages you're proficient in"
            )
            frameworks = st.text_area(
                "Frameworks & Libraries",
                placeholder="e.g., React, Django, Spring Boot, Express.js",
                help="Web frameworks, libraries you've worked with"
            )
        
        with col2:
            databases = st.text_area(
                "Databases",
                placeholder="e.g., MySQL, PostgreSQL, MongoDB, Redis",
                help="Database systems you're familiar with"
            )
            tools = st.text_area(
                "Tools & Technologies",
                placeholder="e.g., Git, Docker, AWS, Jenkins",
                help="Development tools, cloud platforms, DevOps tools"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Validation and submission
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⬅️ Back to Welcome"):
                st.session_state.page = 'welcome'
                st.rerun()
        
        with col3:
            if st.button("✅ Submit & Start Interview", type="primary"):
                # Validate required fields
                if not all([full_name, email, phone, experience, position, location, languages]):
                    st.error("❌ Please fill in all required fields marked with *")
                else:
                    # Validate email
                    if not validate_email(email):
                        st.error("❌ Please enter a valid email address (e.g., user@domain.com)")
                    # Validate phone
                    elif not validate_phone(phone):
                        st.error("❌ Please enter a valid phone number (e.g., +1 (555) 123-4567 or +919876543210)")
                    else:
                        # Compile tech stack
                        tech_stack = []
                        for tech in [languages, frameworks, databases, tools]:
                            if tech:
                                tech_items = [item.strip() for item in tech.replace(',', '\n').split('\n') if item.strip()]
                                tech_stack.extend(tech_items)
                        
                        if not tech_stack:
                            st.error("❌ Please specify at least one programming language or technology")
                            return
                        
                        # Store candidate information
                        st.session_state.candidate_info = {
                            'name': full_name,
                            'email': email,
                            'phone': phone,
                            'experience': experience,
                            'position': position,
                            'location': location,
                            'tech_stack': tech_stack,
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        # Generate questions and save to JSON
                        with st.spinner("🔄 Generating your personalized technical questions..."):
                            questions = generate_technical_questions(tech_stack, experience)
                            
                            if len(questions) >= NUM_QUESTIONS:
                                success = save_questions_to_json(questions, st.session_state.candidate_info)
                                if success:
                                    st.session_state.questions_generated = True
                                    st.success(f"✅ Generated {len(questions)} technical questions! Starting your interview...")
                                    st.session_state.page = 'interview'
                                    st.rerun()
                                else:
                                    st.error("❌ Error saving questions. Please try again.")
                            else:
                                st.error("❌ Error generating questions. Please try again or contact support.")

def interview_page():
    """Interactive interview page"""
    candidate = st.session_state.candidate_info
    
    # Load questions data
    questions_data = load_questions_from_json()
    if not questions_data:
        st.error("❌ No questions found. Please restart the interview process.")
        if st.button("🏠 Return to Welcome"):
            initialize_session_state()
            st.rerun()
        return
    
    questions = questions_data['questions']
    total_questions = len(questions)
    current_index = questions_data['current_question_index']
    
    st.markdown(f"""
    <div class="interview-header">
        <h1>🎤 Technical Interview - {candidate['name']}</h1>
        <p>Position: {candidate['position']} | Experience: {candidate['experience']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress_percentage = (current_index / total_questions) * 100 if total_questions > 0 else 0
    
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_percentage}%"></div>
    </div>
    <p style="text-align: center; margin: 0.5rem 0;">
        Progress: {current_index}/{total_questions} questions completed
    </p>
    """, unsafe_allow_html=True)
    
    # Initialize interview
    if not st.session_state.interview_started:
        welcome_msg = f"""
        Hello {candidate['name']}! 👋 
        
        I'm excited to begin your technical interview for the {candidate['position']} position. 
        
        Based on your tech stack ({', '.join(candidate['tech_stack'][:3])}), I've prepared {total_questions} questions to assess your technical knowledge and problem-solving skills.
        
        Please answer to the best of your ability. Don't worry if you don't know something - honesty is valued!
        
        Let's begin! 🚀
        """
        
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': welcome_msg,
            'timestamp': datetime.now()
        })
        st.session_state.interview_started = True
        st.session_state.current_question_index = 0
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'assistant':
                content_formatted = message['content'].replace('\n', '<br>')
                if content_formatted.startswith('**Question'):
                    # Apply custom styling for questions
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
    
    # Check if interview is completed
    if st.session_state.interview_completed:
        st.markdown("""
        <div class="completion-message">
            <h2>🎉 Interview Completed!</h2>
            <p>Thank you for taking the time to complete our technical assessment.</p>
            <p><strong>Next Steps:</strong></p>
            <ul>
                <li>Our technical team will review your responses</li>
                <li>You'll hear back from us within 2-3 business days</li>
                <li>If selected, we'll schedule a follow-up interview</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Return to Welcome"):
            # Clean up - delete questions file and reset session
            delete_questions_file()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            initialize_session_state()
            st.rerun()
        return
    
    # Ask next question if available
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
    
    # User input section
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
            if st.button("⏭️ Skip Question", help="Skip this question if you're not sure"):
                # Add skip message
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': "I'd like to skip this question.",
                    'timestamp': datetime.now()
                })
                
                # Add acknowledgment
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': "No problem! Let's move on to the next question. 👍",
                    'timestamp': datetime.now()
                })
                
                # Update progress
                new_index = current_index + 1
                update_question_index(new_index)
                st.session_state.current_question_index = new_index
                st.session_state.waiting_for_answer = False
                
                # Check if interview is complete
                if new_index >= total_questions:
                    st.session_state.interview_completed = True
                
                st.rerun()
        
        with col3:
            if st.button("📤 Submit Answer", type="primary", disabled=not user_input.strip()):
                # Check for exit keywords
                if user_input.strip().lower() in ['exit', 'quit', 'end', 'stop']:
                    st.session_state.interview_completed = True
                    st.rerun()
                
                # Add user response
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input,
                    'timestamp': datetime.now()
                })
                
                # Generate feedback
                with st.spinner("🤔 Analyzing your answer..."):
                    feedback = evaluate_answer(
                        questions[current_index],
                        user_input,
                        candidate['tech_stack']
                    )
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': f"Thank you for your answer! {feedback}",
                        'timestamp': datetime.now()
                    })
                
                # Update progress
                new_index = current_index + 1
                update_question_index(new_index)
                st.session_state.current_question_index = new_index
                st.session_state.waiting_for_answer = False
                
                # Check if interview is complete
                if new_index >= total_questions:
                    st.session_state.interview_completed = True
                
                st.rerun()

def main():
    """Main application function"""
    initialize_session_state()
    
    # Navigation based on current page
    if st.session_state.page == 'welcome':
        welcome_page()
    elif st.session_state.page == 'form':
        candidate_form_page()
    elif st.session_state.page == 'interview':
        interview_page()

if __name__ == "__main__":
    main()