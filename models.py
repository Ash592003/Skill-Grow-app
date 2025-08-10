import streamlit as st

# models.py
def load_model():
    # Load or define your ML model here
    model = ...  # Your code
    return model

# === Page Config ===
st.set_page_config(page_title="SkillGrow Login", page_icon="📄", layout="centered")



# === Custom Background Gradient ===import streamlit as st
import streamlit as st

import streamlit as st

# Set page config
st.set_page_config(page_title="SkillGrow Login", layout="centered")

# Inject custom CSSimport streamlit as st

st.set_page_config(page_title="SkillGrow Login", layout="centered")

# Inject custom CSS
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



# === Branding Header ===
col1, col2 = st.columns([0.2, 1.8])
with col1:
    st.image("C:/Users/ashwi/Downloads/logo.png", width=50)
with col2:
    st.markdown("## SkillGrow")
    st.caption("Grow your career with skillgrow.")
st.markdown("---")

# === Access Mode Selection ===
access_mode = st.radio("Select Access Type:", ["Sign In", "Create Account", "Continue as Guest"], horizontal=True)
st.markdown("---")

# === Dynamic Form Rendering ===
if access_mode == "Sign In":
    st.subheader("🔐 Sign In")
    email = st.text_input("Email address", placeholder="your@email.com")
    password = st.text_input("Password", type="password", placeholder="Enter secure password")
    if st.button("Sign In", use_container_width=True):
        if email and password:
            st.success(f"Welcome back, {email}!")
        else:
            st.error("Please enter both email and password.")

elif access_mode == "Create Account":
    st.subheader("📝 Create an Account")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    if st.button("Create Account", use_container_width=True):
        if new_email and new_password:
            st.success("Account created successfully!")
        else:
            st.error("Please fill all required fields.")

elif access_mode == "Continue as Guest":
    st.subheader("👤 Guest Access")
    if st.button("Access Limited Features", use_container_width=True):
        st.warning("Guest mode activated with restricted access.")

# === Footer ===
st.markdown("---")
st.caption("✨ Ready to shape your future with SkillGrow.")
