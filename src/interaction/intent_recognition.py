from src.openai.openai_client import OpenAIClient

class IntentRecognition:
    def __init__(self):
        self.openai_client = OpenAIClient()

    def recognize_intent(self, prompt):
        """
        Analyzes the user's input to recognize the intent.
        Returns an action for system commands or identifies it as a general question.
        """
        openai_response = self.openai_client.ai_assistant(prompt)

        # Debugging: print the OpenAI response for general questions
        print(f"DEBUG: OpenAI Response: {openai_response}")

        # Recognize commands
        if "create" in prompt.lower() and "folder" in prompt.lower():
            print(f"DEBUG: Recognized intent to create a folder with prompt: {prompt}")
            return "create_folder", None
        elif "delete" in prompt.lower() and "file" in prompt.lower():
            return "delete_file", None
        elif "open" in prompt.lower() and "file" in prompt.lower():
            return "open_file", None
        elif "locate" in prompt.lower() and "folder" in prompt.lower():
            return "find_folder", openai_response
        else:
            return "general_question", openai_response

    def generate_action(self, intent, prompt):
        """
        Takes the recognized intent and generates both a system command and a conversational response.
        """
        if intent == "create_folder":
            action = f"Command to create folder generated for: {prompt}"
            response = "I’ll create that folder right away, Master Wayne."
            print(f"DEBUG: Action ready to create folder: {prompt}")  # Logs folder creation action
        elif intent == "delete_file":
            action = f"Command to delete file generated for: {prompt}"
            response = "I’ll delete that file for you now, Master Wayne."
        elif intent == "open_file":
            action = f"Command to open file generated for: {prompt}"
            response = "Opening that file, as you requested."
        elif intent == "find_folder":
            action = f"Command to find folder generated for: {prompt}"
            response = intent[1]
        else:
            action = ""
            response = intent[1]

        return f"{response}\n{action}" if action else f"{response}"
