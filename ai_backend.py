# ============================================
# StudyMate AI - Unified AI Backend
# Works with Ollama (local) and Gemini (cloud)
# ============================================

import os


def chat(prompt, system_prompt=None):
    """
    Single function that works with both Ollama and Gemini.
    Set AI_BACKEND=gemini in environment for cloud deployment.
    Default is ollama for local development.
    """
    backend = os.getenv("AI_BACKEND", "ollama")

    # ── GEMINI (Cloud) ──
    if backend == "gemini":
        try:
            from google import genai
            client = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
            )
            full_prompt = (
                f"{system_prompt}\n\n{prompt}"
                if system_prompt else prompt
            )
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=full_prompt
            )
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"

    # ── OLLAMA (Local) ──
    else:
        try:
            import ollama
            messages = []
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            messages.append({
                "role": "user",
                "content": prompt
            })
            response = ollama.chat(
                model=os.getenv("OLLAMA_MODEL", "gemma3:4b"),
                messages=messages
            )
            return response["message"]["content"]
        except Exception as e:
            return f"Ollama Error: {str(e)}"