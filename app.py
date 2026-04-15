import streamlit as st
import pandas as pd
from openai import OpenAI

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Roosevelt Sports Medicine", layout="wide")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "shoulder" not in st.session_state:
    st.session_state.shoulder = 0
if "acl" not in st.session_state:
    st.session_state.acl = 0

# ---------------- STYLES ----------------
st.markdown("""
<style>
body { background-color: #0e1117; }

h1, h2, h3 { color: white; }

.card {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
}

.green { background-color: #0f5132; color: #00ff9c; }
.yellow { background-color: #664d03; color: #ffd60a; }
.red { background-color: #58151c; color: #ff4b4b; }

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2 = st.columns([1, 5])

with col1:
    st.image("roosevelt_logo.png", width=100)

with col2:
    st.title("Roosevelt Sports Medicine")
    st.caption("AI Form Check • Injury Tracking • Return-to-Play System")

st.divider()

# ---------------- SIDEBAR NAV ----------------
st.sidebar.title("Navigation")

page = st.sidebar.radio("Go to", [
    "Dashboard",
    "Screening",
    "Rehab",
    "AI Form Check"
])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.subheader("🏋️ Athlete Performance Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Athletes", "24", "+3")
    col2.metric("Injuries", "6", "-2")
    col3.metric("Return-to-Play", "82%", "+5%")

    st.divider()

    st.subheader("📊 Performance Trends")

    st.line_chart({
        "Strength": [70, 72, 74, 73, 76],
        "Mobility": [65, 67, 68, 70, 72]
    })

# ---------------- SCREENING ----------------
elif page == "Screening":

    st.subheader("🧪 Movement Screening")

    st.write("### Shoulder Assessment")

    flex = st.number_input("Flexion")
    abd = st.number_input("Abduction")
    er = st.number_input("External Rotation")

    if st.button("Calculate Shoulder Score"):

        flex_s = 2 if flex >=160 else 1 if flex>=140 else 0
        abd_s = 2 if abd >=170 else 1 if abd>=135 else 0
        er_s = 2 if er >=90 else 1 if er>=70 else 0

        shoulder = flex_s + abd_s + er_s
        st.session_state.shoulder = shoulder

        if shoulder <= 2:
            color_class = "red"
            label = "POOR"
        elif shoulder <= 4:
            color_class = "yellow"
            label = "MODERATE"
        else:
            color_class = "green"
            label = "NORMAL"

        st.markdown(
            f"<div class='card {color_class}'>Shoulder Score: {shoulder}/6<br>{label}</div>",
            unsafe_allow_html=True
        )

    st.divider()

    st.write("### ACL Risk Screen")

    valgus = st.selectbox("Knee Valgus", ["Good","Moderate","Poor"])
    landing = st.selectbox("Landing", ["Good","Moderate","Poor"])
    balance = st.selectbox("Balance", ["Good","Moderate","Poor"])

    if st.button("Calculate ACL Score"):

        def score(x): return 2 if x=="Good" else 1 if x=="Moderate" else 0

        acl = score(valgus)+score(landing)+score(balance)
        st.session_state.acl = acl

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

    if st.session_state.shoulder and st.session_state.acl:
        rtp = (st.session_state.shoulder + st.session_state.acl) / 2

        st.markdown(
            f"<div class='card green'>Return to Play Score: {rtp}/6</div>",
            unsafe_allow_html=True
        )

# ---------------- REHAB ----------------
elif page == "Rehab":

    st.subheader("💪 Rehab Center")

    st.write("### Injury Plan")
    st.write("• Band External Rotations")
    st.write("• Scap Stability")
    st.write("• Controlled Landing Drills")

    st.divider()

    st.write("### Rehab Streak")

    if st.button("Log Workout"):
        st.session_state.streak += 1

    st.markdown(
        f"<div class='card green'>🔥 Streak: {st.session_state.streak} days</div>",
        unsafe_allow_html=True
    )

# ---------------- AI FORM CHECK ----------------
elif page == "AI Form Check":

    st.subheader("🤖 AI Form Check")

    video = st.file_uploader("Upload movement video", type=["mp4","mov"])

    if video:
        st.video(video)

        st.info("Analyzing movement...")

        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"You are a sports medicine expert analyzing movement."},
                    {"role":"user","content":"Analyze injury risk, form issues, and performance corrections."}
                ]
            )

            st.success(response.choices[0].message.content)

        except:
            st.warning("Add OpenAI API key in Streamlit secrets to enable AI analysis")


    
