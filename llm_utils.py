import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def get_openai_answer(prompt):
    if not OPENAI_API_KEY:
        return "[No API key provided]"
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {e}]"

def analyze_answers(original, refined):
    if not OPENAI_API_KEY:
        return "[No API key provided]"
    prompt = (
        f"Compare the following two answers.\n"
        f"Answer 1: {original}\n"
        f"Answer 2: {refined}\n"
        "Provide a brief analysis of which answer is better and why, and give a score out of 10 for each answer."
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {e}]"

def explain_refinement(original_prompt, refined_prompt):
    if not OPENAI_API_KEY:
        return "[No API key provided]"
    prompt = (
        f"Original prompt: {original_prompt}\nRefined prompt: {refined_prompt}\n"
        "Explain in a few sentences why the refined prompt is likely to produce a better answer."
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=128
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {e}]"
