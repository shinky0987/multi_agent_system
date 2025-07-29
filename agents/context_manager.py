# agents/context_manager.py

class ContextManager:
    def __init__(self):
        """Initializes the ContextManager with an empty history."""
        self.history = []

    def add_message(self, role: str, content: str):
        """Adds a message to the conversation history."""
        self.history.append({"role": role, "content": content})

    def get_history(self) -> list:
        """Returns the current conversation history."""
        return self.history

    def clear(self):
        """Clears the conversation history."""
        self.history = []