import streamlit as st
import requests 
import json

# === Chat-Like AI Career Counselor ===
st.markdown("---")
st.header("🧑‍🎓 Career Mentor")
openrouter_api_key = "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"

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right, #004d4d, #c1a36f); /* Ancient Teal to Gold */
    font-family: 'Inter', sans-serif;
    color: white !important;
}

/* Headers & Global Text (still centered for main headings) */
h1, h4, p, label, .stMarkdown, .css-1cpxqw2, .css-qrbaxs, .css-1offfwp, .css-1kyxreq {
    color: white !important;
    text-align: center;
}

/* Subheadings Left-Aligned */
h2, h3 {
    color: white !important;
    text-align: left !important;
    margin-left: 8px;
}

/* Inputs */
input, textarea, .stTextInput, .stTextArea {
    background-color: rgba(255,255,255,0.08) !important;
    color: black !important; /* Black text inside inputs for readability */
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

/* Placeholder text styling */
input::placeholder, textarea::placeholder {
    color: rgba(0,0,0,0.5) !important; /* Slightly faded black for contrast */
}

/* Red Button Styling */
div.stButton > button:first-child {
    background-color: #ff4d4d !important;
    color: white !important;
    font-weight: bold;
    padding: 10px 24px;
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    transition: transform 0.2s ease;
}

div.stButton > button:first-child:hover {
    background-color: #e04343 !important;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

chat_query = st.text_area("💬 Ask your education or career-related question (e.g. 'What are top skills for UX Designer?')")

if st.button("🗨️ Ask Career mentor") and chat_query:
    with st.spinner("🎯 Thinking through your question..."):
        counselor_prompt = f"""You're an expert career counselor. Answer only career and education-related queries.
Only give advice aligned to career planning, skill development, job readiness, resume improvement, upskilling, course recommendations, etc.

User Question: {chat_query}

Respond in a friendly, helpful, and encouraging tone. Be specific, use bullet points where helpful, and avoid irrelevant content."""
        
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": counselor_prompt}]
        }

        headers = {
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json"
        }

        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            res.raise_for_status()
            answer = res.json()["choices"][0]["message"]["content"]
            st.markdown("### 🎓 Career Counselor’s Reply")
            st.markdown(answer)
        except Exception as e:
            st.error("❌ Failed to get response from AI counselor.")
            st.code(str(e), language="bash")