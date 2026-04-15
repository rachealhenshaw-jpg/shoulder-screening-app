import streamlit as st
import pandas as pd

st.set_page_config(page_title="Texas TeleAT", layout="centered")

# ---------------- LOGIN ----------------
st.title("Texas TeleAT")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

username = st.text_input("Enter Athlete Name")

if st.button("Login"):
    st.session_state.logged_in = True
    st.session_state.username = username

if st.session_state.logged_in:

    st.success(f"Welcome, {st.session_state.username}")

    st.divider()

    # ---------------- SHOULDER SCREEN ----------------
    st.header("Shoulder ROM Screening")

    flexion = st.number_input("Flexion", 0)
    abduction = st.number_input("Abduction", 0)
    er = st.number_input("External Rotation", 0)

    if st.button("Calculate Shoulder Score"):

        # Scoring
        flex_score = 2 if flexion >= 160 else 1 if flexion >= 140 else 0
        abd_score = 2 if abduction >= 170 else 1 if abduction >= 135 else 0
        er_score = 2 if er >= 90 else 1 if er >= 70 else 0

        total = flex_score + abd_score + er_score

        # Color + Results
        if total <= 2:
            color = "red"
            level = "POOR"
            safety = "NOT Safe to Hit"
        elif total <= 4:
            color = "yellow"
            level = "MODERATE"
            safety = "Modify Activity"
        else:
            color = "green"
            level = "NORMAL"
            safety = "Safe to Hit"

        st.markdown(f"<h2 style='color:{color};'>Score: {total}/6 - {level}</h2>", unsafe_allow_html=True)
        st.write(f"Safety: {safety}")

        # Save Data
        data = pd.DataFrame([[st.session_state.username, flexion, abduction, er, total, level]],
                            columns=["Name","Flexion","Abduction","ER","Score","Level"])

        data.to_csv("data.csv", mode='a', header=False, index=False)

    st.divider()

    # ---------------- ACL SCREEN ----------------
    st.header("ACL Screening")

    knee_valgus = st.selectbox("Knee Valgus", ["Good", "Moderate", "Poor"])
    landing = st.selectbox("Landing Control", ["Good", "Moderate", "Poor"])
    balance = st.selectbox("Balance", ["Good", "Moderate", "Poor"])

    if st.button("Calculate ACL Score"):

        def score(x):
            return 2 if x=="Good" else 1 if x=="Moderate" else 0

        total_acl = score(knee_valgus) + score(landing) + score(balance)

        if total_acl <= 2:
            color = "red"
            level = "HIGH RISK"
        elif total_acl <= 4:
            color = "yellow"
            level = "MODERATE RISK"
        else:
            color = "green"
            level = "LOW RISK"

        st.markdown(f"<h2 style='color:{color};'>ACL Score: {total_acl}/6 - {level}</h2>", unsafe_allow_html=True)

    st.divider()

    # ---------------- AI FORM CHECK ----------------
    st.header("AI Form Check (Upload Video)")

    uploaded_file = st.file_uploader("Upload movement video", type=["mp4", "mov"])

    if uploaded_file:
        st.video(uploaded_file)

        st.write("AI Feedback:")

        # SIMPLE AI LOGIC (placeholder)
        st.info("Possible knee valgus detected. Focus on hip stability and control.")

    st.divider()

    # ---------------- VIEW SAVED DATA ----------------
    st.header("Saved Athlete Data")

    try:
        df = pd.read_csv("data.csv")
        st.dataframe(df)
    except:
        st.write("No data yet.")
