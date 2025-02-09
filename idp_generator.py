import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

# Updated role database with Treasury, Sales, and Marketing roles in a UAE bank context
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

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    return " ".join([t.page_content for t in texts])

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
        idp_recommendations.append({"Competency": comp, "Required Proficiency": level, "Development Mode": mode})

    return pd.DataFrame(idp_recommendations)

