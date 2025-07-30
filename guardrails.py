# guardrails.py

import re
import logging
from PIL import Image
from agents.vision_moderation_agent import VisionModerationAgent
from agents.text_moderation_agent import TextModerationAgent

# Setup logging
logging.basicConfig(
    filename='guardrails.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Allowed agent actions, aligned with action_agent.py
# --- Action Guardrails Configuration ---
# 1. Allowed action types
allowed_actions = {"search", "open_file", "shutdown", "unknown"}

# 2. Parameter-level validation rules
allowed_filenames = {"example.txt", "document.txt", "notes.txt"} # Whitelist of safe files
disallowed_path_keywords = ["..", "/", "\\", ":"] # Prevent path traversal

def is_malicious_text(text: str) -> (bool, str):
    """Check for malicious text using an AI moderation agent and pattern matching."""
    try:
        moderation_agent = TextModerationAgent()
        is_harmful, reason = moderation_agent.is_malicious(text)
        if is_harmful:
            logging.warning(f"Blocked malicious text (reason: {reason}): {text[:100]}...")
            return True, reason
        logging.info(f"Text passed moderation check: {text[:50]}...")
        return False, "safe"
    except Exception as e:
        logging.error(f"Error during text moderation: {e}")
        return True, f"moderation_error: {str(e)}" # Fail safe and block the query

def is_safe_image_content(image_path: str) -> bool:
    """Check if the image content is safe (not NSFW)."""
    try:
        moderation_agent = VisionModerationAgent()
        label = moderation_agent.moderate_image(image_path)
        if label == 'nsfw':
            logging.warning(f"Blocked unsafe image content: {image_path} (classified as NSFW)")
            return False
        return True
    except Exception as e:
        logging.error(f"Error during image content moderation for {image_path}: {e}")
        return False # Fail safe

def is_valid_image(image_path: str) -> bool:
    """Validate the image file format and content."""
    try:
        # 1. Validate format
        img = Image.open(image_path)
        img.verify() # Checks for file integrity

        # 2. Validate content
        if not is_safe_image_content(image_path):
            return False
            
        return True
    except Exception as e:
        logging.warning(f"Blocked invalid image file {image_path}: {e}")
        return False

def validate_action(action_details: dict) -> (bool, str):
    """Ensure the agent is allowed to perform an action and its parameters are safe."""
    action = action_details.get("action")
    params = action_details.get("params", {})

    # 1. Check if the action type is allowed
    if action not in allowed_actions:
        reason = f"Action '{action}' is not in the list of allowed actions."
        logging.warning(f"Blocked illegal action: {reason}")
        return False, reason

    # 2. Perform parameter-level validation
    if action == 'open_file':
        filename = params.get('filename')
        if not filename:
            return False, "Filename not specified for open_file action."
        # Block path traversal attempts
        if any(keyword in filename for keyword in disallowed_path_keywords):
            return False, f"Path traversal attempt blocked in filename: '{filename}'."
        # Check against whitelist
        if filename not in allowed_filenames:
            return False, f"File '{filename}' is not in the list of allowed files."

    elif action == 'search':
        query = params.get('query')
        if not query:
            return False, "Search query not specified."
        # Extra safety: check the search query for malicious intent
        is_harmful, reason = is_malicious_text(query)
        if is_harmful:
            return False, f"Malicious content detected in search query: '{query}'."

    # If all checks pass
    return True, "Action is safe."
