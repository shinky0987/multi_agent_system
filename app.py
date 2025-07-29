import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image

# Import agent and guardrail modules
from agents.vision_agent import VisionAgent
from agents.language_agent import LanguageAgent
from agents.action_agent import ActionAgent
from agents.text_moderation_agent import TextModerationAgent
from guardrails import is_valid_image

# Load environment variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="wide"
)

# --- Session State Initialization ---
def initialize_session_state():
    if "image_path" not in st.session_state:
        st.session_state.image_path = None
    if "image_analyzed" not in st.session_state:
        st.session_state.image_analyzed = False
    if "image_info" not in st.session_state:
        st.session_state.image_info = ""
    if "messages" not in st.session_state:
        st.session_state.messages = []

initialize_session_state()

# --- App Title ---
st.title("Multi-Agent AI System")
st.subheader("An AI-powered image analysis and conversational assistant with advanced guardrails")

# --- Sidebar for Image Upload ---
st.sidebar.header("Image Upload")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Create a temporary directory if it doesn't exist
    if not os.path.exists("temp_images"):
        os.makedirs("temp_images")
    
    temp_image_path = os.path.join("temp_images", uploaded_file.name)
    
    with open(temp_image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.sidebar.image(uploaded_file, caption='Uploaded Image.', use_container_width=True)
    st.session_state.image_path = temp_image_path

    # Reset analysis state for new image and clear previous analysis info
    st.session_state.image_analyzed = False
    st.session_state.image_info = ""

    # Validate the uploaded image with Guardrails
    with st.spinner('Guardrail: Checking image validity...'):
        if not is_valid_image(st.session_state.image_path):
            st.error("[Guardrails] ❌ Invalid or harmful image. Please upload another.")
            # Reset session state related to the invalid image
            st.session_state.image_path = None
            st.session_state.image_analyzed = False
            st.session_state.image_info = ""
        else:
            st.success("[Guardrails] ✅ Image is safe and ready for questions.")
            st.session_state.image_analyzed = True # Mark that a valid image is ready

# --- Main Chat Interface ---
st.header("Chat with the AI")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle chat input (now always available)
if prompt := st.chat_input("Ask about the image or start a new conversation..."):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # All subsequent logic must be inside this block to run correctly
    
    # Moderate the user's prompt
    with st.spinner('Guardrail: Checking prompt safety...'):
        moderation = TextModerationAgent()
        is_safe = moderation.is_safe(prompt)
    
    if not is_safe:
        st.error("[Guardrails] ❌ Malicious prompt detected. Request blocked.")
        # Remove the unsafe message from history and stop further processing
        st.session_state.messages.pop()
    else:
        st.success("[Guardrails] ✅ Prompt is safe.")
        # Determine the correct agent workflow
        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                final_response = ""
                language_agent = LanguageAgent()
                history = st.session_state.messages[:-1]  # Get history before the current prompt

                # If an image is present, use the hybrid VQA + Language Model workflow
                if st.session_state.image_analyzed and st.session_state.image_path:
                    # Step 1: Get factual answer from the Vision Agent
                    vision_agent = VisionAgent()
                    vqa_answer = vision_agent.answer_question(st.session_state.image_path, prompt)
                    
                    # Step 2: Create a new system prompt with the VQA context for the Language Agent
                    image_context_prompt = (
                        f"You are a helpful AI assistant. The user has uploaded an image and asked a question about it. "
                        f"A vision model has analyzed the image and provided the following answer: '{vqa_answer}'. "
                        f"Based on this information and the conversation history, please provide a helpful and conversational response to the user's prompt: '{prompt}'."
                    )
                    
                    # Add the special context to the beginning of the history for this call
                    history.insert(0, {"role": "system", "content": image_context_prompt})
                    response = language_agent.get_response(prompt, history)
                    final_response = response
                else:
                    # Otherwise, use the standard Language Agent workflow for general conversation
                    response = language_agent.get_response(prompt, history)
                    
                    # Check for and execute actions from the language model's response
                    action_agent = ActionAgent()
                    action_response = action_agent.execute_action(response)
                    final_response = action_response if action_response else response

                st.markdown(final_response)
                # Add the assistant's response to the message history
                st.session_state.messages.append({"role": "assistant", "content": final_response})
