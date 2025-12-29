import streamlit as st
import requests

st.title("Vehicle Health & Diagnostics")

soc = st.slider("State of Charge (%)", 0, 100, 80)
temp = st.slider("Battery Temperature (°C)", -20, 80, 30)
cycles = st.number_input("Charge Cycles", 0, 5000, 500)

if st.button("Evaluate"):
    response = requests.post(
        "http://localhost:8000/battery/health",
        json={
            "soc": soc,
            "temperature": temp,
            "charge_cycles": cycles
        }
    )

    result = response.json()
    st.metric("Health Score", result["health_score"])
    st.metric("Risk Level", result["risk_level"])
    if result["risk_level"] == "HIGH":
        st.error("High Risk: Immediate attention required!")
    elif result["risk_level"] == "MEDIUM":
        st.warning("Medium Risk: Monitor closely.")
    else:
        st.success("Low Risk: Battery is healthy.")
    st.info(f"Explanation: {result['explanation']}")

        