import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Workforce Planning Platform",
    layout="wide"
)

st.title("Automated Workforce Planning & Headcount Forecasting Platform")
st.write("Internal workforce analytics tool for headcount, attrition, recruiting, and compensation decision support.")

executive_summary = pd.read_csv("data/processed/executive_workforce_summary.csv")
headcount = pd.read_csv("data/processed/headcount_by_department.csv")
attrition = pd.read_csv("data/processed/attrition_summary.csv")
recruiting = pd.read_csv("data/processed/recruiting_summary.csv")
compensation = pd.read_csv("data/processed/compensation_summary.csv")
forecast = pd.read_csv("data/processed/headcount_forecast.csv")
st.sidebar.header("Filters")

departments = executive_summary["department"].unique()
selected_departments = st.sidebar.multiselect(
    "Select Department(s)",
    departments,
    default=list(departments)
)

filtered_summary = executive_summary[
    executive_summary["department"].isin(selected_departments)
]

filtered_headcount = headcount[
    headcount["department"].isin(selected_departments)
]

filtered_attrition = attrition[
    attrition["department"].isin(selected_departments)
]

filtered_recruiting = recruiting[
    recruiting["department"].isin(selected_departments)
]

filtered_compensation = compensation[
    compensation["department"].isin(selected_departments)
]
filtered_forecast = forecast[
    forecast["department"].isin(selected_departments)
]
total_headcount = int(filtered_summary["current_headcount"].sum())
avg_attrition = round(filtered_summary["attrition_rate"].mean() * 100, 1)
avg_salary = round(filtered_summary["avg_base_salary"].mean(), 2)
avg_compa_ratio = round(filtered_summary["avg_compa_ratio"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Current Headcount", total_headcount)
col2.metric("Avg Attrition Rate", f"{avg_attrition}%")
col3.metric("Avg Base Salary", f"${avg_salary:,.0f}")
col4.metric("Avg Compa Ratio", avg_compa_ratio)
st.divider()

st.subheader("Workforce Risk Alerts")

risk_col1, risk_col2, risk_col3 = st.columns(3)

high_attrition_departments = filtered_summary[
    filtered_summary["attrition_rate"] >= 0.185
]

low_compa_departments = filtered_summary[
    filtered_summary["avg_compa_ratio"] < 1.0
]

forecast_gap_departments = filtered_forecast[
    filtered_forecast["gap_to_plan"] < 0
] if "gap_to_plan" in filtered_forecast.columns else pd.DataFrame()

risk_col1.metric(
    "High Attrition Departments",
    len(high_attrition_departments)
)

risk_col2.metric(
    "Below Market Comp Ratio",
    len(low_compa_departments)
)

risk_col3.metric(
    "Projected Headcount Gaps",
    len(forecast_gap_departments)
)

if len(high_attrition_departments) > 0:
    st.warning(
        "Attrition risk detected in: "
        + ", ".join(high_attrition_departments["department"].tolist())
    )

if len(low_compa_departments) > 0:
    st.warning(
        "Compensation review recommended for: "
        + ", ".join(low_compa_departments["department"].tolist())
    )

if len(forecast_gap_departments) > 0:
    st.warning(
        "Forecasted headcount is below plan for selected departments/months."
    )
st.subheader("6-Month Headcount Forecast")

fig_forecast = px.line(
    filtered_forecast,
    x="forecast_month",
    y="forecasted_headcount",
    color="department",
    markers=True,
    title="Forecasted Headcount by Department"
)

st.plotly_chart(fig_forecast, use_container_width=True)

st.subheader("Headcount Gap to Plan")

gap_data = filtered_forecast.dropna(subset=["gap_to_plan"])

if not gap_data.empty:
    fig_gap = px.bar(
        gap_data,
        x="department",
        y="gap_to_plan",
        color="forecast_month",
        title="Forecasted Headcount Gap vs Plan"
    )
    st.plotly_chart(fig_gap, use_container_width=True)

    biggest_gap = gap_data.sort_values("gap_to_plan").head(1)

    st.warning(
        f"Biggest projected headcount gap is in {biggest_gap.iloc[0]['department']} "
        f"for {biggest_gap.iloc[0]['forecast_month']}, with a gap of "
        f"{int(biggest_gap.iloc[0]['gap_to_plan'])} employees versus plan."
    )
else:
    st.info("No planned headcount comparison available for the selected forecast period.")
st.divider()

st.subheader("Executive Workforce Summary")
st.dataframe(filtered_summary, use_container_width=True)

st.subheader("Current Headcount by Department")
fig_headcount = px.bar(
    filtered_headcount,
    x="department",
    y="current_headcount",
    title="Active Employee Headcount by Department"
)
st.plotly_chart(fig_headcount, use_container_width=True)

st.subheader("Attrition Rate by Department")
fig_attrition = px.bar(
    filtered_attrition,
    x="department",
    y="attrition_rate",
    title="Attrition Rate by Department"
)
st.plotly_chart(fig_attrition, use_container_width=True)

st.subheader("Recruiting Funnel")
fig_recruiting = px.bar(
    filtered_recruiting,
    x="department",
    y="candidate_count",
    color="candidate_status",
    title="Recruiting Funnel by Department"
)
st.plotly_chart(fig_recruiting, use_container_width=True)

st.subheader("Compensation Overview")
fig_compensation = px.scatter(
    filtered_compensation,
    x="avg_base_salary",
    y="avg_compa_ratio",
    size="avg_base_salary",
    hover_name="department",
    title="Average Salary vs Compa Ratio by Department"
)
st.plotly_chart(fig_compensation, use_container_width=True)

st.divider()

st.subheader("Leadership Insights")

highest_attrition = filtered_summary.sort_values("attrition_rate", ascending=False).head(1)
lowest_compa = filtered_summary.sort_values("avg_compa_ratio", ascending=True).head(1)
largest_team = filtered_summary.sort_values("current_headcount", ascending=False).head(1)

if not highest_attrition.empty:
    st.write(
        f"Highest attrition risk is in **{highest_attrition.iloc[0]['department']}** "
        f"with an attrition rate of **{round(highest_attrition.iloc[0]['attrition_rate'] * 100, 1)}%**."
    )

if not lowest_compa.empty:
    st.write(
        f"Lowest average compa ratio is in **{lowest_compa.iloc[0]['department']}**, "
        f"suggesting potential compensation review priority."
    )

if not largest_team.empty:
    st.write(
        f"Largest current team is **{largest_team.iloc[0]['department']}** "
        f"with **{int(largest_team.iloc[0]['current_headcount'])} active employees**."
    )

st.caption("Note: All employee-level data is synthetic. Employee identifiers are hashed for privacy-safe analysis.")
