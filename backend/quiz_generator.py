import requests

def generate_quiz_question(topic: str) -> str:
    """
    Generates a multiple-choice quiz question on the given topic using local LLaMA 3 via Ollama.
    """
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

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False  # Get full response at once
            }
        )
        return response.json().get("response", "No response from LLaMA 3")

    except Exception as e:
        return f"Error communicating with LLaMA 3: {e}"

