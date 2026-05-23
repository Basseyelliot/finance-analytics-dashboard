import streamlit as st
import pandas as pd
import plotly.express as px

from analysis import run_monte_carlo, run_prophet_forecast

st.set_page_config(
    page_title="Finance Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.hero {
    background: linear-gradient(135deg, #12355b, #1f7a8c);
    padding: 45px;
    border-radius: 22px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}
.hero h1 {
    font-size: 48px;
    font-weight: 800;
}
.hero p {
    font-size: 20px;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
.section-title {
    color: #12355b;
    font-size: 30px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📌 Dashboard Menu")

page = st.sidebar.radio(
    "Select a section",
    [
        "🏠 Home",
        "📊 Financial Statements Analysis",
        "💰 CAPM & Cost of Equity",
        "📈 Prophet Forecast",
        "🎲 Monte Carlo Simulation",
        "📘 Methodology",
        "📌 Conclusion",
        "📁 Download Files"
    ]
)

st.markdown("""
<div class="hero">
    <h1>📊 Finance Analytics Dashboard</h1>
    <p>Financial Ratio Analysis • CAPM • Prophet Forecasting • Monte Carlo Simulation</p>
</div>
""", unsafe_allow_html=True)

if page == "🏠 Home":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("""
    ## 📌 Executive Summary

    This finance analytics dashboard analyzes company financial performance,
    stock forecasting using Facebook Prophet,
    and risk assessment using Monte Carlo Simulation.
    """)

    st.markdown('</div>', unsafe_allow_html=True)

    # Read data from Excel
    df_raw = pd.read_excel("data/financial_statements_Analysis.xlsx")

    df_raw = df_raw.loc[:, ~df_raw.columns.str.contains("^Unnamed")]

    df = df_raw.iloc[:, 0:5]

    df.columns = [
        "Financial Item",
        "2025",
        "2024",
        "2023",
        "2022"
    ]

    df = df.dropna(how="all")
    df = df.fillna("")
    df = df.reset_index(drop=True)

    # KPI values
    revenue_2025 = float(df.loc[df["Financial Item"] == "Total Revenue", "2025"].values[0])

    revenue_2024 = float(df.loc[df["Financial Item"] == "Total Revenue", "2024"].values[0])

    gross_profit_2025 = float(df.loc[df["Financial Item"] == "Gross Profit", "2025"].values[0])

    operating_expense_2025 = float(df.loc[df["Financial Item"] == "Operating Expense", "2025"].values[0])

    revenue_growth = ((revenue_2025 - revenue_2024) / revenue_2024) * 100

    gross_margin = (gross_profit_2025 / revenue_2025) * 100

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Revenue 2025",
        f"${revenue_2025:,.0f}",
        f"{revenue_growth:.2f}%"
    )

    col2.metric(
        "📈 Gross Profit",
        f"${gross_profit_2025:,.0f}"
    )

    col3.metric(
        "📊 Gross Margin",
        f"{gross_margin:.2f}%"
    )

    col4.metric(
        "💸 Operating Expense",
        f"${operating_expense_2025:,.0f}"
    )

    st.write("")

    # Revenue trend chart
    chart_df = df.melt(
        id_vars="Financial Item",
        var_name="Year",
        value_name="Amount"
    )

    trend_df = chart_df[
        chart_df["Financial Item"].isin([
            "Total Revenue",
            "Gross Profit",
            "Operating Expense"
        ])
    ]

    fig = px.line(
        trend_df,
        x="Year",
        y="Amount",
        color="Financial Item",
        markers=True,
        title="📈 Financial Performance Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### 🔍 Key Insights

    - Revenue increased from 2024 to 2025.
    - Gross profit remains strong, indicating healthy operations.
    - Operating expenses should continue to be monitored carefully.
    - Prophet forecasting and Monte Carlo simulation provide future financial outlook and risk analysis.

    ### ✅ Recommendation

    The company should continue improving operational efficiency
    while leveraging predictive analytics for future financial planning.
    """)

elif page == "📊 Financial Statements Analysis":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Financial Statements Analysis</div>', unsafe_allow_html=True)

    df = pd.read_excel("data/financial_statements_Analysis.xlsx")
    # Keep only the important columns
    df = df.iloc[:, 0:5]
    # Rename columns professionally
    df.columns = [
        "Financial Item",
        "2025",
        "2024",
        "2023",
        "2022"
]
    # Remove empty rows
    df = df.dropna(how="all")
    # Replace missing values
    df = df.fillna("")
    # Reset index
    df = df.reset_index(drop=True)
    # KPI values directly from Excel
    revenue_2025 = df.loc[df["Financial Item"] == "Total Revenue", "2025"].values[0]
    revenue_2024 = df.loc[df["Financial Item"] == "Total Revenue", "2024"].values[0]
    gross_profit_2025 = df.loc[df["Financial Item"] == "Gross Profit", "2025"].values[0]
    operating_expense_2025 = df.loc[df["Financial Item"] == "Operating Expense", "2025"].values[0]
    
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="📥 Download Financial Statements Excel",
        data=open("data/financial_statements_Analysis.xlsx", "rb"),
        file_name="financial_statements_Analysis.xlsx"
    )

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "💰 CAPM & Cost of Equity":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💰 CAPM & Cost of Equity Analysis</div>', unsafe_allow_html=True)

    df = pd.read_excel("data/CAPM&_Cost_of_Equity_Analysis.xlsx")
    # Remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Remove completely empty rows
    df = df.dropna(how="all")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="📥 Download CAPM Excel",
        data=open("data/CAPM&_Cost_of_Equity_Analysis.xlsx", "rb"),
        file_name="CAPM&_Cost_of_Equity_Analysis.xlsx"
    )

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "📈 Prophet Forecast":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Facebook Prophet Forecast</div>', unsafe_allow_html=True)

    with st.spinner("Running Prophet forecast..."):
        forecast_table, fig1, fig2 = run_prophet_forecast()
    st.subheader("Forecast Chart")
    st.pyplot(fig1)

    st.subheader("Forecast Components")
    st.pyplot(fig2)

    st.subheader("Latest Forecast Values")
    st.dataframe(forecast_table, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "🎲 Monte Carlo Simulation":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎲 Monte Carlo Simulation</div>', unsafe_allow_html=True)

    with st.spinner("Running Monte Carlo simulation..."):
        summary, fig1, fig2 = run_monte_carlo()

    col1, col2, col3 = st.columns(3)
    col1.metric("Mean Forecast Price", summary["Mean Forecast Price"])
    col2.metric("Minimum Forecast Price", summary["Minimum Forecast Price"])
    col3.metric("Maximum Forecast Price", summary["Maximum Forecast Price"])

    st.subheader("30-Day Simulation Paths")
    st.pyplot(fig1)

    st.subheader("Distribution of Final Prices")
    st.pyplot(fig2)

    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Simulation Chart")
    st.pyplot(fig1)

    st.subheader("Distribution of Final Prices")
    st.pyplot(fig2)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "📁 Download Files":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📁 Download Project Files</div>', unsafe_allow_html=True)

    st.download_button(
        label="📥 Download Financial Statements Excel",
        data=open("data/financial_statements_Analysis.xlsx", "rb"),
        file_name="financial_statements_Analysis.xlsx"
    )

    st.download_button(
        label="📥 Download CAPM & Cost of Equity Excel",
        data=open("data/CAPM&_Cost_of_Equity_Analysis.xlsx", "rb"),
        file_name="CAPM&_Cost_of_Equity_Analysis.xlsx"
    )

    with open("files/finance_presentation.pptx", "rb") as file:
        st.download_button(
            label="📥 Download PowerPoint Presentation",
            data=file,
            file_name="finance_presentation.pptx"
        )

    st.markdown('</div>', unsafe_allow_html=True)
elif page == "📘 Methodology":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">📘 Project Methodology</div>', unsafe_allow_html=True)

    st.write("""

    ### Project Objective

    This project focuses on the financial analysis of The Coca-Cola Company (KO)
    using financial statement analysis, forecasting techniques,
    and risk simulation models to evaluate business performance and future investment potential.

    ### Methodology Used

    #### 1. Financial Statement Analysis
    - Analyzed Coca-Cola's revenue, gross profit, operating expenses,
      and overall financial performance across multiple years.
    - Evaluated trends in profitability and operational efficiency.

    #### 2. CAPM & Cost of Equity Analysis
    - Applied the Capital Asset Pricing Model (CAPM)
      to estimate Coca-Cola’s expected return and cost of equity.
    - Evaluated investment risk using beta, market return,
      and risk-free rate assumptions.

    #### 3. Facebook Prophet Forecasting
    - Used Facebook Prophet time series forecasting model
      to predict future Coca-Cola stock prices.
    - Visualized long-term stock trends and forecast confidence intervals.

    #### 4. Monte Carlo Simulation
    - Performed Monte Carlo simulation
      to model possible future stock price scenarios.
    - Evaluated uncertainty, volatility,
      and potential investment risk.

    ### Data Sources

    - Coca-Cola historical financial statement data
    - Historical stock market data from Yahoo Finance

    ### Tools & Technologies

    - Python
    - Streamlit
    - Pandas
    - Plotly
    - Facebook Prophet
    - Matplotlib
    - NumPy
    - Yahoo Finance API

    """)

    st.markdown('</div>', unsafe_allow_html=True)
elif page == "📌 Conclusion":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">📌 Project Conclusion</div>', unsafe_allow_html=True)

    st.write("""

    ### Final Conclusion

    This finance analytics project successfully combined financial analysis,
    predictive forecasting,
    and risk simulation techniques into an interactive dashboard.

    Key findings include:

    - Revenue growth remained positive over the analyzed period.
    - Prophet forecasting indicated potential future stock price growth.
    - Monte Carlo simulation demonstrated possible future risk scenarios.
    - CAPM analysis provided insight into expected investment returns.

    ### Business Recommendation

    Organizations should combine financial statement analysis,
    predictive analytics,
    and risk simulation models to improve strategic decision-making.

    ### Future Improvements

    Future versions of this project may include:

    - Real-time stock market APIs
    - Power BI integration
    - Machine learning models
    - Advanced portfolio optimization

    """)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    ---
    <center>
    Finance Analytics Dashboard  
    Group Project Deployment & Dashboard Development by Bassey Elliot  
    Powered by Python • Streamlit • Prophet • Monte Carlo Simulation
    </center>
    """, unsafe_allow_html=True)
