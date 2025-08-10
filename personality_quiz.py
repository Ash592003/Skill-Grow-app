import streamlit as st
import requests
import json
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ✅ Set your API key
openrouter_api_key = "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"

# === PDF Generator ===
def generate_pdf(content, goal):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "SkillGrow Career Personality Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Career Aspiration: {goal}")

    c.setFont("Helvetica", 11)
    y = height - 100
    for line in content.split("\n"):
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)
        c.drawString(50, y, line.strip())
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer

# === Styling ===
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right, #004d4d, #c1a36f);
    font-family: 'Inter', sans-serif;
    color: white !important;
}
h1, h4, p, label, .stMarkdown, .css-1cpxqw2, .css-qrbaxs, .css-1offfwp, .css-1kyxreq {
    color: white !important;
    text-align: center;
}
h2, h3 {
    color: white !important;
    text-align: left !important;
    margin-left: 8px;
}
input, textarea, .stTextInput, .stTextArea {
    background-color: rgba(255,255,255,0.08) !important;
    color: black !important;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.2) !important;
}
input::placeholder, textarea::placeholder {
    color: rgba(0,0,0,0.5) !important;
}
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

# 🎯 Quiz Logic
def run_quiz():
    with st.form("quiz_form"):
        st.write("✨ Quick Career Preference Survey")
        q1 = st.radio("Do you prefer working with data or people?", ["Data", "People"])
        q2 = st.slider("Enjoy solving technical problems?", 1, 5)
        q3 = st.radio("Are you more analytical or creative?", ["Analytical", "Creative"])
        submitted = st.form_submit_button("Submit")
    if submitted:
        career_type = "Tech/Data" if q1 == "Data" and q2 >= 4 else "People-Focused"
        trait = q3
        return {"career_focus": career_type, "personality_trait": trait}
    return None

# 🎨 Streamlit Layout
st.title("Career Personality Quiz 🎯")

# Section 1: Career Aspiration & Motivation
st.header("Your Motivation & Career Goals")
goal = st.text_input("✨ What's your ideal career 5 years from now?")
success_def = st.radio(
    "🌟 How do you define success in your career?",
    ["Making an impact", "Achieving financial security", "Becoming a subject matter expert", "Leading teams", "Building something new"]
)
values = st.multiselect(
    "💬 Which of these values are most important to you?",
    ["Innovation", "Stability", "Flexibility", "Recognition", "Growth", "Autonomy"]
)

# Section 2: Work Style & Preference
st.header("Your Work Preferences")
work_mode = st.radio("🤝 Do you prefer working:", ["Independently", "In collaborative teams", "Flexible depending on the task"])
challenge_pref = st.selectbox(
    "⚙ What kind of tasks excite you most?",
    ["Solving complex problems", "Designing creative solutions", "Building systems/tools", "Communicating insights", "Organizing projects"]
)
environment = st.radio("🏢 What work environment suits you best?", ["Startup", "Corporate", "Academia", "Freelance", "Government"])

# Section 3: Current Skill Readiness
st.header("Your Current Tech Confidence")
python_conf = st.slider("🐍 How confident are you with Python?", 0, 5, 2)
sql_conf = st.slider("🗃 SQL confidence level", 0, 5, 3)
spreadsheet_conf = st.slider("📊 Spreadsheet skills (Excel/Google Sheets)", 0, 5, 4)
Email_Etiquette_conf = st.slider("📧 Email etiquette and communication", 0, 5, 3)
project_exp = st.radio("🧪 Have you built any personal or group projects?", ["Yes", "No", "In Progress"])

# Section 4: Personality Tendencies
st.header("Behavioral Tendencies")
openness = st.radio("🧠 How do you react to new tools or workflows?", ["Excited to try", "Cautious but curious", "Prefer stability"])
resilience = st.selectbox(
    "🛠 What do you do when something goes wrong in a project?",
    ["Reflect and retry", "Ask for help", "Drop and switch tasks", "Stick to original plan no matter what"]
)
planning_style = st.radio("📅 Planning style:", ["Detailed planner", "Flexible improviser", "Deadline-driven", "Task-list centric"])

# Section 5: Career Commitment & Growth Mindset
st.header("Career Commitment & Growth Mindset")

certification_freq = st.radio("🎓 How often do you pursue certifications?", [
    "Regularly", "Occasionally", "Rarely", "Never"
])

learn_proactively = st.radio("📚 I actively seek to learn skills for my dream job", [
    "Always", "Often", "Sometimes", "Rarely"
])

extra_effort = st.radio("⏱ Willing to work extra hours for career growth", [
    "Absolutely", "If needed", "Prefer balance", "Not really"
])

follow_trends = st.radio("📰 I follow news and trends in my target career", [
    "Frequently", "Sometimes", "Rarely", "Never"
])

take_risks = st.radio("🚀 I take on tasks outside my comfort zone", [
    "Often", "Sometimes", "Rarely", "Avoid them"
])

career_plan = st.radio("🗺 I have a clear plan to reach my career goal", [
    "Yes", "Somewhat", "Not yet"
])

energized_by_work = st.radio("⚡ I feel energized working on career-related tasks", [
    "Always", "Often", "Sometimes", "Rarely"
])

bounce_back = st.radio("💪 I stay committed despite setbacks", [
    "Always", "Usually", "Sometimes", "Struggle with it"
])

invested_resources = st.radio("💰 I've invested time/money to prepare for my dream job", [
    "Yes", "Somewhat", "Not yet"
])

seek_feedback = st.radio("🧠 I actively seek feedback to improve", [
    "Regularly", "Occasionally", "Rarely", "Avoid it"
])

short_term_goals = st.radio("🎯 I set short-term goals toward my career", [
    "Consistently", "Sometimes", "Rarely", "Never"
])

# 🧠 AI Feedback Generator using OpenRouter
def generate_feedback_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 400
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()
    return result["choices"][0]["message"]["content"]

# 🎉 Final Submission Button
if st.button("Submit Quiz"):
    if goal and values:
        prompt = f"""
You are an encouraging career advisor. Based on the user's responses to a career quiz, generate an insightful, motivational analysis including:

1. Their passion and motivation level based on career aspiration and energy indicators.
2. Traits like creativity, analytical thinking, and planning style.
3. Technical readiness: Python, SQL, spreadsheets, email etiquette, and project experience.
4. Behavioral tendencies: openness, resilience, risk-taking, and feedback-seeking.
5. Growth mindset indicators: certifications, learning habits, extra effort, trend-following, goal-setting, and resource investment.
6. Highlight areas of strength clearly.
7. If any responses show low motivation, unclear planning, or lack of effort — mention it constructively and offer realistic suggestions.
8. Keep tone warm, honest, and growth-oriented. Use emojis sparingly and only to reinforce positivity.

Responses:
- Career aspiration: {goal}
- Definition of success: {success_def}
- Core values: {', '.join(values)}
- Python confidence: {python_conf}/5
- SQL confidence: {sql_conf}/5
- Spreadsheet confidence: {spreadsheet_conf}/5
- Email etiquette: {Email_Etiquette_conf}/5
- Project experience: {project_exp}
- Openness to new tools: {openness}
- Resilience behavior: {resilience}
- Task preference: {challenge_pref}
- Planning style: {planning_style}
- Certification frequency: {certification_freq}
- Learning initiative: {learn_proactively}
- Extra effort willingness: {extra_effort}
- Trend following: {follow_trends}
- Risk-taking: {take_risks}
- Career planning: {career_plan}
- Energized by work: {energized_by_work}
- Bounce-back ability: {bounce_back}
- Resource investment: {invested_resources}
- Feedback seeking: {seek_feedback}
- Short-term goals: {short_term_goals}


Keep the tone supportive, growth-oriented, and concise (under 300 words). Use emojis sparingly but warmly.
"""
        try:
            feedback = generate_feedback_openrouter(prompt)
            st.success("✅ Response recorded!")

            tab1, tab2 = st.tabs(["🧭 Personalized Feedback", "📥 Download PDF"])

            with tab1:
                st.markdown("### 🧭 Personalized Feedback")
                st.write(feedback)

            with tab2:
                pdf_buffer = generate_pdf(feedback, goal)
                st.download_button(
                    label="Download Feedback as PDF",
                    data=pdf_buffer,
                    file_name=f"{goal}_Career_Feedback.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error("❌ Error during analysis.")
            st.code(str(e), language="bash")
    else:
        st.warning("⚠ Please fill out all sections before submitting.")