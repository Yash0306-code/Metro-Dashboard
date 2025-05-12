
import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile
import os

st.title("📄 Provider Pay Breakdown + PDF Export")

uploaded_file = st.file_uploader("📂 Upload Payroll Excel File", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    provider_list = df['Provider Name'].dropna().unique()
    selected_provider = st.selectbox("👤 Select Provider", provider_list)

    df_filtered = df[df['Provider Name'] == selected_provider]

    st.write(f"### 💰 Pay Details for {selected_provider}")
    st.dataframe(df_filtered)

    # Generate PDF
    if st.button("📄 Download PDF Report"):
        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, f"Pay Summary - {selected_provider}", ln=True, align="C")

            def footer(self):
                self.set_y(-15)
                self.set_font("Arial", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}", align="C")

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", "", 12)

        for index, row in df_filtered.iterrows():
            for col in df_filtered.columns:
                pdf.cell(0, 10, f"{col}: {row[col]}", ln=True)
            pdf.ln(5)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            pdf.output(tmpfile.name)
            st.success("✅ PDF Generated!")
            with open(tmpfile.name, "rb") as file:
                btn = st.download_button(
                    label="📥 Click to Download PDF",
                    data=file,
                    file_name=f"{selected_provider.replace(' ', '_')}_Pay_Summary.pdf",
                    mime="application/pdf"
                )
