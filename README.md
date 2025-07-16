# 🏦 Smart Bank Statement AI Agent

An AI-powered tool built with Streamlit that allows users to upload bank statements in **CSV or PDF format**, enter human-friendly date queries (like "6 months" or "1 year 2 months"), and instantly extract a filtered version of the statement. Users can download results in **CSV** and **PDF** formats.

---

## 👤 Developer

**Nihal Girish**  
GitHub: [@nihalgirish](https://github.com/nihalgirish)

---

## 🚀 Live Demo

**Try the app here:**  
🔗 [https://bank-statement-agent-1.streamlit.app/](https://bank-statement-agent-1.streamlit.app/)

---

## 📦 Features

- 🔁 Upload your **bank statement** in CSV or PDF
- 🧠 Input natural time periods like:
  - `6 months`
  - `1 year 2 months`
  - `3 weeks`
- 🧾 View all matched transactions in-browser
- 📄 Download results as:
  - CSV file
  - Clean, formatted PDF
- 🎨 Beautiful, minimal interface with smart layout and white header

---

## 📁 Sample Data Format

### CSV Columns Required:
- `Date` (format: YYYY-MM-DD or DD-MM-YYYY)
- `Description`
- `Amount`
- `Balance`

### PDF Requirements:
- Must contain a **clear table format** (4-column structure as above)
- Parsed using `pdfplumber` backend

---

## 🧪 Sample Inputs

You can enter time queries like:
- 6 months
- 1 year 2 months
- 2 weeks
- 3 months and 1 week

---

## 📥 How to Run Locally

### 1. Clone this repository

bash
git clone https://github.com/nihalgirish/bank-statement-agent.git
cd bank-statement-agent
2. Install required libraries
bash
Copy
Edit
pip install -r requirements.txt
3. Launch the app
bash
Copy
Edit
streamlit run bank_agent_app.py
The app will open in your browser.

🛠 Built With
Streamlit — Web UI framework

Pandas — Data manipulation

FPDF — Export to PDF

pdfplumber — Extract tables from PDFs

📬 Contact
For feedback, ideas, or collaboration:

GitHub: @nihalgirish

📘 License
This project is open-source under the MIT License.

