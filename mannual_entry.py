import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# === CONFIG ===
openrouter_api_key = "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"
backend_path = "C:/Users/ashwi/OneDrive/Desktop/VS code streamlit/data.xlsx"

# === PDF Generator ===
def generate_pdf(content, candidate_name):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"SkillGrow Career Advisory Report for {candidate_name}")

    c.setFont("Helvetica", 11)
    y = height - 80
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

# === Custom Styling ===
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

# === Load Backend Skill Library ===
df_skills = pd.read_excel(backend_path)
df_skills['skill library'] = df_skills['skill library'].apply(lambda x: [s.strip().lower() for s in str(x).split(",")])
available_roles = df_skills['Career Aspiration'].dropna().unique().tolist()

# === Streamlit Setup ===
st.set_page_config(page_title="SkillGrow | Manual Entry + AI", layout="centered")
st.title("SkillGrow Manual Analyzer")

# === Personal & Education Info ===
st.header("👤 Personal Information")
name = st.text_input("Full Name")

st.header("🎓 Education")
highest_edu = st.selectbox("Highest Completed Education", ["High School", "Diploma", "Bachelor's", "Master's", "PhD"])
current_edu = st.text_input("Currently Pursuing (if any)")
student_year = st.selectbox("Year of Study", ["1st Year", "2nd Year", "3rd Year", "Final Year", "Graduate"])
stream = st.selectbox("Academic Stream", ["Computer Science", "Data Science", "Electronics", "Business", "Arts", "Other"])

# === Experience ===
st.header("💼 Work Experience")
exp_level = st.radio("Experience Level", ["Fresher", "0–2 years", "2–5 years", "5+ years"])
current_role = st.text_input("Current Role (if any)")
projects_built = st.radio("Projects/Internships", ["Yes", "No", "In Progress"])

# === Skills & Aspirations ===
st.header("Skills & Aspirations")
tech_skills = st.multiselect("Technical Skills", [
    "Python", "SQL", "Power BI", "Excel", "Java", "HTML/CSS/JS", "Streamlit",
    "Git/GitHub", "Figma", "Tableau", "C++"
])
soft_skills = st.multiselect("Soft Skills", [
    "Communication", "Teamwork", "Leadership", "Problem Solving", "Adaptability",
    "Critical Thinking", "Time Management"
])
other_skills = st.text_area("Other Skills")

passion_area = st.multiselect("Passion Areas", [
    "AI/ML", "Web Development", "Data Analysis", "Cybersecurity", "UI/UX", 
    "Project Management", "Digital Marketing", "Teaching", "Entrepreneurship"
])
career_goal = st.selectbox("🎯 Career Aspiration", available_roles)
learning_mode = st.radio("Preferred Learning Mode", [
    "Video tutorials", "Interactive courses", "Text-based blogs", "Mentorship", "Hands-on projects"
])

# === Submit Form ===
if st.button("✅ Submit Info & Analyze"):
    st.success("Profile submitted!")

    resume_skills = [s.strip().lower() for s in tech_skills + soft_skills]
    if other_skills:
        resume_skills += [s.strip().lower() for s in other_skills.split(",") if s.strip()]
    
    matched_row = df_skills[df_skills['Career Aspiration'].str.lower() == career_goal.lower()]
    if matched_row.empty:
        st.warning("⚠️ No backend skill mapping available for this role.")
        st.stop()

    required_skills = matched_row.iloc[0]['skill library']
    matched = list(set(resume_skills) & set(required_skills))
    missing = list(set(required_skills) - set(resume_skills))

    st.subheader("📊 Skill Match Summary")
    st.write(f"✅ **Matched Skills:** {matched}")
    st.write(f"⚠️ **Missing Skills:** {missing}")

    advisory_prompt = f"""
You're an expert AI career advisor.

Candidate Name: {name}
Aspiration: {career_goal}
Current Skills: {resume_skills}
Missing Skills: {missing}
Learning Mode: {learning_mode}

Tasks:
1. Confirm if candidate is eligible for their goal role.
2. Recommend up to 3 roles they can explore now.
3. Suggest courses for missing skills (Coursera/Udemy) with links.
4. Format your response clearly using markdown and bullet points.
5. Keep tone friendly, motivating, and focused.

Begin with a short greeting that includes their name.
"""

    headers = {"Authorization": f"Bearer {openrouter_api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": advisory_prompt}]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        res.raise_for_status()
        report = res.json()["choices"][0]["message"]["content"]

        tab1, tab2 = st.tabs(["📘 Career Advisory Report", "📥 Download PDF"])

        with tab1:
            st.markdown("### 📘 Career Advisory Report")
            st.markdown(report)

        with tab2:
            pdf_buffer = generate_pdf(report, name)
            st.download_button(
                label="Download Career Report as PDF",
                data=pdf_buffer,
                file_name=f"{name}_SkillGrow_Report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error("❌ AI Recommendation Failed")
        st.code(str(e), language="bash")