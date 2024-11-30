import streamlit as st
import pickle
import os

# Constants
MODEL_PATH = r"./model.pickle"
PAGE_TITLE = "Lung Cancer Prediction"
PAGE_ICON = "🫁"

# Page Configuration
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")
st.title(f"{PAGE_ICON} {PAGE_TITLE}")

# Add custom CSS for enhanced visuals
st.markdown(
    """
    <style>
        .main-header {
            text-align: center;
            font-size: 26px;
            font-weight: bold;
        }
        .predict-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: 0.3s ease-in-out;
        }
        .predict-button:hover {
            background-color: #45a049;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }
        .result-container {
            background-color: #f1f1f1;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .result-container h2 {
            font-size: 22px;
            color: #333;
        }
        .result-container p {
            font-size: 18px;
            color: #555;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("Use this tool to predict lung cancer risk.")
st.sidebar.markdown("### Quick Links:")
st.sidebar.markdown("- 🏠 [Home](#)")
st.sidebar.markdown("- 📊 [About Model](#)")
st.sidebar.markdown("- 📩 [Contact Us](pavanpanni6@gmail.com)")

# Load Trained Model
model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as model_file:
        model = pickle.load(model_file)
else:
    st.error("⚠️ Model file not found. Please ensure 'model.pickle' is in the specified directory.")

# Description
st.markdown("### 🤖 Welcome to the Lung Cancer Prediction Tool")
st.markdown(
    """
    This app leverages a machine learning model to estimate the risk of lung cancer based on your health and lifestyle information.  
    Please fill out the form below and click **Predict** to view your results.
    """
)

# Display a health-related image
st.image(
    "https://breathing.co.in/wp-content/uploads/2021/03/Heres-how-cigarattes-smoking-can-affect-your-lungs.png",
    caption="Healthy Lungs vs Affected Lungs",
    use_container_width=True,
)

# Input Form
st.markdown("### 📝 Enter Your Details")
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("🧑‍⚕️ Gender", ["Male", "Female"], help="Select your gender.")
        age = st.number_input("🎂 Age", min_value=1, max_value=100, step=1, help="Enter your age.")
        smoking = st.selectbox("🚬 Smoking", ["No", "Yes"], help="Do you smoke?")
        yellow_fingers = st.selectbox("✋ Yellow Fingers", ["No", "Yes"], help="Do you have yellow-stained fingers?")
        anxiety = st.selectbox("😰 Anxiety", ["No", "Yes"], help="Do you experience anxiety?")
        peer_pressure = st.selectbox("👥 Peer Pressure", ["No", "Yes"], help="Are you influenced by peer pressure?")
        chronic_disease = st.selectbox("🩺 Chronic Disease", ["No", "Yes"], help="Do you have a chronic disease?")
    with col2:
        fatigue = st.selectbox("😴 Fatigue", ["No", "Yes"], help="Do you often feel fatigued?")
        allergy = st.selectbox("🤧 Allergy", ["No", "Yes"], help="Do you have any allergies?")
        wheezing = st.selectbox("🌬️ Wheezing", ["No", "Yes"], help="Do you experience wheezing?")
        alcohol_consuming = st.selectbox("🍷 Alcohol Consumption", ["No", "Yes"], help="Do you consume alcohol?")
        coughing = st.selectbox("🤒 Coughing", ["No", "Yes"], help="Do you have persistent coughing?")
        shortness_of_breath = st.selectbox("😤 Shortness of Breath", ["No", "Yes"], help="Do you experience shortness of breath?")
        swallowing_difficulty = st.selectbox("🥴 Swallowing Difficulty", ["No", "Yes"], help="Do you have difficulty swallowing?")
        chest_pain = st.selectbox("❤️ Chest Pain", ["No", "Yes"], help="Do you experience chest pain?")
    
    submitted = st.form_submit_button("💡 Predict", help="Click to get your prediction!")

# Process Inputs and Display Results
if submitted:
    if model:
        # Map inputs to numeric values
        input_dict = {
            "gender": 1 if gender == "Female" else 0,
            "smoking": 1 if smoking == "Yes" else 0,
            "yellow_fingers": 1 if yellow_fingers == "Yes" else 0,
            "anxiety": 1 if anxiety == "Yes" else 0,
            "peer_pressure": 1 if peer_pressure == "Yes" else 0,
            "chronic_disease": 1 if chronic_disease == "Yes" else 0,
            "fatigue": 1 if fatigue == "Yes" else 0,
            "allergy": 1 if allergy == "Yes" else 0,
            "wheezing": 1 if wheezing == "Yes" else 0,
            "alcohol_consuming": 1 if alcohol_consuming == "Yes" else 0,
            "coughing": 1 if coughing == "Yes" else 0,
            "shortness_of_breath": 1 if shortness_of_breath == "Yes" else 0,
            "swallowing_difficulty": 1 if swallowing_difficulty == "Yes" else 0,
            "chest_pain": 1 if chest_pain == "Yes" else 0
        }
        input_features = [input_dict[key] for key in input_dict]
        input_features.insert(1, age)

        # Predict using the model
        prediction = model.predict([input_features])[0]
        diagnosis = "Lung Cancer" if prediction == 1 else "No Lung Cancer"

        # Display Results
        st.markdown(
            f"""
            <div class="result-container">
                <h2>🩺 Prediction Result:</h2>
                <p><strong>Diagnosis:</strong> {diagnosis}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("⚠️ The prediction model is not available.")
