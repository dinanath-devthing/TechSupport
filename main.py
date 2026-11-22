import os
import re
from dotenv import load_dotenv
from google import genai
from utils.config import SYSTEM_PROMPT

load_dotenv()

class TechSupportChat:
    
    def __init__(self, api_key=None, max_history=15):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash"
        self.conversation_history = []
        self.max_history = max_history
        self.troubleshooting_state = {
            "user_os": None,
            "user_device": None,
            "issue_type": None,
            "attempted_solutions": [],
            "user_tech_level": "unknown",
            "system_info": {},
            "current_step": None,
            "escalation_needed": False,
        }
    
    def add_to_history(self, role, content, metadata=None):
        message = {"role": role, "content": content, "metadata": metadata or {}}
        self.conversation_history.append(message)

        if len(self.conversation_history) > self.max_history:
            system_messages = [
                item for item in self.conversation_history
                if item.get("role") == "system"
            ]
            non_system_messages = [
