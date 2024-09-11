from src.openai.openai_client import OpenAIClient

class IntentRecognition:
    def __init__(self):
        self.openai_client = OpenAIClient()

    def recognize_intent(self, prompt):
        """
        Passes the prompt to OpenAI and receives either a conversational response or a function call.
        """
        openai_response = self.openai_client.ai_assistant(prompt)

        return openai_response
