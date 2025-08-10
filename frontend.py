import streamlit as st
import pandas as pd
import docx2txt
import requests
from PyPDF2 import PdfReader
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# === CONFIG ===
openrouter_api_key = "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"
backend_path = "C:/Users/ashwi/OneDrive/Desktop/VS code streamlit/data.xlsx"

# === PDF Generator ===
def generate_pdf(content, role):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"SkillGrow Career Advisory Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Career Aspiration: {role.title()}")

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

# === PAGE SETUP ===
st.set_page_config(page_title="SkillGrow Career Analyzer", layout="centered")

# === GLOBAL THEME INJECTION ===
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

# === Branding Header ===
st.title("SkillGrow – AI Career Skill Analyzer")
st.markdown("📄 Upload your resume and get a tailored career advisory based on your goal and skill data.")

# === Load Skill Library ===
df_skills = pd.read_excel(backend_path)
df_skills['skill library'] = df_skills['skill library'].apply(lambda x: [s.strip().lower() for s in str(x).split(",")])

# === Upload Resume ===
resume_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])
resume_text = ""
if resume_file:
    if resume_file.name.endswith(".pdf"):
        reader = PdfReader(resume_file)
        resume_text = "\n".join([page.extract_text() or "" for page in reader.pages])
    else:
        resume_text = docx2txt.process(resume_file)
    st.success("✅ Resume uploaded and extracted!")

# === Career Aspiration Input
career_goal = st.text_input("🎯 Career Aspiration (e.g. Data Analyst, UX Designer)").strip().lower()

# === Analyze & Recommend Button
if st.button("🔍 Full Career Recommendation") and resume_text and career_goal:
    with st.spinner("🔎 Analyzing resume and comparing with backend skill data..."):

        try:
            # STEP 1: Extract Resume Skills via GPT
            extract_prompt = f"""Extract ONLY the technical and professional skills from the resume below.
Resume:
{resume_text}

Return skills in comma-separated lowercase format."""
            gpt_url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {"Authorization": f"Bearer {openrouter_api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": extract_prompt}]
            }

            extract_res = requests.post(gpt_url, headers=headers, json=payload)
            extract_res.raise_for_status()
            extracted_skills = extract_res.json()["choices"][0]["message"]["content"]
            resume_skills = [s.strip() for s in extracted_skills.split(",") if s.strip()]

            st.subheader("✅ Resume Skills")
            st.write(resume_skills)

            # STEP 2: Match Backend Role Skills
            matched_row = df_skills[df_skills['Career Aspiration'].str.lower() == career_goal]
            if matched_row.empty:
                st.warning("No backend data available for this role.")
                st.stop()

            required_skills = matched_row.iloc[0]['skill library']
            st.subheader(f"📚 Skills Expected for '{career_goal.title()}'")
            st.write(required_skills)

            # STEP 3: Compare Resume Skills vs Role Skills
            matched = list(set(resume_skills) & set(required_skills))
            missing = list(set(required_skills) - set(resume_skills))

            st.markdown("### 🔍 Skill Gap Analysis")
            st.write(f"**Matched Skills:** {matched}")
            st.write(f"**Missing Skills:** {missing}")

            # STEP 4: GPT-Based Advisory for Missing Skills
            advisory_prompt = f"""You're a career advisor recommending learning paths.

Role: {career_goal}
Current Skills: {resume_skills}
Missing Skills: {missing}

Recommend helpful online courses for each missing skill using Coursera, Udemy, or other trusted platforms. Include skill name, course title, platform, and course link. Explain why it's useful for the role.
Format your response clearly using bullet points."""
            payload["messages"] = [{"role": "user", "content": advisory_prompt}]
            advise_res = requests.post(gpt_url, headers=headers, json=payload)
            advise_res.raise_for_status()
            recommendations = advise_res.json()["choices"][0]["message"]["content"]

            # STEP 5: Display Final Advisory with PDF Tab
            tab1, tab2 = st.tabs(["🎓 Career Advisory", "📥 Download PDF"])

            with tab1:
                st.markdown("### 🎓 Personalized Career Advisory")
                st.markdown(recommendations)

            with tab2:
                pdf_buffer = generate_pdf(recommendations, career_goal)
                st.download_button(
                    label="Download Career Report as PDF",
                    data=pdf_buffer,
                    file_name=f"{career_goal}_SkillGrow_Report.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error("❌ Error during analysis.")
            st.code(str(e), language="bash")