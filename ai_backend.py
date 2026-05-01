<<<<<<< HEAD
# ============================================
# StudyMate AI - Unified AI Backend
# Supports: Ollama (local), Gemini, Groq
# ============================================

import os
from dotenv import load_dotenv
load_dotenv()


def chat(prompt, system_prompt=None):
    """
    Universal chat function.
    AI_BACKEND options: ollama / gemini / groq
    """
    backend = os.getenv("AI_BACKEND", "ollama")

    # ── GROQ (Free Cloud) ──
    if backend == "groq":
        try:
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
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
            response = client.chat.completions.create(
                model=os.getenv(
                    "GROQ_MODEL", "llama-3.1-8b-instant"
                ),
                messages=messages,
                max_tokens=4096
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Groq Error: {str(e)}"

    # ── GEMINI (Google) ──
    elif backend == "gemini":
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
                model=os.getenv(
                    "GEMINI_MODEL", "gemini-1.5-flash"
                ),
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
=======
# ============================================
# StudyMate AI - Unified AI Backend
# Supports: Ollama (local), Gemini, Groq
# ============================================

import os
from dotenv import load_dotenv
load_dotenv()


def chat(prompt, system_prompt=None):
    """
    Universal chat function.
    AI_BACKEND options: ollama / gemini / groq
    """
    backend = os.getenv("AI_BACKEND", "ollama")

    # ── GROQ (Free Cloud) ──
    if backend == "groq":
        try:
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
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
            response = client.chat.completions.create(
                model=os.getenv(
                    "GROQ_MODEL", "llama-3.1-8b-instant"
                ),
                messages=messages,
                max_tokens=4096
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Groq Error: {str(e)}"

    # ── GEMINI (Google) ──
    elif backend == "gemini":
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
                model=os.getenv(
                    "GEMINI_MODEL", "gemini-1.5-flash"
                ),
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
>>>>>>> b09323630fd2f2924f4f0231828396c7cbd43d21
            return f"Ollama Error: {str(e)}"