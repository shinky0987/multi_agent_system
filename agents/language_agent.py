import requests
import os
from dotenv import load_dotenv

load_dotenv()

class LanguageAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_response(self, prompt: str, history: list) -> str:
        """Calls the Groq API with the given prompt and conversation history."""
        if not self.api_key:
            return "[Language Agent] Error: GROQ_API_KEY is not set."

        # Combine history with the new prompt
        messages = history + [{"role": "user", "content": prompt}]

        # Ensure a system prompt is present
        if not any(msg['role'] == 'system' for msg in messages):
            messages.insert(0, {"role": "system", "content": "You are a helpful AI assistant."})

        payload = {
            "model": "llama3-70b-8192",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            return f"[Language Agent] Error connecting to API: {e}"
        except (KeyError, IndexError) as e:
            return f"[Language Agent] Error parsing API response: {e}"
