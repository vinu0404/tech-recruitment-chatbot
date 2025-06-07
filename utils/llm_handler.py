from groq import Groq
import streamlit as st
import os
from config import MODEL_ID, MAX_TOKENS, TEMPERATURE

def initialize_groq_client():
    """Initialize Groq client"""
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        return client
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {e}")
        return None

def get_llm_response(client, prompt, system_prompt):
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
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error getting LLM response: {str(e)}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again."