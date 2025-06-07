import streamlit as st
from utils.validators import validate_email, validate_phone
from utils.file_handler import save_questions_to_json
from utils.llm_handler import get_llm_response, initialize_groq_client
from prompts import get_question_generation_prompt, get_question_generation_system_prompt
from config import NUM_QUESTIONS
from datetime import datetime
import re

def generate_technical_questions(client, tech_stack, experience_level,position):
    """Generate technical questions based on tech stack,positions experience"""
    system_prompt = get_question_generation_system_prompt()
    prompt = get_question_generation_prompt(tech_stack, experience_level,NUM_QUESTIONS,position)
    
    response = get_llm_response(client, prompt, system_prompt)
    
    # Log response for debugging
    st.write(f"LLM Response: {response}")
    
    # Parse questions from response
    questions = []
    lines = response.split('\n')
    for line in lines:
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
            question = re.sub(r'^\d+\.?\s*', '', line)
            question = re.sub(r'^[-•]\s*', '', question)
            if question and len(question) > 10:
                questions.append(question.strip())
    
    # Fallback parsing
    if len(questions) < NUM_QUESTIONS:
        fallback_questions = []
        text = response.replace('\n', ' ')
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and ('?' in sentence or any(word in sentence.lower() for word in ['what', 'how', 'why', 'explain', 'describe', 'implement'])):
                fallback_questions.append(sentence)
        
        if fallback_questions:
            questions = fallback_questions[:NUM_QUESTIONS]
    
    # Ensure exactly NUM_QUESTIONS questions
    if len(questions) < NUM_QUESTIONS:
        generic_questions = [
            f"Explain the key features of {tech_stack[0] if tech_stack else 'your main technology'}.",
            f"How would you handle error handling in {tech_stack[0] if tech_stack else 'your projects'}?",
            "Describe a challenging project you've worked on and how you solved it.",
            f"What are the best practices you follow when working with {tech_stack[0] if tech_stack else 'your technology stack'}?",
            "How do you stay updated with the latest developments in your field?",
            f"Compare two features of {tech_stack[1] if len(tech_stack) > 1 else 'a technology you use'} and {tech_stack[0] if tech_stack else 'another technology'}.",
            f"Explain a design pattern commonly used in {tech_stack[0] if tech_stack else 'your projects'}."
        ]
        
        while len(questions) < NUM_QUESTIONS:
            questions.append(generic_questions[len(questions) % len(generic_questions)])
    
    return questions[:NUM_QUESTIONS]

def candidate_form_page():
    """Candidate information form page"""
    client = initialize_groq_client()
    
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
                if not all([full_name, email, phone, experience, position, location, languages]):
                    st.error("❌ Please fill in all required fields marked with *")
                else:
                    if not validate_email(email):
                        st.error("❌ Please enter a valid email address (e.g., user@domain.com)")
                    elif not validate_phone(phone):
                        st.error("❌ Please enter a valid phone number (e.g., +1 (555) 123-4567 or +919876543210)")
                    else:
                        tech_stack = []
                        for tech in [languages, frameworks, databases, tools]:
                            if tech:
                                tech_items = [item.strip() for item in tech.replace(',', '\n').split('\n') if item.strip()]
                                tech_stack.extend(tech_items)
                        
                        if not tech_stack:
                            st.error("❌ Please specify at least one programming language or technology")
                            return
                        
                        st.session_state.candidate_info = {
                            'name': full_name,
                            'email': email,
                            'phone': phone,
                            'experience': experience,
                            'position': position,
                            'location': location,
                            'tech_stack': tech_stack,
                            'timestamp': st.session_state.get('timestamp', datetime.now().isoformat())
                        }
                        
                        with st.spinner("🔄 Generating your personalized technical questions..."):
                            questions = generate_technical_questions(client, tech_stack, experience, position)
                            
                            if len(questions) == NUM_QUESTIONS:
                                success = save_questions_to_json(questions, st.session_state.candidate_info)
                                if success:
                                    st.session_state.questions_generated = True
                                    st.success(f"✅ Generated {len(questions)} technical questions! Starting your interview...")
                                    st.session_state.page = 'interview'
                                    st.rerun()
                                else:
                                    st.error("❌ Error saving questions. Please try again.")
                            else:
                                st.error(f"❌ Failed to generate {NUM_QUESTIONS} questions. Got {len(questions)}. Please try again.")