import pandas as pd
import os

employees = pd.read_csv("data/raw/employees.csv")
recruiting = pd.read_csv("data/raw/recruiting_funnel.csv")
headcount_plan = pd.read_csv("data/raw/headcount_plan.csv")
compensation = pd.read_csv("data/raw/compensation.csv")
performance = pd.read_csv("data/raw/performance_reviews.csv")

os.makedirs("data/processed", exist_ok=True)

# 1. Current headcount by department
active_employees = employees[employees["employment_status"] == "Active"]

headcount_by_department = (
    active_employees
    .groupby("department")
    .agg(current_headcount=("employee_id", "count"))
    .reset_index()
)

# 2. Attrition by department
total_by_department = (
    employees
    .groupby("department")
    .agg(total_employees=("employee_id", "count"))
    .reset_index()
)

terminated_by_department = (
    employees[employees["employment_status"] == "Terminated"]
    .groupby("department")
    .agg(terminated_employees=("employee_id", "count"))
    .reset_index()
)

attrition_summary = total_by_department.merge(
    terminated_by_department,
    on="department",
    how="left"
)

attrition_summary["terminated_employees"] = attrition_summary["terminated_employees"].fillna(0)
attrition_summary["attrition_rate"] = (
    attrition_summary["terminated_employees"] / attrition_summary["total_employees"]
).round(3)

# 3. Recruiting funnel summary
recruiting_summary = (
    recruiting
    .groupby(["department", "candidate_status"])
    .agg(candidate_count=("candidate_id", "count"))
    .reset_index()
)

# 4. Compensation summary
compensation_joined = employees.merge(compensation, on=["employee_id", "salary_band"], how="left")

compensation_summary = (
    compensation_joined
    .groupby("department")
    .agg(
        avg_base_salary=("base_salary", "mean"),
        avg_compa_ratio=("compa_ratio", "mean")
    )
    .reset_index()
)

compensation_summary["avg_base_salary"] = compensation_summary["avg_base_salary"].round(2)
compensation_summary["avg_compa_ratio"] = compensation_summary["avg_compa_ratio"].round(2)

# 5. Executive workforce summary
executive_summary = (
    headcount_by_department
    .merge(attrition_summary[["department", "attrition_rate"]], on="department", how="left")
    .merge(compensation_summary, on="department", how="left")
)

executive_summary.to_csv("data/processed/executive_workforce_summary.csv", index=False)
headcount_by_department.to_csv("data/processed/headcount_by_department.csv", index=False)
attrition_summary.to_csv("data/processed/attrition_summary.csv", index=False)
recruiting_summary.to_csv("data/processed/recruiting_summary.csv", index=False)
compensation_summary.to_csv("data/processed/compensation_summary.csv", index=False)

print("Workforce analysis files created successfully.")
print(executive_summary)

