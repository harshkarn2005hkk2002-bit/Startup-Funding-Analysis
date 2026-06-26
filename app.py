import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os
from dotenv import load_dotenv
import requests
import io

# --- Load API key ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Page Config ---
st.set_page_config(page_title="Global Startup Explorer 2.0", page_icon="🚀", layout="wide")

# --- ADVANCED UI DESIGN ---
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #1e293b);
    color: #ffffff;
}

/* HEADINGS (FIXED VISIBILITY) */
h1, h2, h3, h4 {
    color: #f8fafc !important;
    text-shadow: 0 0 10px rgba(99,102,241,0.7);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #020617);
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* METRICS (NEON STYLE) */
.metric-box {
    background: linear-gradient(135deg, #6366f1, #06b6d4);
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    font-weight: bold;
    box-shadow: 0 0 20px rgba(99,102,241,0.6);
}

/* TABLE FIX */
[data-testid="stDataFrame"] {
    background: white !important;
    color: black !important;
    border-radius: 10px;
}

/* NORMAL TABLE */
table {
    background: white !important;
    color: black !important;
}

/* INPUT BOX */
input, textarea {
    background-color: #f8fafc !important;
    color: black !important;
    border-radius: 10px !important;
}

/* BUTTON */
.stDownloadButton button {
    background: linear-gradient(90deg,#22c55e,#06b6d4);
    color: white;
    border-radius: 10px;
    font-weight: bold;
}

/* CHATBOX */
.chat-box {
    background: linear-gradient(135deg, #e0f2fe, #f0fdf4);
    color: black;
    padding: 15px;
    border-radius: 12px;
}

/* SUCCESS BOX */
.stSuccess {
    background-color: #dcfce7 !important;
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

# --- Load Dataset ---
df = pd.read_csv("data/real_companies.csv")

# --- Clean Data ---
df['Funding Stage'] = df['Funding Stage'].fillna("Unknown")
df['Amount Raised (USD)'] = df['Amount Raised (USD)'].fillna(0)
df['Country'] = df['Country'].fillna("Unknown")
df['Industry'] = df['Industry'].fillna("Unknown")
df['Funding Date'] = pd.to_datetime(df['Funding Date'], errors='coerce')
df['Year'] = df['Funding Date'].dt.year.fillna(0).astype(int)
df['Number of Employees'] = df['Number of Employees'].fillna(0)

# --- Sidebar Filters ---
st.sidebar.header("🎛️ Filter Startups")

countries = ["All"] + sorted(df['Country'].unique())
industries = ["All"] + sorted(df['Industry'].unique())
stages = ["All"] + sorted(df['Funding Stage'].unique())
years = ["All"] + sorted(df['Year'].unique())

selected_country = st.sidebar.selectbox("Country", countries)
selected_industry = st.sidebar.selectbox("Industry", industries)
selected_stage = st.sidebar.selectbox("Funding Stage", stages)
selected_year = st.sidebar.selectbox("Year", years)

employee_range = st.sidebar.slider("Employees", 0, int(df['Number of Employees'].max()), (0, int(df['Number of Employees'].max())))
funding_range = st.sidebar.slider("Funding", 0, int(df['Amount Raised (USD)'].max()), (0, int(df['Amount Raised (USD)'].max())))

# --- Apply Filters ---
filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]
if selected_industry != "All":
    filtered_df = filtered_df[filtered_df['Industry'] == selected_industry]
if selected_stage != "All":
    filtered_df = filtered_df[filtered_df['Funding Stage'] == selected_stage]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]

filtered_df = filtered_df[
    (filtered_df['Number of Employees'] >= employee_range[0]) &
    (filtered_df['Number of Employees'] <= employee_range[1]) &
    (filtered_df['Amount Raised (USD)'] >= funding_range[0]) &
    (filtered_df['Amount Raised (USD)'] <= funding_range[1])
]

# --- TITLE ---
st.title("🚀 Global Startup Explorer 2.0")

# --- METRICS ---
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='metric-box'>Total Startups<br>{len(filtered_df)}</div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box'>Countries<br>{filtered_df['Country'].nunique()}</div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box'>Industries<br>{filtered_df['Industry'].nunique()}</div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-box'>Funding<br>${filtered_df['Amount Raised (USD)'].sum():,.0f}</div>", unsafe_allow_html=True)

# --- TABLE ---
st.subheader("📋 Startups Data")
st.dataframe(filtered_df)

# --- DOWNLOAD ---
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    filtered_df.to_excel(writer, index=False)

st.download_button("📥 Download Excel", output.getvalue(), "startup_report.xlsx")

# --- CHARTS ---
st.subheader("📊 Visualizations")
st.plotly_chart(px.pie(filtered_df, names='Country'), use_container_width=True)
st.plotly_chart(px.pie(filtered_df, names='Industry'), use_container_width=True)

yearly = filtered_df.groupby('Year')['Amount Raised (USD)'].sum().reset_index()
fig5 = px.line(yearly, x='Year', y='Amount Raised (USD)', title="Funding Over Years")
st.plotly_chart(fig5, use_container_width=True)

# --- CHATBOT ---
st.subheader("🤖 AI Startup Chatbot")

question = st.text_input("Ask anything about startups")

if question:
    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "Startup expert"},
                    {"role": "user", "content": question}
                ]
            }
        ).json()

        if "choices" in res:
            st.markdown(f"<div class='chat-box'>{res['choices'][0]['message']['content']}</div>", unsafe_allow_html=True)
        else:
            st.error("Chatbot error")

    except Exception as e:
        st.error(e)

# --- RECOMMENDATION ---
st.subheader("💡 Recommendations")

selected = st.selectbox("Select Startup", filtered_df['Startup Name'].unique())

if selected:
    df_copy = filtered_df.copy()
    df_copy['Country_enc'] = LabelEncoder().fit_transform(df_copy['Country'])
    df_copy['Industry_enc'] = LabelEncoder().fit_transform(df_copy['Industry'])

    sim = cosine_similarity(df_copy[['Country_enc','Industry_enc','Number of Employees']])
    idx = df_copy[df_copy['Startup Name'] == selected].index[0]

    scores = sorted(list(enumerate(sim[idx])), key=lambda x: x[1], reverse=True)[1:6]
    rec = df_copy.iloc[[i[0] for i in scores]]

    st.table(rec[['Startup Name','Country','Industry','Funding Stage','Amount Raised (USD)']])

# --- PREDICTION ---
st.subheader("🔮 Future Investment Prediction")

try:
    from prediction_engine import StartupPredictor

    predictor = StartupPredictor(filtered_df)
    predictor.preprocess()
    predictor.train_models()

    name = st.selectbox("Select Startup", filtered_df['Startup Name'].unique(), key="pred")

    row = filtered_df[filtered_df['Startup Name'] == name].iloc[0]

    pred = predictor.predict_next({
        "Country": row['Country'],
        "Industry": row['Industry'],
        "Funding Stage": row['Funding Stage'],
        "Number of Employees": row['Number of Employees'],
        "Funding Year": row['Year']
    })

    st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #22c55e, #4ade80);
    color: black;
    padding: 20px;
    border-radius: 12px;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    box-shadow: 0 0 15px rgba(34,197,94,0.6);
">
💰 Predicted Investment: ${pred:,.2f}
</div>
""", unsafe_allow_html=True)
except Exception as e:
    st.warning(e)