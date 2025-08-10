import streamlit as st
import os
import base64

# === Page Config ===
st.set_page_config(page_title="SkillGrow Home", layout="centered")

# === CSS Styling ===
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right, #004d4d, #c1a36f);
    font-family: 'Inter', sans-serif;
    color: lightgreen !important;
}
label, .stRadio > div, .stCaption, h1, h2, h3, h4, h5, h6, p, span {
    color: white !important;
}
input, textarea {
    background-color: rgba(0,100,0,0.3) !important;
    color: white !important;
}
input::placeholder, textarea::placeholder {
    color: rgba(255,255,255,0.5) !important;
}
.stButton button {
    background: linear-gradient(to right, #c1a36f, #b3935e);
    color: white !important;
    font-weight: 600;
    border-radius: 10px;
    border: none;
    padding: 10px;
}
.logo-box {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 50px;
    margin-bottom: 30px;
}
.logo-box img {
    width: 100px;
    margin-right: 25px;
    border-radius: 8px;
}
.branding-text h2 {
    font-size: 32px;
    font-weight: 700;
    color: white;
}
.branding-text p {
    font-size: 16px;
    color: white;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #004d4d, #006666);
    color: white;
}
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebar"] div {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# === Logo Load ===
def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

image_path = r"C:/Users/ashwi/Downloads/SkillGrow logo with .png"

if os.path.exists(image_path):
    logo_base64 = get_image_base64(image_path)
    st.markdown(f"""
        <div class="logo-box">
            <img src="data:image/png;base64,{logo_base64}" />
            <div class="branding-text">
                <h2>SkillGrow</h2>
                <p>Grow your career with SkillGrow.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Logo not found, check your image path!")

st.markdown("---")

# === Access Mode Selection ===
access_mode = st.radio("Select Access Type:", ["Sign In", "Create Account", "Continue as Guest"], horizontal=True)
st.markdown("---")

# === Session Setup ===
if "navigate" not in st.session_state:
    st.session_state.navigate = None

# === Form Logic ===
if access_mode == "Sign In":
    st.subheader("🔐 Sign In")
    email = st.text_input("Email address", placeholder="your@email.com")
    password = st.text_input("Password", type="password", placeholder="Enter secure password")
    if st.button("Sign In", use_container_width=True):
        if email and password:
            st.success(f"Welcome back, {email}!")
            st.session_state.navigate = "app"
            st.rerun()
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
        st.session_state.navigate = "app"
        st.rerun()

# === Redirect Logic ===
# ✅ Put this **at the end** after all buttons
if st.session_state.navigate == "app":
    st.switch_page("pages/app.py")
elif st.session_state.navigate == "frontend":
    st.switch_page("pages/frontend.py")
elif st.session_state.navigate == "mannual_entry":
    st.switch_page("pages/mannual_entry.py")
elif st.session_state.navigate == "personality_quiz":
    st.switch_page("pages/personality_quiz.py")

st.markdown("---")
st.caption("✨ Ready to shape your future with SkillGrow.")

