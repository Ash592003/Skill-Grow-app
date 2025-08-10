import streamlit as st

# === Page Config ===
st.set_page_config(page_title="SkillGrow | Career Onboarding", layout="centered")

# === Redirect if a page is chosen ===
if "navigate" in st.session_state:
    if st.session_state.navigate == "resume":
        st.switch_page("pages/frontend.py")
    elif st.session_state.navigate == "manual":
        st.switch_page("pages/mannual_entry.py")
    elif st.session_state.navigate == "quiz":
        st.switch_page("pages/personality_quiz.py")

# === Branding Header ===
st.markdown("""
<div style='text-align: center;'>
    <h1 style='color:#824EF3;'>Welcome to SkillGrow👋</h1>
    <p>🧠 <b>Skill Mapping</b> | 🎯 <b>Personalized Recommendation</b> | 🔥 <b>Fuzzy Matching</b></p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# === Custom CSS Styling ===
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right, #004d4d, #c1a36f);
    font-family: 'Inter', sans-serif;
    color: white !important;
}
h1, h2, h3, h4 {
    color: white !important;
    text-align: center;
}
p, label, .stMarkdown {
    color: white !important;
}
input, textarea {
    background-color: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.2) !important;
}
input::placeholder, textarea::placeholder {
    color: rgba(255,255,255,0.6) !important;
}
button.proceed-btn {
    background-color: #ff4d4d;
    color: white !important;
    font-weight: bold;
    padding: 10px 24px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    transition: transform 0.2s ease;
    width: 100%;
}
button.proceed-btn:hover {
    background-color: #e04343;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

# === Radio Options ===
choice = st.radio("Start with:", [
    "📄 Upload Resume",
    "✍️ Manual Entry",
    "🧩 Personality Quiz"
])

# === Proceed Button Logic ===
if st.button("Proceed", key="proceed", type="primary"):
    if "Upload" in choice:
        st.session_state.navigate = "resume"
    elif "Manual" in choice:
        st.session_state.navigate = "manual"
    elif "Personality" in choice:
        st.session_state.navigate = "quiz"
    st.rerun()

st.markdown("---")
st.caption("✨ Powered by SkillGrow Intelligence")
