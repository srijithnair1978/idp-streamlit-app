import pandas as pd
import tempfile
import time
import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

# Sample database of roles, future roles, and required competencies
roles_data = {
    "Current Role": ["Relationship Manager", "Credit Analyst", "Treasury Specialist"],
    "Future Role": ["Senior Relationship Manager", "Senior Credit Risk Manager", "Head of Treasury"],
    "Competencies": [
        ["Client Relationship", "Risk Management", "Financial Analysis"],
        ["Risk Assessment", "Financial Modelling", "Regulatory Compliance"],
        ["Liquidity Management", "Market Risk", "Investment Strategy"]
    ],
    "Proficiency Level Required": [
        ["Expert", "Advanced", "Advanced"],
        ["Advanced", "Expert", "Advanced"],
        ["Expert", "Expert", "Advanced"]
    ]
}

roles_df = pd.DataFrame(roles_data)

def extract_text_from_pdf(uploaded_file):
    """Extract text from a Streamlit-uploaded PDF file."""
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())  
            temp_file_path = temp_file.name  

        start_time = time.time()
        loader = PyPDFLoader(temp_file_path)
        documents = loader.load()
        
        if time.time() - start_time > 10:
            return "⚠️ Processing timeout. PDF is too large."

        text = " ".join([page.page_content for page in documents])

        return text  

    return ""  

def generate_idp(hipo_cv_text, jd_text, role_selected):
    """Generate a detailed Individual Development Plan (IDP)."""

    role_data = roles_df[roles_df["Future Role"] == role_selected]
    
    required_competencies = role_data["Competencies"].values[0]
    proficiency_levels = role_data["Proficiency Level Required"].values[0]

    # Extract existing competencies from CV
    existing_competencies = [comp for comp in required_competencies if comp.lower() in hipo_cv_text.lower()]
    
    # Identify competency gaps
    competency_gaps = [comp for comp in required_competencies if comp not in existing_competencies]
    proficiency_gaps = {comp: level for comp, level in zip(required_competencies, proficiency_levels) if comp in competency_gaps}

    # IDP recommendations
    idp_recommendations = []
    for comp, level in proficiency_gaps.items():
        if level == "Expert":
            mode = "Executive Coaching"
            timeline = "6-12 months"
            description = f"Develop advanced expertise in {comp} through high-level coaching with industry leaders."
            action_plan = "Schedule 1-on-1 executive coaching sessions and participate in leadership forums."
        elif level == "Advanced":
            mode = "On-the-job Training & Mentoring"
            timeline = "3-6 months"
            description = f"Enhance proficiency in {comp} through real-world project assignments and mentoring."
            action_plan = "Shadow senior professionals, take on complex projects, and engage in knowledge-sharing sessions."
        else:
            mode = "E-learning & Virtual Courses"
            timeline = "1-3 months"
            description = f"Build foundational skills in {comp} through structured online courses."
            action_plan = "Enroll in virtual courses, complete interactive assignments, and take skill assessments."

        idp_recommendations.append({
            "Future Role": role_selected,
            "Competency": comp,
            "Current Proficiency": "Basic" if comp not in existing_competencies else "Intermediate",  
            "Required Proficiency": level,
            "Development Need": description,
            "Action Plan": action_plan,
            "Mode of Training": mode,
            "Timeline": timeline
        })

    return pd.DataFrame(idp_recommendations)
