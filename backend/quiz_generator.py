import os
import requests
from dotenv import load_dotenv
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

OLLAMA_HOST = os.getenv("HOST")


class QuizGenerator:
    """
    A class to generate quiz questions using a local LLM model via the Ollama API.
    """
    def __init__(self, ollama_model="llama3", host=OLLAMA_HOST):
        # Ensure host always contains a valid scheme for requests
        self.model = ollama_model
        self.host = host

    def generate_quiz_question(self, topic: str) -> str:
        """
        Generates a multiple-choice quiz question on the given topic using local LLaMA 3 via Ollama.
        This is an instance method and MUST be called on a QuizGenerator object (e.g., generator.generate_quiz_question(topic)).
        """
        if not self.host:
            logging.error("OLLAMA_HOST environment variable is not set in the instance.")
            return "Error: OLLAMA_HOST environment variable is not set."

        prompt = f"""You are a quiz generator.

    Create one high-quality multiple-choice quiz question (with 4 options) based on the topic: "{topic}".
    Clearly indicate the correct answer.

    Format:
    Question:
    A.
    B.
    C.
    D.
    Answer:
    """
        api_url = f"{self.host}/api/generate"
        print(api_url)

        try:
            # Note: The original code used OLLAMA_HOST which might not be defined if called statically.
            # We now correctly use self.host from the instance.
            response = requests.post(
                api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30 # Add a timeout for better resource management
            )

            # 1. Check HTTP Status Code
            if response.status_code != 200:
                error_msg = f"Error from Ollama server (Status {response.status_code}): {response.text}"
                logging.error(error_msg)
                return error_msg

            # 2. Extract Response
            return response.json().get("response", "No 'response' key in LLaMA 3 output.")

        # 3. Handle specific request exceptions (network, timeout)
        except requests.exceptions.RequestException as e:
            error_message = f"Network/connection error with LLaMA 3 at {api_url}: {e}"
            logging.error(error_message)
            return error_message

        # 4. Handle other unexpected errors (e.g., JSON parsing)
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            logging.error(error_message, exc_info=True)
            return error_message
