import streamlit as st
import pandas as pd
from huggingface_hub import hf_hub_download
import joblib

# Download and load the model
model_path = hf_hub_download(repo_id="Santhu976/machine_failure_model", filename="best_machine_failure_model_v1.joblib")
model = joblib.load(model_path)

# Streamlit UI for Machine Failure Prediction
st.title("Machine Failure Prediction App")
st.write("""
This application predicts the likelihood of a machine failing based on its operational parameters.
Please enter the sensor and configuration data below to get a prediction.
""")

# User input
Type = st.selectbox("Machine Type", ["H", "L", "M"])
air_temp = st.number_input("Air Temperature (K)", min_value=250.0, max_value=400.0, value=298.0, step=0.1)
process_temp = st.number_input("Process Temperature (K)", min_value=250.0, max_value=500.0, value=324.0, step=0.1)
rot_speed = st.number_input("Rotational Speed (RPM)", min_value=0, max_value=3000, value=1400)
torque = st.number_input("Torque (Nm)", min_value=0.0, max_value=100.0, value=40.0, step=0.1)
tool_wear = st.number_input("Tool Wear (min)", min_value=0, max_value=300, value=10)

# Assemble input into DataFrame
input_data = pd.DataFrame([{
    'Air temperature': air_temp,
    'Process temperature': process_temp,
    'Rotational speed': rot_speed,
    'Torque': torque,
    'Tool wear': tool_wear,
    'Type': Type
}])


if st.button("Predict Failure"):
    prediction = model.predict(input_data)[0]
    result = "Machine Failure" if prediction == 1 else "No Failure"
    st.subheader("Prediction Result:")
    st.success(f"The model predicts: **{result}**")
