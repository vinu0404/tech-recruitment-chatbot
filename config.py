import random

# App settings
APP_TITLE = "TalentScout - AI Hiring Assistant"
APP_ICON = " "
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "collapsed"

# Question settings
MIN_QUESTIONS = 4
MAX_QUESTIONS = 7
NUM_QUESTIONS = 5

# File paths
QUESTIONS_FILE = "generated_questions.json"
INTERVIEW_DATA_FILE = "interview_data.json"

# LLM settings
MAX_TOKENS = 800
TEMPERATURE = 0.7
MODEL_ID="meta-llama/llama-4-scout-17b-16e-instruct"