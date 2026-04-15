import streamlit as st

st.title("Shoulder ROM Screening App")

flexion = st.number_input("Shoulder Flexion (degrees)", min_value=0)
abduction = st.number_input("Shoulder Abduction (degrees)", min_value=0)
er = st.number_input("External Rotation 90/90 (degrees)", min_value=0)

if st.button("Calculate Score"):

    if flexion >= 160:
        flex_score = 2
    elif flexion >= 140:
        flex_score = 1
    else:
        flex_score = 0

    if abduction >= 170:
        abd_score = 2
    elif abduction >= 135:
        abd_score = 1
    else:
        abd_score = 0

    if er >= 90:
        er_score = 2
    elif er >= 70:
        er_score = 1
    else:
        er_score = 0

    total = flex_score + abd_score + er_score

    if total <= 2:
        risk = "Red (Poor)"
        safety = "NOT Safe to Hit"
        action = "Rehab Required"
    elif total <= 4:
        risk = "Yellow (Moderate)"
        safety = "Modify Activity"
        action = "Mobility + Strength Work"
    else:
        risk = "Green (Normal)"
        safety = "Safe to Hit"
        action = "No Action Needed"

    st.subheader("Results")
    st.write(f"Total Score: {total}/6")
    st.write(f"Risk Level: {risk}")
    st.write(f"Safety: {safety}")
    st.write(f"Action: {action}")
