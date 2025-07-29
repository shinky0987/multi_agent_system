# agents/action_agent.py

import re
import webbrowser
import os

class ActionAgent:
    def execute_action(self, response: str) -> str:
        """Extracts and performs an action, returning a status message or None."""
        action_details = self._extract_action(response)
        
        if action_details["action"] == "unknown":
            return None # No action found, return None to indicate original response should be used

        return self._perform_action(action_details)

    def _extract_action(self, response: str) -> dict:
        """Extracts an action and its parameters from the response using regex."""
        response = response.lower()
        patterns = {
            'search': r"(search|open browser)(?: for)? (.+)",
            'open_file': r"open (?:the )?file (.+)",
        }
        
        for action, pattern in patterns.items():
            match = re.search(pattern, response)
            if match:
                if action == 'search':
                    return {"action": action, "params": {"query": match.group(2).strip()}}
                elif action == 'open_file':
                    filename = match.group(1).strip('"\' `')
                    return {"action": action, "params": {"filename": filename}}
        
        return {"action": "unknown", "params": {}}

    def _perform_action(self, action_details: dict) -> str:
        """
        Performs a validated action. For a web app, direct execution is a security risk.
        This implementation returns descriptive messages instead of executing.
        """
        action = action_details.get("action")
        params = action_details.get("params", {})
        
        if action == "search":
            query = params.get('query')
            # This is a placeholder. In a real web app, you wouldn't use webbrowser.
            # webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"[Action Agent] Simulating a search for: '{query}'. In a real app, this would open a new tab."
        
        elif action == "open_file":
            filename = params.get('filename')
            return f"[Action Agent] Simulating opening the file: '{filename}'. This is a restricted action in a web environment."

        return f"[Action Agent] Action '{action}' is recognized but not implemented."
