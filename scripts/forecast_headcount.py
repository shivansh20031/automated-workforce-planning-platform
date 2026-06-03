import pandas as pd
import numpy as np
import os
from datetime import datetime

os.makedirs("data/processed", exist_ok=True)

employees = pd.read_csv("data/raw/employees.csv")
headcount_plan = pd.read_csv("data/raw/headcount_plan.csv")

employees["hire_date"] = pd.to_datetime(employees["hire_date"])
employees["termination_date"] = pd.to_datetime(employees["termination_date"], errors="coerce")
headcount_plan["month"] = pd.to_datetime(headcount_plan["month"])

forecast_records = []

departments = employees["department"].unique()

for department in departments:
    dept_employees = employees[employees["department"] == department]

    monthly_hires = (
        dept_employees
        .groupby(pd.Grouper(key="hire_date", freq="MS"))
        .size()
        .reset_index(name="hires")
        .rename(columns={"hire_date": "month"})
    )

    monthly_terms = (
        dept_employees.dropna(subset=["termination_date"])
        .groupby(pd.Grouper(key="termination_date", freq="MS"))
        .size()
        .reset_index(name="terminations")
        .rename(columns={"termination_date": "month"})
    )

    monthly = monthly_hires.merge(monthly_terms, on="month", how="outer").fillna(0)
    monthly = monthly.sort_values("month")

    monthly["net_change"] = monthly["hires"] - monthly["terminations"]
    monthly["actual_headcount"] = monthly["net_change"].cumsum()

    if len(monthly) < 6:
        continue

    recent_growth = monthly["net_change"].tail(6).mean()
    last_headcount = monthly["actual_headcount"].iloc[-1]
    last_month = monthly["month"].max()

    for i in range(1, 7):
        forecast_month = last_month + pd.DateOffset(months=i)
        forecast_headcount = max(0, round(last_headcount + recent_growth * i))

        plan_match = headcount_plan[
            (headcount_plan["department"] == department) &
            (headcount_plan["month"] == forecast_month)
        ]

        planned_headcount = None
        gap_to_plan = None

        if not plan_match.empty:
            planned_headcount = int(plan_match.iloc[0]["planned_headcount"])
            gap_to_plan = forecast_headcount - planned_headcount

        forecast_records.append({
            "department": department,
            "forecast_month": forecast_month.date(),
            "forecasted_headcount": forecast_headcount,
            "planned_headcount": planned_headcount,
            "gap_to_plan": gap_to_plan,
            "recent_avg_monthly_net_growth": round(recent_growth, 2)
        })

forecast_df = pd.DataFrame(forecast_records)

forecast_df.to_csv("data/processed/headcount_forecast.csv", index=False)

print("Headcount forecast created successfully.")
print(forecast_df.head())
