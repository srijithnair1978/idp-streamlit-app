import pandas as pd
from PyPDF2 import PdfReader

# Updated role database with additional competencies & proficiency levels
roles_data = {
    "Current Role": [
        "Relationship Manager", "Credit Analyst", "Treasury Specialist",
        "Treasury Analyst", "Senior Treasury Specialist",
        "Sales Executive", "Senior Sales Manager",
        "Marketing Analyst", "Senior Marketing Manager"
    ],
    "Future Role": [
        "Senior Relationship Manager", "Senior Credit Risk Manager", "Head of Treasury",
        "Treasury Manager", "Head of Treasury Operations",
        "Sales Manager", "Head of Corporate Sales",
        "Marketing Manager", "Head of Digital Marketing"
    ],
    "Competencies": [
        ["Client Relationship", "Risk Management", "Financial Analysis"],
        ["Risk Assessment", "Financial Modelling", "Regulatory Compliance"],
        ["Liquidity Management", "Market Risk", "Investment Strategy"],
        ["Foreign Exchange", "Liquidity Risk", "Derivatives Trading"],
        ["Treasury Operations", "Risk Hedging", "Cash Flow Management"],
        ["Customer Acquisition", "Negotiation", "Sales Analytics"],
        ["Sales Strategy", "B2B Partnerships", "Revenue Optimization"],
        ["Brand Management", "Market Research", "Product Positioning"],
        ["Digital Marketing", "SEO & PPC", "Campaign Analytics"]
    ],
    "Proficiency Level Required": [
        ["Expert", "Advanced", "Advanced"],
        ["Advanced", "Expert", "Advanced"],
        ["Expert", "Expert", "Advanced"],
        ["Advanced", "Expert", "Advanced"],
        ["Expert", "Advanced", "Advanced"],
        ["Advanced", "Expert", "Advanced"],
        ["Expert", "Expert", "Advanced"],
        ["Advanced", "Expert", "Advanced"],
        ["Expert", "Advanced", "Advanced"]
    ]
}

roles_df = pd.DataFrame(roles_data)

# Mapping for development needs descriptions
development_needs = {
    "Client Relationship": "Enhance client communication and stakeholder management.",
    "Risk Management": "Develop skills in identifying and mitigating financial risks.",
    "Financial Analysis": "Improve ability to analyze financial reports and market trends.",
    "Risk Assessment": "Enhance risk evaluation strategies for credit decisions.",
    "Financial Modelling": "Gain expertise in predictive financial modelling techniques.",
    "Regulatory Compliance": "Deepen understanding of compliance frameworks and regulations.",
    "Liquidity Management": "Optimize cash and liquidity management strategies.",
    "Market Risk": "Strengthen knowledge of market risk assessment and trading strategies.",
    "Investment Strategy": "Advance expertise in portfolio and investment planning.",
    "Foreign Exchange": "Gain deeper understanding of FX markets and risk mitigation.",
    "Liquidity Risk": "Enhance forecasting and liquidity planning capabilities.",
    "Derivatives Trading": "Expand expertise in derivatives and risk hedging strategies.",
    "Treasury Operations": "Improve efficiency in treasury functions and cash management.",
    "Risk Hedging": "Develop skills in hedging strategies for financial risk.",
    "Cash Flow Management": "Enhance forecasting and cash allocation methodologies.",
    "Customer Acquisition": "Improve techniques for acquiring and retaining customers.",
    "Negotiation": "Enhance negotiation skills for corporate deals and sales.",
    "Sales Analytics": "Develop data-driven sales decision-making capabilities.",
    "Sales Strategy": "Strengthen sales leadership and strategic sales planning.",
    "B2B Partnerships": "Improve collaboration and deal structuring for B2B sales.",
    "Revenue Optimization": "Develop strategies for increasing profitability and sales revenue.",
    "Brand Management": "Enhance brand positioning and corporate communication strategies.",
    "Market Research": "Strengthen ability to analyze market trends and consumer behavior.",
    "Product Positioning": "Improve marketing and product differentiation strategies.",
    "Digital Marketing": "Advance digital campaign strategies including SEO & PPC.",
    "SEO & PPC": "Gain expertise in search engine optimization and paid advertising.",
    "Campaign Analytics": "Develop ability to analyze and optimize marketing campaigns."
}

def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF file."""
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

def generate_idp(hipo_cv_text, jd_text, role_selected):
    """Generate Individual Development Plan (IDP) based on competency gaps."""
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
        mode = "E-learning & Virtual Courses" if level == "Basic" else "On-the-job Training & Mentoring"
        timeline = "3-6 months" if level == "Advanced" else "6-12 months"
        description = development_needs.get(comp, "Enhance skills in this area.")

        idp_recommendations.append({
            "Role": role_selected,
            "Competency": comp,
            "Current Proficiency": "Basic",  # Assuming basic unless detected from CV
            "Required Proficiency": level,
            "Development Need": description,
            "Action Plan": mode,
            "Estimated Timeline": timeline
        })

    return pd.DataFrame(idp_recommendations)
