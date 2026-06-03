import pandas as pd
import numpy as np
import hashlib
from faker import Faker
from datetime import timedelta
import random
import os

fake = Faker()
np.random.seed(42)
random.seed(42)

os.makedirs("data/raw", exist_ok=True)

departments = ["Engineering", "Product", "Sales", "Marketing", "Finance", "People", "Operations", "Support"]
job_levels = ["L1", "L2", "L3", "L4", "L5", "L6"]
locations = ["Toronto", "Ottawa", "Remote Canada", "New York", "London", "Dublin"]
job_families = ["Data", "Software", "Product", "Operations", "Finance", "Recruiting", "Customer Success"]
salary_bands = ["Band A", "Band B", "Band C", "Band D", "Band E"]

def hash_id(value):
    return hashlib.sha256(str(value).encode()).hexdigest()

def generate_employees(n=20000):
    employees = []

    for i in range(1, n + 1):
        hire_date = fake.date_between(start_date="-6y", end_date="today")
        terminated = np.random.choice([0, 1], p=[0.82, 0.18])

        termination_date = None
        employment_status = "Active"

        if terminated:
            termination_date = fake.date_between(start_date=hire_date, end_date="today")
            employment_status = "Terminated"

        employees.append({
            "employee_id": i,
            "hashed_employee_id": hash_id(i),
            "department": np.random.choice(departments),
            "job_level": np.random.choice(job_levels, p=[0.22, 0.24, 0.22, 0.16, 0.10, 0.06]),
            "job_family": np.random.choice(job_families),
            "location": np.random.choice(locations),
            "hire_date": hire_date,
            "termination_date": termination_date,
            "employment_status": employment_status,
            "manager_id": np.random.randint(1, 900),
            "salary_band": np.random.choice(salary_bands),
            "performance_rating": np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.12, 0.48, 0.25, 0.10]),
            "engagement_score": round(np.random.normal(7.2, 1.4), 1),
            "promotion_count": np.random.choice([0, 1, 2, 3], p=[0.55, 0.30, 0.12, 0.03]),
            "last_promotion_date": fake.date_between(start_date=hire_date, end_date="today") if np.random.rand() > 0.5 else None
        })

    df = pd.DataFrame(employees)
    df["engagement_score"] = df["engagement_score"].clip(1, 10)
    df.to_csv("data/raw/employees.csv", index=False)

def generate_recruiting_funnel(n=8000):
    records = []

    for i in range(1, n + 1):
        application_date = fake.date_between(start_date="-2y", end_date="today")

        candidate_status = np.random.choice(
            ["Applied", "Screened", "Interviewed", "Offered", "Hired", "Rejected"],
            p=[0.20, 0.18, 0.22, 0.08, 0.12, 0.20]
        )

        recruiter_screen_date = None
        interview_date = None
        offer_date = None
        hire_date = None

        if candidate_status in ["Screened", "Interviewed", "Offered", "Hired", "Rejected"]:
            recruiter_screen_date = application_date + timedelta(days=np.random.randint(1, 8))

        if candidate_status in ["Interviewed", "Offered", "Hired", "Rejected"]:
            interview_date = application_date + timedelta(days=np.random.randint(7, 25))

        if candidate_status in ["Offered", "Hired"]:
            offer_date = application_date + timedelta(days=np.random.randint(20, 45))

        if candidate_status == "Hired":
            hire_date = application_date + timedelta(days=np.random.randint(30, 70))

        records.append({
            "candidate_id": i,
            "role_id": np.random.randint(1000, 1200),
            "department": np.random.choice(departments),
            "application_date": application_date,
            "recruiter_screen_date": recruiter_screen_date,
            "interview_date": interview_date,
            "offer_date": offer_date,
            "hire_date": hire_date,
            "candidate_status": candidate_status,
            "source_channel": np.random.choice(["LinkedIn", "Referral", "Company Website", "Recruiter", "Campus"]),
            "time_to_fill_days": (hire_date - application_date).days if hire_date else None
        })

    pd.DataFrame(records).to_csv("data/raw/recruiting_funnel.csv", index=False)

def generate_headcount_plan():
    months = pd.date_range(start="2023-01-01", end="2026-12-01", freq="MS")
    records = []

    for month in months:
        for dept in departments:
            records.append({
                "month": month.date(),
                "department": dept,
                "planned_headcount": np.random.randint(120, 900),
                "approved_hiring_budget": np.random.randint(500000, 5000000),
                "priority_level": np.random.choice(["Low", "Medium", "High"])
            })

    pd.DataFrame(records).to_csv("data/raw/headcount_plan.csv", index=False)

def generate_compensation(n=20000):
    records = []

    for i in range(1, n + 1):
        salary = np.random.randint(55000, 210000)

        records.append({
            "employee_id": i,
            "base_salary": salary,
            "bonus": round(salary * np.random.uniform(0.03, 0.20), 2),
            "salary_band": np.random.choice(salary_bands),
            "compa_ratio": round(np.random.uniform(0.75, 1.25), 2),
            "last_comp_review_date": fake.date_between(start_date="-2y", end_date="today")
        })

    pd.DataFrame(records).to_csv("data/raw/compensation.csv", index=False)

def generate_performance_reviews(n=20000):
    cycles = ["2024-H1", "2024-H2", "2025-H1", "2025-H2"]
    records = []

    for i in range(1, n + 1):
        for cycle in cycles:
            records.append({
                "employee_id": i,
                "review_cycle": cycle,
                "performance_rating": np.random.choice([1, 2, 3, 4, 5], p=[0.04, 0.10, 0.50, 0.26, 0.10]),
                "potential_rating": np.random.choice(["Low", "Medium", "High"], p=[0.15, 0.65, 0.20]),
                "review_submitted_date": fake.date_between(start_date="-2y", end_date="today"),
                "promotion_recommendation": np.random.choice(["Yes", "No"], p=[0.18, 0.82])
            })

    pd.DataFrame(records).to_csv("data/raw/performance_reviews.csv", index=False)

if __name__ == "__main__":
    generate_employees()
    generate_recruiting_funnel()
    generate_headcount_plan()
    generate_compensation()
    generate_performance_reviews()

    print("All synthetic workforce datasets generated successfully.")
    