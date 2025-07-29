# Multi-Agent AI System for Image Analysis

This project is a Python-based multi-agent system that uses AI to analyze images and hold a conversation about them. It features a vision agent for image captioning, a language agent for chat, and safety guardrails for content moderation.

## Features

- **Image Analysis**: Upload an image to get an AI-generated description.
- **Conversational AI**: Ask follow-up questions about the image.
- **Action Execution**: Ask the AI to perform simple tasks like opening a web browser.
- **Safety Guardrails**: Built-in checks for harmful images and text prompts.

## Prerequisites

- Python 3.8+

## How to Run

1.  **Clone the Repository (if needed)**
    ```bash
    git clone <your-repo-url>
    cd multi_agent_system
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate on Windows
    venv\Scripts\activate

    # Activate on macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**
    - Create a file named `.env` in the project's root directory.
    - Add your Groq API key to it:
      ```
      GROQ_API_KEY="gsk_YourSecretGroqApiKeyGoesHere"
      ```

5.  **Run the Application**
    ```bash
    streamlit run app.py
    ```
    
    Open the local URL provided in your terminal to view the application.

**Note:** The first time you run the app, it will download several large AI models from Hugging Face. This is a one-time setup and may take a few minutes.