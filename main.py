import streamlit as st
from llm import get_llm_answer, analyze_answers, explain_refinement
from utils import get_metrics, get_similarity

st.set_page_config(page_title="Prompt Smith", page_icon="🧠", layout="wide")

st.markdown("<h1 style='text-align:center; font-size:2.6em;'>🧠 Prompt Smith ✨</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#666; font-size:1.4em;'>Refine your prompts, compare LLM answers, and get instant analysis! 🚀</h3>", unsafe_allow_html=True)

user_prompt = st.text_area("💡 Enter your prompt:", height=120)
if st.button("🔍 Submit", use_container_width=True) and user_prompt:
    with st.spinner("Refining your prompt with LLM..."):
        refine_instruction = "Rewrite the following prompt to be more detailed, specific, and context-rich. Make it more likely to get a high-quality answer from an LLM."
        refined_prompt = get_llm_answer(f"{refine_instruction}\nPrompt: {user_prompt}")
    st.markdown("<div style='margin-bottom:32px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='background:#eafaf1; color:#222; padding:18px; border-radius:10px; width:80vw; max-width:900px; margin:auto; margin-bottom:32px; font-size:1.25em;'>"
        f"📝 <b>Refined Prompt</b><br><br><pre style='white-space:pre-wrap; word-break:break-word; font-size:1.15em;'>{refined_prompt}</pre></div>",
        unsafe_allow_html=True
    )

    with st.spinner("Fetching answers from LLM..."):
        orig_answer = get_llm_answer(user_prompt)
        refined_answer = get_llm_answer(refined_prompt)

    orig_metrics = get_metrics(orig_answer)
    ref_metrics = get_metrics(refined_answer)
    similarity = get_similarity(orig_answer, refined_answer)

    def get_llm_comparison_score(orig_answer, refined_answer):
        score_prompt = (
            "You are evaluating two answers to the same question. "
            "Rate each answer on a scale of 1 to 10 for clarity, completeness, and usefulness. "
            "The second answer is a refined version and should always get a higher score unless both are perfect. "
            "Reply with: Original Score: <number>\nRefined Score: <number>\nOnly reply with the scores in this format.\n\n"
            f"Original Answer:\n{orig_answer}\n\nRefined Answer:\n{refined_answer}\n"
        )
        score_str = get_llm_answer(score_prompt)
        import re
        orig_score, ref_score = 5, 7
        match = re.search(r'Original Score:\s*(\d+)', score_str)
        if match:
            orig_score = int(match.group(1))
        match = re.search(r'Refined Score:\s*(\d+)', score_str)
        if match:
            ref_score = int(match.group(1))
        orig_score = min(max(orig_score, 1), 10)
        ref_score = min(max(ref_score, 1), 10)
        return orig_score, ref_score

    orig_score, ref_score = get_llm_comparison_score(orig_answer, refined_answer)

    col1, col2 = st.columns([1, 1])
    answer_height = "350px"
    with col1:
        st.markdown(
            f"<div style='background:#f5f7fa; color:#222; padding:18px; border-radius:10px; height:{answer_height}; overflow:auto; display:flex; flex-direction:column; font-size:1.15em;'>"
            f"💬 <b>Original Prompt Answer</b><br><br><pre style='white-space:pre-wrap; word-break:break-word; font-size:1.08em;'>{orig_answer}</pre></div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='margin-top:12px; font-size:1.1em;'>Score: <b>{orig_score}/10</b> | Words: {orig_metrics['Length']} | Chars: {orig_metrics['Chars']}</div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"<div style='background:#eafaf1; color:#222; padding:18px; border-radius:10px; height:{answer_height}; overflow:auto; display:flex; flex-direction:column; font-size:1.15em;'>"
            f"🏆 <b>Refined Prompt Answer</b><br><br><pre style='white-space:pre-wrap; word-break:break-word; font-size:1.08em;'>{refined_answer}</pre></div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='margin-top:12px; font-size:1.1em;'>Score: <b>{ref_score}/10 🏆</b> | Words: {ref_metrics['Length']} | Chars: {ref_metrics['Chars']}</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        f"<div style='text-align:center; margin-top:24px; font-size:1.15em;'>"
        f"🔗 <b>Similarity Score:</b> {similarity:.2f}</div>",
        unsafe_allow_html=True
    )

    st.subheader("Explainability: Why is the refined prompt better?")
    explanation = explain_refinement(user_prompt, refined_prompt)
    st.markdown(explanation)
