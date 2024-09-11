import openai
from config.config import openai_api_key
from src.system_commands.folder_file_operations import create_folder, create_file
import json

class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls.client = openai.OpenAI(api_key=openai_api_key)
        return cls._instance

    def ai_assistant(self, prompt):
        refined_prompt = (
            f"As Alfred, Batman's trusted butler, whose been given to Zack now, you must always respond politely and respectfully to the user's input. "
            "For commands that involve system actions (like creating, deleting, or searching for files), interpret the command clearly and provide the required action. "
            "For general questions or non-actionable requests, provide helpful and conversational responses. "
            "Always maintain the tone of Alfred—polite, helpful, and slightly witty."
        )

        # Define the available functions for function calling
        functions = [
            {
                "name": "create_folder",
                "description": "Create a folder at the given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "folder_name": {"type": "string", "description": "The name of the folder to create."},
                        "path": {"type": "string", "description": "The path where the folder should be created."}
                    },
                    "required": ["folder_name"]
                }
            },
            {
                "name": "create_file",
                "description": "Create a file at the given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {"type": "string", "description": "The name of the file to create."},
                        "path": {"type": "string", "description": "The path where the file should be created."}
                    },
                    "required": ["file_name"]
                }
            }
        ]

        # Send the request to OpenAI with function calling
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": refined_prompt},
                {"role": "user", "content": prompt}
            ],
            functions=functions,
            function_call="auto"
        )

        # Get the message object from the response
        message = response.choices[0].message

        # Check if the response includes a function call
        if message.function_call:
            # Dynamic response before the action is performed
            pre_action_response = "I'll get right on that, Master Zack."

            function_name = message.function_call.name
            arguments = json.loads(message.function_call.arguments)

            # Handle function calling logic
            if function_name == "create_folder":
                action_result = create_folder(arguments["folder_name"], arguments.get("path", "."))
                # Dynamic response after the action is completed
                post_action_response = f"The folder '{arguments['folder_name']}' has been successfully created, sir."
                return f"{pre_action_response}\n{post_action_response}"
            elif function_name == "create_file":
                action_result = create_file(arguments["file_name"], arguments.get("path", "."))
                post_action_response = f"The file '{arguments['file_name']}' has been created, sir."
                return f"{pre_action_response}\n{post_action_response}"

        # Return the regular conversational response if available
        if hasattr(message, "content") and message.content:
            return message.content

        # Fallback only if neither function nor content is found
        return "I couldn't quite catch that, Master Zack. Could you rephrase?"
