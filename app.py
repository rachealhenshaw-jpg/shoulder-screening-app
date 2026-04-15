import streamlit as st

st.set_page_config(page_title="Roosevelt Sports Medicine", layout="wide")

# HEADER SECTION
col1, col2 = st.columns([1, 5])

with col1:
    st.image("roosevelt_logo.png", width=100)  # your logo file

with col2:
    st.markdown("""
    # Roosevelt Sports Medicine
    ### AI Form Check • Injury Tracking • Return-to-Play System
    """)import streamlit as st
import pandas as pd
import random
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

h1, h2, h3 {
    color: white;
}

.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}

.card {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}

.green {
    background-color: #0f5132;
    color: #00ff9c;
}

.yellow {
    background-color: #664d03;
    color: #ffd60a;
}

.red {
    background-color: #58151c;
    color: #ff4b4b;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="Roosevelt Sports Medicine", layout="centered")

# ---------------- GOOGLE SHEETS ----------------
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# Upload your JSON key to Streamlit secrets later
# creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp"], scope)
# client = gspread.authorize(creds)
# sheet = client.open("Roosevelt_Data").sheet1

# ---------------- LOGIN ----------------
st.title("Roosevelt Sports Medicine")

if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login":

    st.header("Sign In")

    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Athlete", "Coach"])
    injury = st.selectbox("Currently Injured?", ["No", "Yes"])
    assessment = st.selectbox("Need Assessment?", ["Yes", "No"])

    if st.button("Enter App"):
        st.session_state.name = name
        st.session_state.role = role
        st.session_state.injury = injury
        st.session_state.assessment = assessment
        st.session_state.page = "home"
        st.rerun()

# ---------------- HOME ----------------
st.title("🏋️ Roosevelt Sports Medicine")

st.markdown("### Athlete Performance Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏃 Screening"):
        st.session_state.page = "screen"

with col2:
    if st.button("💪 Rehab"):
        st.session_state.page = "rehab"

with col3:
    if st.button("🤖 AI Form Check"):
        st.session_state.page = "ai"
# ---------------- SCREENING ----------------
elif st.session_state.page == "screen":

    st.header("Screening")

    # Shoulder
    st.subheader("Shoulder")

    flex = st.number_input("Flexion")
    abd = st.number_input("Abduction")
    er = st.number_input("External Rotation")

    if st.button("Calculate Shoulder"):

        flex_s = 2 if flex >=160 else 1 if flex>=140 else 0
        abd_s = 2 if abd >=170 else 1 if abd>=135 else 0
        er_s = 2 if er >=90 else 1 if er>=70 else 0

        total = flex_s + abd_s + er_s

      if total <= 2:
    color_class = "red"
    label = "POOR"
elif total <= 4:
    color_class = "yellow"
    label = "MODERATE"
else:
    color_class = "green"
    label = "NORMAL"

st.markdown(
    f"<div class='card {color_class}'>Shoulder Score: {total}/6<br>{label}</div>",
    unsafe_allow_html=True
)

    # ACL
    st.subheader("ACL")

    valgus = st.selectbox("Knee Valgus", ["Good","Moderate","Poor"])
    landing = st.selectbox("Landing", ["Good","Moderate","Poor"])
    balance = st.selectbox("Balance", ["Good","Moderate","Poor"])

    if st.button("Calculate ACL"):

        def score(x): return 2 if x=="Good" else 1 if x=="Moderate" else 0

        acl = score(valgus)+score(landing)+score(balance)

       if acl <= 2:
    color_class = "red"
    label = "HIGH RISK"
elif acl <= 4:
    color_class = "yellow"
    label = "MODERATE"
else:
    color_class = "green"
    label = "LOW RISK"

st.markdown(
    f"<div class='card {color_class}'>ACL Score: {acl}/6<br>{label}</div>",
    unsafe_allow_html=True
)

    # Return to Play Score
 if "shoulder" in st.session_state and "acl" in st.session_state:
        rtp = (st.session_state.shoulder + st.session_state.acl) / 2
        st.subheader(f"Return to Play Score: {rtp}/6")
  st.markdown(
    f"<div class='card green'>Return to Play Score: {rtp}/6</div>",
    unsafe_allow_html=True
)

# ---------------- REHAB ----------------
st.header("💪 Rehab Center")

if st.session_state.injury == "Yes":
    st.markdown("### 🔴 Injury Plan")

    st.write("• Band External Rotations")
    st.write("• Scap Stability")
    st.write("• Controlled Landing Drills")

st.markdown("### 🔥 Rehab Streak")

if st.button("Log Workout"):
    st.session_state.streak += 1

st.markdown(
    f"<div class='card green'>🔥 Streak: {st.session_state.streak} days</div>",
    unsafe_allow_html=True
)

# ---------------- AI FORM CHECK ----------------
st.divider()
st.header("AI Form Check")

video = st.file_uploader("Upload video", type=["mp4","mov"])

if video:
    st.video(video)

    st.write("AI Analysis:")

    # REAL AI (requires OpenAI key in secrets)
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are a sports medicine expert analyzing movement."},
                {"role":"user","content":"Analyze this athlete movement for injury risk and form issues."}
            ]
        )

        st.write(response.choices[0].message.content)

    except:
        st.warning("Add OpenAI API key to enable AI analysis")
elif st.session_state.page == "ai":

    st.header("🤖 AI Form Check")

    video = st.file_uploader("Upload movement video", type=["mp4","mov"])

    if video:
        st.video(video)

        st.markdown("### 📊 AI Feedback")

        st.info("Knee valgus detected. Improve hip control and stability.")
