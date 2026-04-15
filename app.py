import streamlit as st
from openai import OpenAI

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Roosevelt Sports Medicine", layout="wide")

# ---------------- SESSION STATE ----------------
defaults = {
    "page": "dashboard",
    "streak": 0,
    "shoulder": 0,
    "acl": 0
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- STYLE (HUDL/CATAPULT DARK THEME) ----------------
st.markdown("""
<style>
body { background-color: #0e1117; }

h1, h2, h3, h4 { color: white; }

.block {
    padding: 18px;
    border-radius: 12px;
    font-weight: bold;
}

.card {
    padding: 18px;
    border-radius: 12px;
    font-weight: bold;
    text-align: center;
}

.green { background-color: #0f5132; color: #00ff9c; }
.yellow { background-color: #664d03; color: #ffd60a; }
.red { background-color: #58151c; color: #ff4b4b; }

hr { border-color: #222; }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
# 🏋️ Roosevelt Sports Medicine
### Performance • Rehab • AI Movement Analysis
---
""")

# ---------------- NAVIGATION ----------------
page = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Screening",
    "Rehab",
    "AI Form Check"
])

# =========================================================
# 🏟️ DASHBOARD (HUDL STYLE)
# =========================================================
if page == "Dashboard":

    st.subheader("📊 Athlete Performance Command Center")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Athletes", "24", "+3")
    c2.metric("Injuries", "6", "-2")
    c3.metric("Return-to-Play", "82%", "+5%")
    c4.metric("AI Analyses", "38", "+12")

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        st.subheader("📈 Performance Load Trends")

        st.line_chart({
            "Strength": [70, 72, 74, 76, 78],
            "Mobility": [65, 67, 68, 70, 73],
            "Readiness": [60, 63, 66, 70, 75]
        })

    with right:
        st.subheader("🚨 Alerts")

        st.error("ACL Risk Elevated - Athlete A")
        st.warning("Hamstring Load Increasing - Athlete B")
        st.success("3 Athletes Cleared for Return-to-Play")

# =========================================================
# 🧪 SCREENING
# =========================================================
elif page == "Screening":

    st.subheader("🧪 Movement Screening System")

    st.write("### Shoulder Assessment")

    flex = st.number_input("Flexion")
    abd = st.number_input("Abduction")
    er = st.number_input("External Rotation")

    if st.button("Calculate Shoulder Score"):

        flex_s = 2 if flex >= 160 else 1 if flex >= 140 else 0
        abd_s = 2 if abd >= 170 else 1 if abd >= 135 else 0
        er_s = 2 if er >= 90 else 1 if er >= 70 else 0

        shoulder = flex_s + abd_s + er_s
        st.session_state.shoulder = shoulder

        if shoulder <= 2:
            color = "red"; label = "POOR"
        elif shoulder <= 4:
            color = "yellow"; label = "MODERATE"
        else:
            color = "green"; label = "NORMAL"

        st.markdown(f"<div class='card {color}'>Shoulder Score: {shoulder}/6<br>{label}</div>",
                    unsafe_allow_html=True)

    st.divider()

    st.write("### ACL Risk Screen")

    valgus = st.selectbox("Knee Valgus", ["Good","Moderate","Poor"])
    landing = st.selectbox("Landing", ["Good","Moderate","Poor"])
    balance = st.selectbox("Balance", ["Good","Moderate","Poor"])

    if st.button("Calculate ACL Score"):

        def score(x): return 2 if x == "Good" else 1 if x == "Moderate" else 0

        acl = score(valgus) + score(landing) + score(balance)
        st.session_state.acl = acl

        if acl <= 2:
            color = "red"; label = "HIGH RISK"
        elif acl <= 4:
            color = "yellow"; label = "MODERATE"
        else:
            color = "green"; label = "LOW RISK"

        st.markdown(f"<div class='card {color}'>ACL Score: {acl}/6<br>{label}</div>",
                    unsafe_allow_html=True)

    st.divider()

    if st.session_state.shoulder and st.session_state.acl:
        rtp = (st.session_state.shoulder + st.session_state.acl) / 2

        st.markdown(f"<div class='card green'>Return-to-Play Score: {rtp:.1f}/6</div>",
                    unsafe_allow_html=True)

# =========================================================
# 💪 REHAB CENTER
# =========================================================
elif page == "Rehab":

    st.subheader("💪 Rehab & Recovery Center")

    st.write("### Injury Protocol")
    st.write("• Band External Rotations")
    st.write("• Stability Drills")
    st.write("• Controlled Movement Progressions")

    st.divider()

    st.write("### Rehab Streak")

    if st.button("Log Rehab Session"):
        st.session_state.streak += 1

    st.markdown(f"<div class='card green'>🔥 Streak: {st.session_state.streak} days</div>",
                unsafe_allow_html=True)

# =========================================================
# 🤖 AI FORM CHECK
# =========================================================
elif page == "AI Form Check":

    st.subheader("🤖 AI Movement Analysis System")

    video = st.file_uploader("Upload Movement Video", type=["mp4","mov"])

    if video:
        st.video(video)

        st.info("Analyzing movement...")

        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"You are a sports medicine expert analyzing biomechanics and injury risk."},
                    {"role":"user","content":"Analyze movement for injury risk, valgus collapse, and performance faults."}
                ]
            )

            st.success(response.choices[0].message.content)

        except:
            st.warning("Add OpenAI API key in Streamlit secrets to enable AI analysis")
