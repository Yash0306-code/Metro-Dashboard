
import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import tempfile

st.set_page_config(page_title="Provider Dashboard", layout="wide")
st.title("📊 Metro Physicians Provider Dashboard")

# Load cleaned data
df = pd.read_excel("Perfect_Cleaned_Temp_With_RandomCodes.xlsx")

# Sidebar login
with st.sidebar:
    st.header("🔐 Secure Login")
    provider_names = df["Provider Name"].dropna().unique()
    selected_provider = st.selectbox("Select Provider", provider_names)
    input_code = st.text_input("Enter Access Code", type="password")
    login = st.button("Login")

if login:
    # Get correct code
    provider_code = df[df["Provider Name"] == selected_provider]["Code"].iloc[0]

    if input_code == provider_code or input_code == "admin":
        st.success(f"✅ Access granted for {selected_provider if input_code != 'admin' else 'Admin'}")
        
        if input_code == "admin":
            provider_df = df.copy()
        else:
            provider_df = df[df["Provider Name"] == selected_provider]

        st.subheader("📋 Provider Data")
        st.dataframe(provider_df)

        st.subheader("📈 Visual Insights")

        # Line chart of Total Pay
        if "Total Pay" in provider_df.columns:
            fig1 = px.line(provider_df, x="Pay Period", y="Total Pay", title="Total Pay Over Time", markers=True)
            st.plotly_chart(fig1, use_container_width=True)

        # Bar chart of Extra Shifts
        if "Extra shifts Pay" in provider_df.columns:
            fig2 = px.bar(provider_df, x="Pay Period", y="Extra shifts Pay", title="Extra Shift Pay")
            st.plotly_chart(fig2, use_container_width=True)

        # CME over time
        if "CME" in provider_df.columns:
            fig3 = px.line(provider_df, x="Pay Period", y="CME", title="CME Pay Trend", markers=True)
            st.plotly_chart(fig3, use_container_width=True)

        # JCMH vs St. Mary’s Pay
        if "JCMH Pay" in provider_df.columns and "St. Mary's Pay" in provider_df.columns:
            fig4 = px.bar(provider_df, x="Pay Period", y=["JCMH Pay", "St. Mary's Pay"], title="JCMH vs St. Mary's Pay")
            st.plotly_chart(fig4, use_container_width=True)

        # Weekend Pay trend
        if "Weekend Pay" in provider_df.columns:
            fig5 = px.line(provider_df, x="Pay Period", y="Weekend Pay", title="Weekend Pay Trend", markers=True)
            st.plotly_chart(fig5, use_container_width=True)

        # Encounter WRUs
        if "Encounter WRUs" in provider_df.columns:
            fig6 = px.line(provider_df, x="Pay Period", y="Encounter WRUs", title="Encounter WRUs Trend", markers=True)
            st.plotly_chart(fig6, use_container_width=True)

        # Bonus Metrics
        if "Bonus Metrics Pay" in provider_df.columns:
            fig7 = px.bar(provider_df, x="Pay Period", y="Bonus Metrics Pay", title="Bonus Metrics Pay")
            st.plotly_chart(fig7, use_container_width=True)

        # PDF Summary Download
        if st.button("📄 Download PDF Summary"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Provider Report - {selected_provider}", ln=True, align="C")
            for col in provider_df.columns:
                try:
                    val = provider_df[col].iloc[0]
                    pdf.cell(200, 10, txt=f"{col}: {val}", ln=True)
                except:
                    continue
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                pdf.output(tmpfile.name)
                with open(tmpfile.name, "rb") as f:
                    st.download_button("📥 Download PDF", f, file_name=f"{selected_provider}_summary.pdf")
    else:
        st.error("❌ Invalid code. Access denied.")
