# TalentScout - AI Hiring Assistant 



**TalentScout** is an AI-powered technical recruitment chatbot built with Streamlit and Groq. It guides candidates through a welcome page, a form to collect details, and an interactive technical interview with 5 tailored questions based on their tech stack. The app provides real-time feedback, tracks progress, and offers a modern, distraction-free UI.

## Table of Contents

- [Features](#features)
- [Project Architecture](#project-architecture)
- [Query Flow](#query-flow)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Live Demo](#live-demo)
- [Challenges & Solutions](#challenges--solutions)
- [Why No LangChain?](#why-no-langchain)
- [Bonus Features](#bonus-features)


## Features

- **Welcome Page**: Engaging introduction with Inter and Open Sans fonts.
- **Candidate Form**: Collects name, email, phone, experience, position, and tech stack with validation.
- **Interactive Interview**: 5 technical questions tailored to the candidate's tech stack, with skip/submit options.
- **Real-Time Feedback**: Groq evaluates answers and provides feedback.
- **Progress Tracking**: Progress bar showing question count (e.g., "3/5").
- **Session Management**: Streamlit session state and JSON storage for context, with LLM memory for interview flow.
- **Modern UI**: Wide layout, custom CSS, hidden sidebar, and responsive design.
- **Modular Code**: Reusable modules for maintainability.

## Project Architecture

The project uses a modular architecture for clean code organization. Below is the directory structure:

```
├── .env                    # Environment variables (GROQ_API_KEY)
├── README.md               # Project documentation
├── config.py               # App configuration
├── prompts.py              # LLM prompt templates
├── app.py                  # Streamlit app entry point
├── utils/                  # Utility modules
│   ├── file_handler.py     # JSON file operations
│   ├── llm_handler.py      # Groq API integration
│   ├── validators.py       # Email/phone validation
│   ├── session_manager.py  # Session state initialization
├── pages/                  # Page-specific logic
│   ├── welcome_page.py     # Welcome page UI/logic
│   ├── form_page.py        # Form and question generation
│   ├── interview_page.py   # Interview page with chat
├── styles/                 # Styling
│   ├── custom_css.py       # Custom CSS for UI
```

### Key Components

- **app.py**: Configures Streamlit (wide layout, hidden sidebar) and routes pages.
- **pages/**: Separates UI/logic for welcome, form, and interview.
- **utils/**: Handles file operations, LLM calls, validation, and session management.
- **styles/**: Custom CSS with gradients and fonts (Inter/Open Sans).
- **config.py**: Defines settings like `NUM_QUESTIONS=5`.
- **prompts.py**: Manages Groq prompts for questions and feedback.

## Query Flow

The app follows a linear flow across three pages:

1. **Welcome Page**:
   - Shows a welcome card with a "Start Assessment" button.
   - Sets `st.session_state.page = 'form'` on click.

2. **Candidate Form Page**:
   - Collects candidate details with validation.
   - On submission:
     - Stores data in `st.session_state.candidate_info`.
     - Generates 5 questions using Groq (`utils/llm_handler.py`).
     - Saves questions to `generated_questions.json` (`utils/file_handler.py`).
     - Sets `st.session_state.page = 'interview'`.

3. **Interview Page**:
   - Loads questions from JSON.
   - Displays progress bar and chat interface.
   - For each question:
     - Presents question (e.g., "Question 1 of 5").
     - Accepts user input (skip/submit).
     - Evaluates answers with Groq and shows feedback.
     - Updates `current_question_index` in JSON/session state.
   - After 5 questions, displays completion message and "Return to Welcome" button.
   - Resets session and JSON on return.

## Technologies Used

- **Python 3.10+**: Core language.
- **Streamlit**: Web framework.
- **Groq**: AI for question generation and evaluation.
- **Markdown**: Documentation.
- **CSS**: Custom styling with Google Fonts (Inter, Open Sans).
- **JSON**: Data storage.
- **python-dotenv**: Environment variables.
- **GitHub**: Version control.


## Setup Instructions

### Prerequisites

- Python 3.10+
- Git
- Text editor (e.g., VS Code)
- Groq API key (free)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vinu0404/tech-recruitment-chatbot.git
   cd tech-recruitment-chatbot
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install streamlit groq python-dotenv
   ```

4. **Set Up Environment Variables**:
   - Create `.env` file:
     ```bash
     touch .env
     ```
   - Add:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     MODEL_ID=meta-llama/llama-4-scout-17b-16e-instruct
     ```

5. **Run the App**:
   ```bash
   streamlit run app.py
   ```
   - Open `http://localhost:8501`.
   - Navigate through welcome, form, and interview.

### Troubleshooting

- **API Key Error**: Verify `GROQ_API_KEY` in `.env`.
- **IndexError**: Delete `generated_questions.json` and restart.
- **Streamlit Version**: Ensure Streamlit 1.36.0+ for hidden sidebar.
- **LLM Issues**: Check `form_page.py` debug output.

## Live Demo

- **Deployed Link**: [TalentScout on Render](https://tech-recruitment-chatbot.onrender.com)
- **Video Demo**: [Watch the Demo](https://www.loom.com/share/becb6fc375524966940b1c7e91e87b02?sid=f6d34a85-4c24-47fa-80c8-356863e73896).


## Challenges & Solutions

### 1. Groq Output in JSON Format
- **Problem**: Groq returned questions in JSON, complicating parsing for plain text.
- **Solution**: Updated `prompts.py` to request numbered lists. Added regex parsing in `form_page.py` with generic question fallbacks.

### 2. Lack of Session Management and Memory
- **Problem**: No context retention, leading to disjointed interviews.
- **Solution**: Used Streamlit session state (`utils/session_manager.py`), JSON storage (`utils/file_handler.py`), and LLM chat history in `interview_page.py` for seamless flow.


## Why No LangChain?

We opted for a direct API approach over LangChain for this project.

### Reasons for Direct API

- ✅ **Simplicity**: Straightforward API calls for a simple interface.
- ✅ **Performance**: Minimal dependencies (4 packages) for faster execution.
- ✅ **Control**: Full control over prompts and responses.
- ✅ **Lightweight**: Low overhead for requirements.
- ✅ **Reliability**: Fewer failure points.

### Architecture Pattern: Direct Groq API Usage

```python
# utils/llm_handler.py
client = Groq(api_key=GROQ_API_KEY)
response = client.chat.completions.create(
    model=MODEL_ID,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
)
```

### LLM Integration Features

- **Context Management**: Streamlit session state (`utils/session_manager.py`).
- **Prompt Engineering**: Custom prompts (`prompts.py`).
- **Memory**: Chat history in session state (`interview_page.py`).
- **Response Processing**: Parsing/validation in `form_page.py`.
- **Error Handling**: API exceptions in `utils/llm_handler.py`.

### Framework Comparison

| Feature            | Direct API (Used)       | LangChain              |
|--------------------|-------------------------|------------------------|
| **Complexity**     | Low                     | Medium-High            |
| **Dependencies**   | Minimal (4 packages)    | Heavy (20+ packages)   |
| **Performance**    | Fast                    | Slower                 |
| **Customization**  | Full Control            | Framework Constraints   |
| **Learning Curve** | Minimal                 | Steeper                |

### When to Use LangChain

- Complex Retrieval Augmented Generation (RAG).
- Multiple LLM providers.
- Advanced chains/workflows.
- Vector database integration.
- Document processing pipelines.
- Agent-based architectures.

### Why Direct API Suits This Use Case

- Simple conversational interface with single LLM (Groq).
- Straightforward prompt-response pattern.
- Custom logic for interview flow (`interview_page.py`, `form_page.py`).
- Streamlit manages UI state efficiently.

The app achieves context memory and adaptive questioning through custom code, avoiding framework overhead.

## Bonus Features

- **Multilingual Support**: The app leverages the Meta-Llama-4-Scout model, trained on multilingual data for diverse language support ([Oracle Docs](https://docs.oracle.com/en-us/iaas/Content/generative-ai/meta-llama-4-scout.htm#:~:text=Multilingual%20Support%3A%20Trained%20on%20data,understanding%20is%20limited%20to%20English)).
- **Personalized Responses**: Enhanced evaluation prompts in `prompts.py` use candidate history (tech stack, experience) to tailor feedback, improving interview relevance.
- **Sentiment Analysis**: Integrated into the evaluation prompt to gauge candidate emotions during the interview, enabling empathetic and supportive responses.

*Built with 😎 by Vinu for the tech hiring community.*