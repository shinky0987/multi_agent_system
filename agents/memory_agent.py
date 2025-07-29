class MemoryAgent:
    def __init__(self):
        self.context = ""

    def update_context(self, new_info):
        self.context += " " + new_info

    def get_context(self):
        return self.context.strip()
