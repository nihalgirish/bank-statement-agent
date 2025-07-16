import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import re
from fpdf import FPDF
import pdfplumber
import io

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Bank Statement Filter", layout="centered", initial_sidebar_state="collapsed")

# ---------- HEADER ----------
st.markdown("""
    <h1 style='text-align: center; color: white;'>🏦 Smart Bank Statement AI</h1>
    <p style='text-align: center; color: white;'>Upload your CSV or PDF and extract statements for any period like <b>“6 months”</b> or <b>“1 year 2 months”</b>.</p>
    <hr style="border-color: #444;">
""", unsafe_allow_html=True)

# ---------- UPLOAD ----------
uploaded_file = st.file_uploader("📁 Upload your bank_statement.csv or bank_statement.pdf", type=["csv", "pdf"])

# ---------- TIME RANGE INPUT ----------
time_query = st.text_input("⏱️ Enter Time Range (e.g. '6 months', '1 year 2 months')")

# ---------- PROCESS ----------
df = None
if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]
    
    # --------- CSV Upload ---------
    if file_type == "csv":
        df = pd.read_csv(uploaded_file)

    # --------- PDF Upload ---------
    elif file_type == "pdf":
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                all_rows = []
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        all_rows.extend(table[1:])  # skip header

                df = pd.DataFrame(all_rows, columns=["Date", "Description", "Amount", "Balance"])
                df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
                df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce")
        except:
            st.error("❌ Could not read table from PDF. Make sure it's a proper table format.")
            st.stop()

# ---------- Filter Logic ----------
if df is not None and time_query:
    try:
        df["Date"] = pd.to_datetime(df["Date"])
    except:
        st.error("❌ Date column couldn't be parsed. Please check your file format.")
        st.stop()

    end_date = datetime.today()
    start_date = end_date
    matches = re.findall(r"(\d+)\s*(year|month|week|day)s?", time_query.lower())

    if not matches:
        st.error("❌ Please enter a time query like '6 months', '1 year 2 months'")
        st.stop()

    for value, unit in matches:
        value = int(value)
        if unit == "year":
            start_date -= timedelta(days=365 * value)
        elif unit == "month":
            start_date -= timedelta(days=30 * value)
        elif unit == "week":
            start_date -= timedelta(weeks=value)
        elif unit == "day":
            start_date -= timedelta(days=value)

    filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    # ---------- Display ----------
    st.success(f"✅ Transactions from {start_date.date()} to {end_date.date()}")
    st.dataframe(filtered, use_container_width=True)

    # ---------- Download CSV ----------
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("💾 Download as CSV", data=csv, file_name="filtered_statement.csv", mime="text/csv")

    # ---------- Download PDF ----------
    def generate_pdf(dataframe):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Filtered Statement: {start_date.date()} to {end_date.date()}", ln=True, align='C')
        pdf.ln(5)

        col_widths = [35, 70, 30, 30]
        headers = ["Date", "Description", "Amount", "Balance"]
        for i, col in enumerate(headers):
            pdf.cell(col_widths[i], 10, col, border=1)
        pdf.ln()

        for _, row in dataframe.iterrows():
            pdf.cell(col_widths[0], 10, row["Date"].strftime("%Y-%m-%d"), border=1)
            desc = row["Description"][:30] + "..." if len(row["Description"]) > 33 else row["Description"]
            pdf.cell(col_widths[1], 10, desc, border=1)
            pdf.cell(col_widths[2], 10, f"{row['Amount']:.2f}", border=1)
            pdf.cell(col_widths[3], 10, f"{row['Balance']:.2f}", border=1)
            pdf.ln()

        return pdf.output(dest='S').encode('latin-1')

    pdf_data = generate_pdf(filtered)
    st.download_button("📄 Export as PDF", data=pdf_data, file_name="filtered_statement.pdf", mime="application/pdf")
