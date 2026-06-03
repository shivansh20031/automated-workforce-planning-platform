# Automated Workforce Planning & Headcount Forecasting Platform

End-to-end workforce analytics platform built to support headcount planning, attrition monitoring, recruiting funnel analysis, compensation review, and privacy-safe people data decision support.

This project simulates an internal analytics product used by leadership teams to understand workforce trends, identify talent risks, and make planning decisions using synthetic HR and recruiting data.

Project Overview

Most workforce dashboards stop at static reporting. This project turns simulated workforce data into a self-service internal tool with automated data generation, processed analytics layers, headcount forecasting, risk alerts, and leadership-ready insights.

The platform answers questions such as:

- Which departments have the highest attrition risk?
- Where are headcount gaps likely to appear?
- Which teams may need compensation review?
- How is recruiting activity distributed across departments?
- What does the next 6 months of workforce growth look like?

Tech Stack

- Python
- Pandas / NumPy
- Streamlit
- Plotly
- SQL
- GitHub
- Data Governance Documentation

Key Features

1. Synthetic Workforce Data Layer

Generated synthetic HR and recruiting datasets covering:

- Employee records
- Compensation data
- Performance reviews
- Recruiting funnel activity
- Headcount planning data

2. Processed Analytics Layer

Built processed datasets for:

- Department-level headcount
- Attrition rate
- Compensation summary
- Recruiting funnel summary
- Executive workforce summary

3. Headcount Forecasting

Created a 6-month department-level headcount forecast using historical hiring and termination patterns.

The forecast helps identify expected workforce growth and potential gaps against headcount planning targets.

4. Internal Streamlit Dashboard

Built an interactive dashboard with:

- Executive KPI cards
- Department filters
- Headcount by department
- Attrition by department
- Compensation overview
- Recruiting funnel analysis
- 6-month headcount forecast
- Workforce risk alerts
- Leadership insights

5. Workforce Risk Alerts

Added automated alerts for:

- High attrition departments
- Departments below compensation benchmark
- Projected headcount gaps

 6. Data Governance & Privacy Controls

Included privacy-safe design principles such as:

- Hashed employee identifiers
- Department-level aggregation
- No individual salary display
- Synthetic employee data
- Data quality checks
- Responsible decision-support framing

Project Structure
automated-workforce-planning-platform/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   └── data_governance.md
│
├── scripts/
│   ├── generate_synthetic_data.py
│   ├── workforce_analysis.py
│   └── forecast_headcount.py
│
├── sql/
│   └── data_quality_checks.sql
│
├── streamlit_app/
│   └── app.py
│
├── README.md
├── requirements.txt
└── .gitignore
