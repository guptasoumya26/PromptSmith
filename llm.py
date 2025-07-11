import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_llm_answer(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {e}]"

def analyze_answers(orig, refined):
    prompt = f"Compare these two answers.\nAnswer 1: {orig}\nAnswer 2: {refined}\nScore each out of 10 and explain which is better."
    return get_llm_answer(prompt)

def explain_refinement(orig_prompt, refined_prompt):
    prompt = f"Original: {orig_prompt}\nRefined: {refined_prompt}\nExplain why the refined prompt is better."
    return get_llm_answer(prompt)
