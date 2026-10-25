import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import os

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Fraud Detection Analytics",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================
# LOGIN DETAILS - CHANGE THESE WHEN REQUIRED
# ============================================================

USERNAME = "sony"
PASSWORD = "Sony@4961"

# ============================================================
# FILE PATHS
# ============================================================

DATA_FILE = "Fraud_Detection_Cleaned.csv"
BACKGROUND_FILE = "Fin-Care Office.png"

# ============================================================
# BACKGROUND IMAGE
# ============================================================

def set_background(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as file:
            image_data = base64.b64encode(file.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image:
                    linear-gradient(
                        rgba(255, 255, 255, 0.88),
                        rgba(255, 255, 255, 0.88)
                    ),
                    url("data:image/png;base64,{image_data}");
                background-size: cover;
                background-position: center top;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(
            f"Background image not found: {image_file}"
        )

set_background(BACKGROUND_FILE)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()

    if "Transaction_Date" in data.columns:
        data["Transaction_Date"] = pd.to_datetime(
            data["Transaction_Date"],
            errors="coerce"
        )

    if "Transaction_Amount" in data.columns:
        data["Transaction_Amount"] = pd.to_numeric(
            data["Transaction_Amount"],
            errors="coerce"
        ).fillna(0)

    if "Fraud_Flag" in data.columns:
        data["Fraud_Flag"] = pd.to_numeric(
            data["Fraud_Flag"],
            errors="coerce"
        ).fillna(0).astype(int)

    return data

# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.write("")

    left, header, right = st.columns([1, 3, 1])

    with header:
        st.markdown(
            "<h2 style='text-align:center;'>"
            "🛡️ Fraud Detection in Online Transactions</h2>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align:center;'>"
            "Fin-Care Starpowerz Digital Technology Pvt. Ltd."
            "</p>",
            unsafe_allow_html=True
        )

    st.divider()

    left, login_box, right = st.columns([1, 2, 1])

    with login_box:
        st.subheader("🔐 Login")

        user_id = st.text_input(
            "👤 User ID",
            placeholder="Enter User ID"
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter Password"
        )

        if st.button("🔐 Login", use_container_width=True):

            if user_id == USERNAME and password == PASSWORD:
                st.session_state.logged_in = True
                st.session_state.page = "Home"
                st.rerun()
            else:
                st.error("❌ Invalid User ID or Password.")

    st.stop()

# ============================================================
# LOAD DATA AFTER LOGIN
# ============================================================

if not os.path.exists(DATA_FILE):
    st.error(f"Dataset not found: {DATA_FILE}")
    st.info("Place the CSV file in the same folder as Stream.py.")
    st.stop()

try:
    df = load_data(DATA_FILE)
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

if df.empty:
    st.error("The dataset is empty.")
    st.stop()

# ============================================================
# COLUMN HELPERS
# ============================================================

def numeric_column(column):
    if column in df.columns:
        return pd.to_numeric(
            df[column], errors="coerce"
        ).fillna(0)
    return pd.Series(0, index=df.index, dtype=float)

fraud_flag = numeric_column("Fraud_Flag")
amount = numeric_column("Transaction_Amount")

total_transactions = len(df)
fraud_transactions = int((fraud_flag == 1).sum())
legitimate_transactions = total_transactions - fraud_transactions
fraud_rate = (
    fraud_transactions / total_transactions * 100
    if total_transactions else 0
)
total_amount = amount.sum()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.title("🛡️ Fraud Detection")
    st.caption("Fin-Care Starpowerz Digital Technology Pvt. Ltd.")
    st.divider()

    pages = {
        "🏠 Home": "Home",
        "📊 Dashboard": "Dashboard",
        "📈 Fraud Analytics": "Fraud Analytics",
        "⚠️ Risk Analysis": "Risk Analysis",
        "💳 Transactions": "Transactions",
        "🔎 Fraud Prediction": "Fraud Prediction",
        "📋 Model Performance": "Model Performance"
    }

    for label, page_name in pages.items():
        if st.button(label, use_container_width=True):
            st.session_state.page = page_name
            st.rerun()

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.rerun()

# ============================================================
# HOME
# ============================================================

if st.session_state.page == "Home":

    st.title("🛡️ Welcome to Fraud & Risk Management Analytics")

    st.write(
        "Analyze online transaction data, fraud patterns, "
        "risk indicators and transaction behaviour."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📊 Dashboard\n\nView fraud KPIs and trends.")

    with col2:
        st.warning("⚠️ Risk Analysis\n\nReview transaction risk indicators.")

    with col3:
        st.success("🔎 Fraud Prediction\n\nExplore fraud prediction inputs.")

    st.subheader("Project Overview")

    st.write(
        "This project analyzes transaction data to identify "
        "fraudulent transactions and examine patterns by "
        "transaction type, merchant category, customer type, "
        "device type and risk indicators."
    )

# ============================================================
# DASHBOARD
# ============================================================

elif st.session_state.page == "Dashboard":

    st.title("🛡️ Fraud Detection in Online Transactions")
    st.caption("Fin-Care Starpowerz Digital Technology Pvt. Ltd.")
    st.subheader("Fraud & Risk Management Analytics Dashboard")

    k1, k2, k3 = st.columns(3)

    k1.metric("Total Transactions", f"{total_transactions:,}")
    k2.metric("Fraudulent Transactions", f"{fraud_transactions:,}")
    k3.metric("Legitimate Transactions", f"{legitimate_transactions:,}")

    k4, k5, k6 = st.columns(3)

    k4.metric("Fraud Rate", f"{fraud_rate:.2f}%")
    k5.metric("Total Transaction Amount", f"{total_amount:,.2f}")
    k6.metric(
        "Average Transaction Amount",
        f"{amount.mean():,.2f}" if len(amount) else "0"
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        if "Fraud_Status" in df.columns:
            counts = df["Fraud_Status"].astype(str).value_counts()
            fig = px.pie(
                values=counts.values,
                names=counts.index,
                title="Fraudulent vs Legitimate Transactions",
                hole=0.45
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Fraud_Status column is unavailable.")

    with right:
        if "Transaction_Type" in df.columns:
            temp = df.assign(Fraud_Flag=fraud_flag)
            fraud_types = temp[temp["Fraud_Flag"] == 1]
            counts = fraud_types["Transaction_Type"].value_counts()

            fig = px.bar(
                x=counts.index,
                y=counts.values,
                title="Fraudulent Transactions by Transaction Type",
                labels={
                    "x": "Transaction Type",
                    "y": "Fraudulent Transactions"
                },
                color=counts.values
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Transaction_Type column is unavailable.")

    left, right = st.columns(2)

    with left:
        if "Transaction_Date" in df.columns:
            temp = df.copy()
            temp["Fraud_Flag"] = fraud_flag
            temp = temp[temp["Fraud_Flag"] == 1].copy()
            temp["Year"] = temp["Transaction_Date"].dt.year

            yearly = temp.groupby("Year").size().reset_index(
                name="Fraudulent Transactions"
            )

            if not yearly.empty:
                fig = px.line(
                    yearly,
                    x="Year",
                    y="Fraudulent Transactions",
                    markers=True,
                    title="Fraudulent Transactions Trend by Year"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No valid transaction dates available.")
        else:
            st.info("Transaction_Date column is unavailable.")

    with right:
        if "Merchant_Category" in df.columns:
            temp = df.assign(Fraud_Flag=fraud_flag)
            counts = (
                temp[temp["Fraud_Flag"] == 1]
                ["Merchant_Category"]
                .value_counts()
                .head(10)
            )

            fig = px.bar(
                x=counts.values,
                y=counts.index,
                orientation="h",
                title="Fraud by Merchant Category",
                labels={"x": "Fraudulent Transactions", "y": "Merchant Category"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Merchant_Category column is unavailable.")

    left, right = st.columns(2)

    with left:
        if "Customer_Type" in df.columns:
            temp = df.assign(Fraud_Flag=fraud_flag)
            counts = (
                temp[temp["Fraud_Flag"] == 1]["Customer_Type"]
                .value_counts()
            )

            fig = px.bar(
                x=counts.index,
                y=counts.values,
                title="Fraudulent Transactions by Customer Type",
                labels={"x": "Customer Type", "y": "Fraudulent Transactions"}
            )
            st.plotly_chart(fig, use_container_width=True)

    with right:
        if "Device_Type" in df.columns:
            temp = df.assign(Fraud_Flag=fraud_flag)
            counts = (
                temp[temp["Fraud_Flag"] == 1]["Device_Type"]
                .value_counts()
            )

            fig = px.bar(
                x=counts.index,
                y=counts.values,
                title="Fraudulent Transactions by Device Type",
                labels={"x": "Device Type", "y": "Fraudulent Transactions"}
            )
            st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)

    with left:
        if "Location_Mismatch" in df.columns:
            mismatch = df["Location_Mismatch"].astype(str).value_counts()

            fig = px.pie(
                values=mismatch.values,
                names=mismatch.index,
                title="Location Mismatch Analysis",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

    with right:
        risk_columns = [
            c for c in
            ["IP_Risk_Score", "Device_Risk_Score", "Velocity_Score"]
            if c in df.columns
        ]

        if risk_columns and "Fraud_Status" in df.columns:
            temp = df.copy()
            for column in risk_columns:
                temp[column] = numeric_column(column)

            risk_data = temp.groupby("Fraud_Status")[risk_columns].mean()
            fig = px.bar(
                risk_data.reset_index().melt(
                    id_vars="Fraud_Status",
                    var_name="Risk Indicator",
                    value_name="Average Score"
                ),
                x="Fraud_Status",
                y="Average Score",
                color="Risk Indicator",
                barmode="group",
                title="Average Risk Score by Fraud Status"
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================
# FRAUD ANALYTICS
# ============================================================

elif st.session_state.page == "Fraud Analytics":

    st.title("📈 Fraud Analytics")

    if "Transaction_Type" in df.columns:
        temp = df.assign(Fraud_Flag=fraud_flag)
        counts = (
            temp[temp["Fraud_Flag"] == 1]["Transaction_Type"]
            .value_counts()
        )

        st.subheader("Fraud by Transaction Type")
        st.bar_chart(counts)

    if "Merchant_Category" in df.columns:
        temp = df.assign(Fraud_Flag=fraud_flag)
        counts = (
            temp[temp["Fraud_Flag"] == 1]["Merchant_Category"]
            .value_counts()
        )

        st.subheader("Fraud by Merchant Category")
        st.bar_chart(counts)

    if "Transaction_Date" in df.columns:
        temp = df.copy()
        temp["Fraud_Flag"] = fraud_flag
        temp = temp[temp["Fraud_Flag"] == 1].copy()
        temp["Year"] = temp["Transaction_Date"].dt.year

        st.subheader("Yearly Fraud Trend")
        st.line_chart(temp.groupby("Year").size())

# ============================================================
# RISK ANALYSIS
# ============================================================

elif st.session_state.page == "Risk Analysis":

    st.title("⚠️ Risk Analysis")

    risk_columns = [
        c for c in [
            "IP_Risk_Score",
            "Device_Risk_Score",
            "Velocity_Score",
            "Location_Mismatch",
            "International_Transaction",
            "Failed_Transactions_24H"
        ]
        if c in df.columns
    ]

    if risk_columns:
        st.subheader("Risk Indicator Summary")
        st.dataframe(df[risk_columns].describe(include="all"))
    else:
        st.info("No supported risk columns were found.")

    if "Fraud_Status" in df.columns:
        st.subheader("Transactions by Fraud Status")
        st.bar_chart(df["Fraud_Status"].value_counts())

    if "Location_Mismatch" in df.columns:
        st.subheader("Location Mismatch")
        st.bar_chart(df["Location_Mismatch"].astype(str).value_counts())

    if "International_Transaction" in df.columns:
        st.subheader("International Transactions")
        st.bar_chart(
            df["International_Transaction"].astype(str).value_counts()
        )

# ============================================================
# TRANSACTIONS
# ============================================================

elif st.session_state.page == "Transactions":

    st.title("💳 Transaction Records")

    filtered = df.copy()

    if "Fraud_Flag" in df.columns:
        status = st.selectbox(
            "Filter Transactions",
            ["All", "Fraudulent", "Legitimate"]
        )

        if status == "Fraudulent":
            filtered = filtered[fraud_flag == 1]
        elif status == "Legitimate":
            filtered = filtered[fraud_flag == 0]

    if "Transaction_Type" in filtered.columns:
        transaction_types = sorted(
            filtered["Transaction_Type"].dropna().astype(str).unique()
        )

        selected_type = st.selectbox(
            "Transaction Type",
            ["All"] + transaction_types
        )

        if selected_type != "All":
            filtered = filtered[
                filtered["Transaction_Type"].astype(str) == selected_type
            ]

    st.write(f"Records found: {len(filtered):,}")
    st.dataframe(filtered, use_container_width=True)

    st.download_button(
        "⬇️ Download Filtered Transactions",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="Filtered_Fraud_Transactions.csv",
        mime="text/csv"
    )

# ============================================================
# FRAUD PREDICTION
# ============================================================

elif st.session_state.page == "Fraud Prediction":

    st.title("🔎 Fraud Prediction")
    st.warning(
        "This form provides a risk screening estimate only. "
        "It does not use a trained machine-learning model."
    )

    transaction_amount = st.number_input(
        "Transaction Amount",
        min_value=0.0,
        value=1000.0
    )

    ip_score = st.slider("IP Risk Score", 0, 100, 20)
    device_score = st.slider("Device Risk Score", 0, 100, 20)
    velocity_score = st.slider("Velocity Score", 0, 100, 20)

    location_mismatch = st.selectbox(
        "Location Mismatch",
        ["No", "Yes"]
    )

    international = st.selectbox(
        "International Transaction",
        ["No", "Yes"]
    )

    if st.button("Analyze Transaction", use_container_width=True):

        risk_score = (
            ip_score * 0.25
            + device_score * 0.25
            + velocity_score * 0.30
            + (15 if location_mismatch == "Yes" else 0)
            + (10 if international == "Yes" else 0)
        )

        st.metric("Screening Risk Score", f"{risk_score:.1f}/100")

        if risk_score >= 60:
            st.error("High-risk transaction. Further review recommended.")
        elif risk_score >= 35:
            st.warning("Medium-risk transaction. Review recommended.")
        else:
            st.success("Lower-risk transaction based on entered indicators.")

        st.caption(
            "This is a rule-based demonstration, not a trained ML prediction."
        )

# ============================================================
# MODEL PERFORMANCE
# ============================================================

elif st.session_state.page == "Model Performance":

    st.title("📋 Model Performance")

    st.info(
        "Actual model metrics are not calculated by this dashboard. "
        "Run your machine-learning training script and use its results "
        "to report accuracy, precision, recall, F1-score and ROC-AUC."
    )

    metrics = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"],
        "Meaning": [
            "Overall proportion of correct predictions",
            "Proportion of predicted fraud cases that were actually fraud",
            "Proportion of actual fraud cases detected",
            "Balance between precision and recall",
            "Ability to distinguish fraudulent from legitimate transactions"
        ]
    })

    st.dataframe(metrics, use_container_width=True)

    st.subheader("Dataset Overview")
    st.write(f"Total records: {total_transactions:,}")
    st.write(f"Fraudulent records: {fraud_transactions:,}")
    st.write(f"Legitimate records: {legitimate_transactions:,}")

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Fin-Care Starpowerz Digital Technology Pvt. Ltd. | "
    "Fraud Detection & Risk Management Analytics"
)