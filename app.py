import streamlit as st
import pandas as pd

from detector import detect_inconsistencies
from risk_engine import compute_risk_score
from rag import DatasetRAG
from pdf_parser import extract_clauses
from llm_explainer import explain_issue

st.set_page_config(page_title="Legal AI System", layout="wide")

st.sidebar.title("⚖️ Legal AI System")

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Violations", "Risk Analysis", "Chat AI", "PDF Insights"]
)

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
pdf_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

rag = DatasetRAG()

df = None

# ---------------- LOAD CSV ----------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "DateOfJoining" in df.columns:
        df["DateOfJoining"] = pd.to_datetime(df["DateOfJoining"], errors="coerce")

    if "DateOfExit" in df.columns:
        df["DateOfExit"] = pd.to_datetime(df["DateOfExit"], errors="coerce")

    if "DateOfJoining" in df.columns:
        df["Tenure_Days"] = (df["DateOfExit"] - df["DateOfJoining"]).dt.days

    df = detect_inconsistencies(df)
    df = compute_risk_score(df)

    rag.add_texts(df.astype(str).apply(lambda x: " | ".join(x), axis=1).tolist())

# ---------------- LOAD PDF ----------------
clauses = None

if pdf_file:
    clauses, _ = extract_clauses(pdf_file)
    rag.add_texts([c["clause"] for c in clauses])

# build index
if uploaded_file or pdf_file:
    rag.build_index()

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 Dashboard")

    if df is not None:
        col1, col2, col3 = st.columns(3)

        col1.metric("Records", len(df))
        col2.metric("Avg Risk", round(df["RiskScore"].mean(), 2))
        col3.metric("High Risk", len(df[df["RiskScore"] > 60]))

        st.dataframe(df, use_container_width=True)

# ---------------- VIOLATIONS ----------------
elif page == "Violations":
    st.title("🚨 Red / Green Flags")

    if df is not None:
        st.dataframe(df[["EmployeeID", "Name", "Issues", "Flags"]])

# ---------------- RISK ----------------
elif page == "Risk Analysis":
    st.title("📊 Risk Scores")

    if df is not None:
        st.dataframe(df[["EmployeeID", "RiskScore", "Flags"]])
        st.bar_chart(df["RiskScore"])

# ---------------- CHAT ----------------
elif page == "Chat AI":
    st.title("💬 Legal AI Chat")

    query = st.text_input("Ask anything")

    if query:
        answer = rag.ask(query)
        st.success(answer)

# ---------------- PDF ----------------
elif page == "PDF Insights":
    st.title("📄 Contract Clauses")

    if clauses:
        for c in clauses[:30]:
            color = "🔴" if "shall not" in c["clause"].lower() else "🟢"
            st.markdown(f"{color} Page {c['page']}: {c['clause']}")
