import streamlit as st
import pandas as pd
from idp_generator import extract_text_from_pdf, generate_idp, roles_df

# ✅ Updated Heading
st.title("Individual Development Plan (IDP) Created by Talent Management and Leadership Development Team")

# ✅ Step 1: Select Role
role_selected = st.selectbox("Select Future Role", roles_df["Future Role"].unique())

# ✅ Step 2: Upload JD & CV PDFs
uploaded_jd = st.file_uploader("Upload Job Description (JD) PDF", type=["pdf"])
uploaded_cv = st.file_uploader("Upload HiPo Employee's CV PDF", type=["pdf"])

if st.button("Generate IDP"):
    if uploaded_jd and uploaded_cv:
        # ✅ Extract Text from PDFs
        jd_text = extract_text_from_pdf(uploaded_jd)
        cv_text = extract_text_from_pdf(uploaded_cv)

        # ✅ Generate IDP
        idp_df = generate_idp(cv_text, jd_text, role_selected)

        # ✅ Display Results
        st.write(f"### 📄 IDP for {role_selected}")
        st.dataframe(idp_df)

        # ✅ Download as Excel
        output = "IDP_Output.xlsx"
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            idp_df.to_excel(writer, sheet_name="IDP", index=False)
        with open(output, "rb") as file:
            st.download_button("Download IDP as Excel", file, file_name="IDP_Output.xlsx")

    else:
        st.error("❌ Please upload both JD and CV PDFs!")
