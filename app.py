import streamlit as st
import pandas as pd
import random
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
elif st.session_state.page == "home":

    st.success(f"Welcome {st.session_state.name}")

    st.divider()

    col1, col2 = st.columns(2)

    if col1.button("Screening"):
        st.session_state.page = "screen"

    if col2.button("Rehab"):
        st.session_state.page = "rehab"

    st.divider()

    # Motivational Quotes
    quotes = [
        "Small progress is still progress.",
        "Strong athletes recover smarter.",
        "Consistency beats intensity.",
        "Rehab today = performance tomorrow"
    ]
    st.info(random.choice(quotes))

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

        if total <=2:
            color="red"; level="POOR"
        elif total <=4:
            color="orange"; level="MODERATE"
        else:
            color="green"; level="NORMAL"

        st.markdown(f"<h2 style='color:{color};'>Score: {total} - {level}</h2>", unsafe_allow_html=True)

        st.session_state.shoulder = total

    # ACL
    st.subheader("ACL")

    valgus = st.selectbox("Knee Valgus", ["Good","Moderate","Poor"])
    landing = st.selectbox("Landing", ["Good","Moderate","Poor"])
    balance = st.selectbox("Balance", ["Good","Moderate","Poor"])

    if st.button("Calculate ACL"):

        def score(x): return 2 if x=="Good" else 1 if x=="Moderate" else 0

        acl = score(valgus)+score(landing)+score(balance)

        if acl <=2:
            color="red"; level="HIGH RISK"
        elif acl <=4:
            color="orange"; level="MODERATE"
        else:
            color="green"; level="LOW RISK"

        st.markdown(f"<h2 style='color:{color};'>ACL: {acl} - {level}</h2>", unsafe_allow_html=True)

        st.session_state.acl = acl

    # Return to Play Score
    if "shoulder" in st.session_state and "acl" in st.session_state:
        rtp = (st.session_state.shoulder + st.session_state.acl) / 2
        st.subheader(f"Return to Play Score: {rtp}/6")

# ---------------- REHAB ----------------
elif st.session_state.page == "rehab":

    st.header("Rehab Center")

    if st.session_state.injury == "Yes":
        st.subheader("Injury Rehab Plan")

        st.write("• Band External Rotations")
        st.write("• Scap Stability")
        st.write("• Balance + Landing Mechanics")

    st.subheader("Rehab Streak")

    if "streak" not in st.session_state:
        st.session_state.streak = 0

    if st.button("Log Rehab Day"):
        st.session_state.streak += 1

    st.success(f"Streak: {st.session_state.streak} days")

    st.divider()

    st.subheader("Exercise Library")

    st.write("• Shoulder Mobility")
    st.write("• Hip Strength")
    st.write("• Plyometrics")

    st.divider()

    st.subheader("Coach Feedback")
    feedback = st.text_area("Coach Notes")

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

