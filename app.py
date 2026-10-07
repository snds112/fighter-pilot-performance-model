

# To run this application:
# 1. Install Streamlit (if not already installed): pip install streamlit
# 2. Navigate to this file's directory
# 3. Run: streamlit run app.py



import streamlit as st
import numpy as np

st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-size: 12px;
    }

    h1 { font-size: 24px; }
    h2 { font-size: 18px; }
    h3 { font-size: 16px; }

    label { font-size: 12px !important; }

    .stMetricValue {
        font-size: 18px !important;
    }

    .stMetricLabel {
        font-size: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



def clamp(x):
    return np.clip(x, 0, 1)


def fighter_pilot_model(HR, SQ, MC, EL, ES):
    
    cognitive_load = clamp(
        0.3 * MC + 0.3 * ES + 0.3 * HR - 0.3 * EL
    )

    physical_fatigue = clamp(
        0.5 * HR - 0.4 * SQ
    )

    stress_level = clamp(
        0.3 * cognitive_load + 0.3 * physical_fatigue + 0.3 * ES -0.1 * EL
    )

    situational_awareness = clamp(
        0.7 * EL + 0.7 * SQ - 0.4 * cognitive_load
    )

    pilot_performance = clamp(
        0.8 * situational_awareness - 0.4 * stress_level
    )


    return cognitive_load, physical_fatigue, stress_level, situational_awareness, pilot_performance


# Page setup
st.set_page_config(
    page_title="Fighter Pilot Performance Model",
    layout="wide"
)

st.title("Fighter Pilot Performance Simulation")
st.write("Interactive prototype for evaluating pilot performance under varying conditions.")

st.divider()

# Create two main columns
input_col, spacer, output_col = st.columns([1, 0.15, 1])


with input_col:
    st.subheader("Input Parameters")

    HR = st.slider("Heart Rate", 0.0, 1.0, 0.5)
    SQ = st.slider("Sleep Quality", 0.0, 1.0, 0.5)
    MC = st.slider("Mission Complexity", 0.0, 1.0, 0.5)
    EL = st.slider("Experience Level", 0.0, 1.0, 0.5)
    ES = st.slider("Environmental Stress", 0.0, 1.0, 0.5)

# Compute model
CL, PF, SL, SA, PP = fighter_pilot_model(HR, SQ, MC, EL, ES)


with output_col:
    st.subheader("Model Outputs")

    st.metric("Cognitive Load", f"{CL:.2f}")
    st.metric("Physical Fatigue", f"{PF:.2f}")
    st.metric("Stress Level", f"{SL:.2f}")
    st.metric("Situational Awareness", f"{SA:.2f}")
    st.metric("Pilot Performance", f"{PP:.2f}")


st.divider()

st.subheader("Performance Interpretation")

if PP >= 0.7:
    st.success("High performance expected. Pilot is well-prepared for mission demands.")
elif PP >= 0.4:
    st.warning("Moderate performance. Pilot may experience manageable stress and workload.")
else:
    st.error("Low performance predicted. High stress or fatigue may impair mission effectiveness.")
