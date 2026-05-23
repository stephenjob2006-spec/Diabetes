from matplotlib.pylab import number
import streamlit as st
from PIL import Image
import pickle

model=pickle.load(open('model.save','rb'))
scaler=pickle.load(open('scaler.save','rb'))
gender=pickle.load(open('gender.save','rb'))
smoking=pickle.load(open('smoking.save','rb'))
def main():
    st.set_page_config(
        page_title="Diabetes Predictor",
        page_icon="🩺",
        layout="wide"
    )
    
    st.markdown("""
    <style>
    /* ========== MAIN APP BACKGROUND ========== */
    .stApp {
        background: #f8f9fa;
    }

    /* Remove default padding */
    .main > div {
        padding: 0;
    }

    /* ========== HEADER/HERO SECTION ========== */
    .hero-section {
        background: linear-gradient(135deg, #0088cc 0%, #00b4d8 25%, #90e0ef 50%, #caf0f8 75%, #e89b9b 100%);
        padding: 60px 40px;
        border-radius: 0;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
        min-height: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .hero-section::before {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 100px;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120"><path d="M0,50 Q300,0 600,50 T1200,50 L1200,120 L0,120 Z" fill="%23f8f9fa"/></svg>');
        background-size: cover;
        background-repeat: no-repeat;
    }

    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 800px;
    }

    .hero-title {
        font-size: 56px !important;
        font-weight: 900 !important;
        margin-bottom: 20px !important;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
        line-height: 1.2 !important;
    }

    .hero-subtitle {
        font-size: 20px !important;
        font-weight: 500 !important;
        margin-bottom: 30px !important;
        line-height: 1.6 !important;
        opacity: 0.95;
    }

    /* ========== MAIN APP BACKGROUND ========== */
    .stApp {
        background: #f8f9fa !important;
    }

    /* ========== MAIN CONTAINER ========== */
    .block-container {
        background: white !important;
        border-radius: 0;
        padding: 40px 60px !important;
        box-shadow: none;
        border: none;
        margin-top: 0 !important;
    }

    /* ========== FORM SECTION ========== */
    .form-section {
        background: white;
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin: 40px 0;
    }

    .section-title {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #0088cc !important;
        margin-bottom: 30px !important;
        border-bottom: 3px solid #00b4d8;
        padding-bottom: 15px;
    }

    /* ========== TYPOGRAPHY ========== */
    h1 {
        text-align: center;
        font-size: 56px !important;
        color: white !important;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px !important;
    }

    h2, h3 {
        color: #0088cc !important;
        font-weight: 800;
        margin-top: 20px !important;
    }

    p, label {
        color: #333333 !important;
        font-weight: 600;
        font-size: 16px;
    }

    /* ========== RADIO BUTTONS ========== */
    .stRadio > label {
        font-weight: 700 !important;
        color: #0088cc !important;
        font-size: 16px !important;
        margin-bottom: 15px !important;
    }

    .stRadio [role="radiogroup"] {
        background: linear-gradient(135deg, #f0f7ff 0%, #e0f2ff 100%);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #00b4d8;
        gap: 15px;
    }

    .stRadio [role="radio"] {
        accent-color: #0088cc !important;
    }

    /* ========== SLIDERS ========== */
    .stSlider > label {
        font-weight: 700 !important;
        color: #0088cc !important;
        font-size: 16px !important;
    }

    .stSlider [data-testid="stSlider"] {
        background: linear-gradient(135deg, #f0f7ff 0%, #e0f2ff 100%);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #00b4d8;
    }

    /* ========== NUMBER INPUTS ========== */
    .stNumberInput > label {
        font-weight: 700 !important;
        color: #0088cc !important;
        font-size: 16px !important;
    }

    .stNumberInput input {
        background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%) !important;
        border: 2px solid #00b4d8 !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        font-size: 16px !important;
        color: #333 !important;
        transition: all 0.3s ease;
        font-weight: 600;
    }

    .stNumberInput input:focus {
        background: #ffffff !important;
        border-color: #0088cc !important;
        box-shadow: 0 0 20px rgba(0, 136, 204, 0.3);
    }

    /* ========== BUTTONS ========== */
    .stButton > button {
        background: linear-gradient(135deg, #0088cc 0%, #00b4d8 100%);
        color: white !important;
        padding: 16px 40px !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 800 !important;
        font-size: 17px !important;
        width: 100% !important;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0, 136, 204, 0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #00b4d8 0%, #0088cc 100%);
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 136, 204, 0.5);
    }

    .stButton > button:active {
        transform: translateY(-1px);
    }

    /* ========== SUCCESS & ERROR MESSAGES ========== */
    .stSuccess {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(76, 175, 80, 0.05) 100%) !important;
        border-left: 5px solid #4caf50 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        color: #2e7d32 !important;
        font-weight: 700;
        font-size: 16px;
    }

    .stError {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.15) 0%, rgba(244, 67, 54, 0.05) 100%) !important;
        border-left: 5px solid #f44336 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        color: #c62828 !important;
        font-weight: 700;
        font-size: 16px;
    }

    /* ========== INFO MESSAGES ========== */
    .stInfo {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.15) 0%, rgba(33, 150, 243, 0.05) 100%) !important;
        border-left: 5px solid #2196f3 !important;
        border-radius: 8px !important;
        padding: 16px !important;
        color: #1565c0 !important;
        font-weight: 700;
        font-size: 16px;
    }

    /* ========== IMAGE STYLING ========== */
    img {
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    .floating-tooltip {
        position: fixed;
        top: 50%;
        right: -300px;
        width: 280px;
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        transition: right 0.4s ease;
        z-index: 999;
        border-left: 4px solid #0088cc;
    }

    .floating-tooltip.show {
        right: 20px;
    }

    .floating-tooltip h4 {
        color: #0088cc;
        margin-bottom: 10px;
        font-size: 16px;
    }

    .floating-tooltip p {
        color: #666;
        font-size: 14px;
        line-height: 1.5;
    }

    .floating-stats {
        position: fixed;
        top: 20px;
        left: 20px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        z-index: 998;
        border: 1px solid rgba(0, 136, 204, 0.2);
    }

    .stat-item {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        font-size: 14px;
    }

    .stat-item:last-child {
        margin-bottom: 0;
    }

    .stat-icon {
        width: 20px;
        margin-right: 8px;
        opacity: 0.7;
    }

    .floating-nav {
        position: fixed;
        top: 50%;
        left: 20px;
        transform: translateY(-50%);
        z-index: 997;
    }

    .nav-button {
        display: block;
        width: 50px;
        height: 50px;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 2px solid #0088cc;
        border-radius: 50%;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        color: #0088cc;
        text-decoration: none;
    }

    .nav-button:hover {
        background: #0088cc;
        color: white;
        transform: scale(1.1);
        box-shadow: 0 4px 15px rgba(0, 136, 204, 0.3);
    }

    /* ========== ANIMATED FLOATING CARDS ========== */
    .floating-card {
        animation: float 6s ease-in-out infinite;
        margin-bottom: 20px;
    }

    .floating-card:nth-child(2) {
        animation-delay: 2s;
    }

    .floating-card:nth-child(3) {
        animation-delay: 4s;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    /* ========== FLOATING HEALTH TIPS ========== */
    .health-tip {
        position: absolute;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        font-size: 14px;
        color: #333;
        border-left: 3px solid #4caf50;
        opacity: 0;
        animation: fadeInOut 8s infinite;
    }

    .health-tip.show {
        opacity: 1;
    }

    @keyframes fadeInOut {
        0%, 100% { opacity: 0; transform: translateY(10px); }
        10%, 90% { opacity: 1; transform: translateY(0); }
    }

    /* ========== FLOATING PARTICLES ========== */
    .floating-particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
        overflow: hidden;
    }

    .particle {
        position: absolute;
        background: rgba(0, 136, 204, 0.1);
        border-radius: 50%;
        animation: particleFloat 15s linear infinite;
    }

    .particle:nth-child(1) { width: 4px; height: 4px; left: 10%; animation-delay: 0s; }
    .particle:nth-child(2) { width: 6px; height: 6px; left: 20%; animation-delay: 2s; }
    .particle:nth-child(3) { width: 3px; height: 3px; left: 30%; animation-delay: 4s; }
    .particle:nth-child(4) { width: 5px; height: 5px; left: 40%; animation-delay: 6s; }
    .particle:nth-child(5) { width: 4px; height: 4px; left: 50%; animation-delay: 8s; }
    .particle:nth-child(6) { width: 6px; height: 6px; left: 60%; animation-delay: 10s; }
    .particle:nth-child(7) { width: 3px; height: 3px; left: 70%; animation-delay: 12s; }
    .particle:nth-child(8) { width: 5px; height: 5px; left: 80%; animation-delay: 14s; }

    @keyframes particleFloat {
        0% { transform: translateY(100vh) rotate(0deg); }
        100% { transform: translateY(-100px) rotate(360deg); }
    }

    </style>
    """,
    unsafe_allow_html=True
    )

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">Check Your Diabetes Risk</h1>
            <p class="hero-subtitle">
                Get an instant health prediction based on your medical information. 
                Our advanced AI model analyzes your data to help you understand your diabetes risk level.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Floating particles background
    st.markdown("""
    <div class="floating-particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    """, unsafe_allow_html=True)

    # Floating stats
    st.markdown("""
    <div class="floating-stats">
        <div class="stat-item">
            <span class="stat-icon">📊</span>
            <span>AI-Powered Analysis</span>
        </div>
        <div class="stat-item">
            <span class="stat-icon">⚡</span>
            <span>Instant Results</span>
        </div>
        <div class="stat-item">
            <span class="stat-icon">🛡️</span>
            <span>Privacy Protected</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Floating navigation
    st.markdown("""
    <div class="floating-nav">
        <button class="nav-button" onclick="document.querySelector('.hero-section').scrollIntoView({behavior: 'smooth'})">🏠</button>
        <button class="nav-button" onclick="document.querySelectorAll('.form-section')[0].scrollIntoView({behavior: 'smooth'})">👤</button>
        <button class="nav-button" onclick="document.querySelectorAll('.form-section')[1].scrollIntoView({behavior: 'smooth'})">🚬</button>
        <button class="nav-button" onclick="document.querySelectorAll('.form-section')[2].scrollIntoView({behavior: 'smooth'})">🔬</button>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    # Form Section
    st.markdown('<div class="form-section floating-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Personal Information")
        gendere=st.radio("Select Gender",["Female","Male"])
        if gendere=="Female":
            st.success("✓ Selected: **Female**")
        else:
            st.success("✓ Selected: **Male**")
        
        age = st.slider("How old are you?", 0, 100, 25)
        st.info(f"📅 Your age: **{age}** years old")
    
    with col2:
        st.markdown("### ❤️ Medical Conditions")
        hypertension=st.radio("Do you have hypertension?", [1, 0], format_func=lambda x: "Yes" if x==1 else "No")
        if hypertension==1:
            st.error("⚠ You have hypertension")
        else:
            st.success("✓ No hypertension")
        
        heart_disease=st.radio("Do you have heart disease?", [1, 0], format_func=lambda x: "Yes" if x==1 else "No")
        if heart_disease==1:
            st.error("⚠ You have heart disease")
        else:
            st.success("✓ No heart disease")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="form-section floating-card">', unsafe_allow_html=True)
    
    st.markdown("### 🚬 Lifestyle Information")
    smoking_history=st.radio("Do you have smoking history?", ["never","ever","former","current","unknown"])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="form-section floating-card">', unsafe_allow_html=True)
    
    st.markdown("### 🔬 Medical Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        bmi = st.number_input("Insert your BMI", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
        st.info(f"📊 Your BMI: **{bmi:.2f}**")
    
    with col2:
        HbA1c_level = st.number_input("Enter your HbA1c Level", min_value=0.0, max_value=15.0, value=5.5, step=0.1)
        st.info(f"📈 Your HbA1c: **{HbA1c_level:.2f}%**")
    
    with col3:
        blood_glucose_level = st.number_input("Enter your Blood Glucose Level", min_value=0.0, max_value=500.0, value=100.0, step=1.0)
        st.info(f"🩸 Your Glucose: **{blood_glucose_level:.0f}** mg/dL")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    ge=gender.transform([gendere])[0]
    smk=smoking.transform([smoking_history])[0]

    f=[[ge,age,hypertension,heart_disease,smk,bmi,HbA1c_level,blood_glucose_level]] 

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        a=st.button("🏥 Get Prediction", use_container_width=True)

    # Floating Health Tips
    st.markdown("""
    <div class="floating-tooltip" id="healthTip">
        <h4>💡 Health Tip</h4>
        <p>Maintain a healthy BMI between 18.5-24.9, regular exercise, and balanced diet to reduce diabetes risk.</p>
    </div>
    """, unsafe_allow_html=True)

    # JavaScript to show/hide floating tooltip
    st.markdown("""
    <script>
        let tipShown = false;
        setInterval(() => {
            const tip = document.getElementById('healthTip');
            if (tip) {
                tip.classList.toggle('show');
            }
        }, 10000);
    </script>
    """, unsafe_allow_html=True)
    
    if a:
        s=scaler.transform(f)
        pred=model.predict(s)
        
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        
        if pred[0]==1:
            st.markdown("""
            <div style='text-align: center;'>
                <h2 style='color: #e74c3c; font-size: 32px;'>⚠️ Diabetes Risk Detected</h2>
                <p style='font-size: 18px; color: #333; margin: 20px 0;'>
                    Based on your medical information, our analysis suggests a <b>HIGH RISK</b> of diabetes.
                </p>
                <p style='font-size: 16px; color: #666;'>
                    We recommend consulting with a healthcare professional for proper diagnosis and guidance.
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.error("🔴 **Diabetes Detected** - Please seek medical consultation")
        else:
            st.markdown("""
            <div style='text-align: center;'>
                <h2 style='color: #4caf50; font-size: 32px;'>✅ Low Diabetes Risk</h2>
                <p style='font-size: 18px; color: #333; margin: 20px 0;'>
                    Based on your medical information, our analysis suggests a <b>LOW RISK</b> of diabetes.
                </p>
                <p style='font-size: 16px; color: #666;'>
                    Continue maintaining a healthy lifestyle and regular check-ups.
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.success("🟢 **No Diabetes Detected** - Keep up the good health!")
        
        st.markdown("</div>", unsafe_allow_html=True)
main()