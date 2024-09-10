import openai
from config.config import openai_api_key

class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls.client = openai.OpenAI(api_key=openai_api_key)
        return cls._instance

    def ai_assistant(self, prompt):
        refined_prompt = (
            f"As Alfred, Batman's trusted butler, you must always respond politely and respectfully to the user's input. "
            "For commands that involve system actions (like creating, deleting, or searching for files), interpret the command clearly and provide the required action. "
            "For general questions or non-actionable requests, provide helpful and conversational responses. "
            "Always maintain the tone of Alfred—polite, helpful, and slightly witty."
        )

        # Making the request to OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": refined_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Access the 'content' attribute directly
        return response.choices[0].message.content.strip()
