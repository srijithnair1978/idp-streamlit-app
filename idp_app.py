import streamlit as st
import pandas as pd
import io
from idp_generator import extract_text_from_pdf, generate_idp, roles_df

st.title("🚀 HiPo Individual Development Plan (IDP) Generator")

# Role selection
selected_role = st.selectbox("📌 Select Future Role", roles_df["Future Role"].tolist())

# Upload JD & CV
uploaded_jd = st.file_uploader("📄 Upload Job Description (PDF)", type=["pdf"])
uploaded_cv = st.file_uploader("📄 Upload HiPo CV (PDF)", type=["pdf"])

if st.button("Generate IDP"):
    if uploaded_jd and uploaded_cv:
        st.write("🔄 **Extracting text from Job Description...**")
        jd_text = extract_text_from_pdf(uploaded_jd)
        
        st.write("🔄 **Extracting text from HiPo CV...**")
        cv_text = extract_text_from_pdf(uploaded_cv)

        st.write("🔄 **Generating IDP...**")
        idp_df = generate_idp(cv_text, jd_text, selected_role)

        # Display the IDP DataFrame
        st.subheader("✅ **Individual Development Plan (IDP)**")
        st.dataframe(idp_df)

        # Convert DataFrame to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            idp_df.to_excel(writer, sheet_name="IDP", index=False)
        excel_data = output.getvalue()

        # Create a download button
        st.download_button(
            label="📥 Download IDP as Excel",
            data=excel_data,
            file_name=f"IDP_{selected_role}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.error("❌ Please upload both the Job Description (JD) and HiPo CV.")
