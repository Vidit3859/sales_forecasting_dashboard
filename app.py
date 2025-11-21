import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Forecast Dashboard", layout="wide")

# Load Data
weekly_sales = pd.read_csv("weekly_sales.csv", parse_dates=["Date"], index_col="Date")
forecast = pd.read_csv("forecast.csv", parse_dates=["Unnamed: 0"])
forecast.rename(columns={"Unnamed: 0": "Date", "predicted_mean": "Forecast"}, inplace=True)
forecast.set_index("Date", inplace=True)

st.title("📊 Walmart Weekly Sales Forecasting Dashboard")

# =========================
# SECTION 1 — RAW DATA
# =========================
st.header("1️⃣ Weekly Sales Data")
st.dataframe(weekly_sales.tail(10))

# =========================
# SECTION 2 — HISTORICAL SALES PLOT
# =========================
st.header("2️⃣ Historical Weekly Sales Trend")

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(weekly_sales.index, weekly_sales["Weekly_Sales"], label="Weekly Sales")
ax.set_title("Weekly Sales Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Sales")
ax.grid()
ax.legend()
st.pyplot(fig)

# =========================
# SECTION 3 — ROLLING AVERAGE
# =========================
st.header("3️⃣ Rolling 12-Week Average")

weekly_sales['Rolling_Avg'] = weekly_sales['Weekly_Sales'].rolling(12).mean()

fig2, ax2 = plt.subplots(figsize=(14, 6))
ax2.plot(weekly_sales.index, weekly_sales["Weekly_Sales"], label="Weekly Sales")
ax2.plot(weekly_sales.index, weekly_sales["Rolling_Avg"], label="Rolling 12-Week Average", linewidth=3)
ax2.set_title("Rolling Average Trend")
ax2.set_xlabel("Date")
ax2.set_ylabel("Sales")
ax2.grid()
ax2.legend()
st.pyplot(fig2)

# =========================
# SECTION 4 — FORECAST PLOT
# =========================
st.header("4️⃣ SARIMA Forecast")

fig3, ax3 = plt.subplots(figsize=(14, 6))
ax3.plot(weekly_sales.index, weekly_sales["Weekly_Sales"], label="Actual")
ax3.plot(forecast.index, forecast["Forecast"], label="Forecast", color="orange", linewidth=3)
ax3.set_title("SARIMA Forecast of Weekly Sales")
ax3.set_xlabel("Date")
ax3.set_ylabel("Sales")
ax3.grid()
ax3.legend()
st.pyplot(fig3)

# =========================
# SECTION 5 — FORECAST TABLE
# =========================
st.header("5️⃣ Forecasted Values (Next 12 Weeks)")
st.dataframe(forecast)

# Download button
csv = forecast.to_csv().encode("utf-8")
st.download_button(
    label="📥 Download Forecast as CSV",
    data=csv,
    file_name="forecast_output.csv",
    mime="text/csv",
)