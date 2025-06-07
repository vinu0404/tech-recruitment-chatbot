def get_question_generation_prompt(tech_stack, experience_level, num_questions,position):
    return f"""
    Generate exactly {num_questions} technical interview questions for a candidate with:
    - Experience Level: {experience_level}
    - Tech Stack: {', '.join(tech_stack)}
    - Position: {position}
    
    Requirements:
    - Questions should be appropriate for {experience_level} level
    - Most Focus on Generate questions that are relevant to the position and tech stack
    - Most Focus mainly on the question likely from  {position} with level should be {experience_level} as the interview is for specific position.Ask question on the subjects which comes under the {position} position.
    - Include both theoretical and practical questions
    - Make questions progressive in difficulty
    - Format as a simple numbered list (1. 2. 3. etc.)
    - Ask questions on the  technologies: {', '.join(tech_stack[:3])}
    
    
    Return ONLY the {num_questions} questions, nothing else.
    """

def get_question_generation_system_prompt():
    return """You are an expert technical interviewer for a recruitment agency. 
    Generate technical interview questions based on the candidate's tech stack and experience level.
    Questions should be appropriate for the experience level and cover practical knowledge.
    Return ONLY the questions, numbered, without any additional text."""

def get_evaluation_prompt(question, answer, tech_stack, position):
    return f"""
    Question: {question}
    Candidate's Answer: {answer}
    Tech Stack: {', '.join(tech_stack)}
    Position: {position}

    
    Provide brief feedback on their answer. Be encouraging and professional. Maximum 1-2 sentences.
    """

def get_evaluation_system_prompt():
    return """You are an expert technical interviewer. 
    Provide brief, encouraging feedback on the candidate's answer. 
    Keep it professional and constructive. Maximum 2-3 sentences."""