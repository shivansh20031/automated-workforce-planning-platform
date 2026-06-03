# Data Governance & Privacy Controls

This project uses synthetic workforce data, but it is designed to follow privacy-safe principles for sensitive people analytics workflows.

## Sensitive Data Areas

The platform handles simulated data related to:

- Employee records
- Compensation bands
- Performance ratings
- Engagement scores
- Recruiting funnel activity
- Headcount planning

## Privacy Controls Used

### 1. Hashed Employee Identifiers

Raw employee IDs are converted into hashed identifiers using SHA-256 before analysis.

This allows workforce trends to be analyzed without exposing direct employee identifiers.

### 2. Aggregated Reporting

The dashboard focuses on department-level trends instead of individual-level employee records.

Examples:

- Headcount by department
- Attrition rate by department
- Average compensation ratio by department
- Forecasted headcount by department

### 3. Compensation Masking

The dashboard avoids showing individual salary records. Compensation data is summarized using average base salary and average compa ratio by department.

### 4. Data Quality Checks

The project includes validation logic for:

- Missing employee IDs
- Duplicate records
- Invalid employment status values
- Null department fields
- Missing compensation records
- Forecast gaps versus headcount plan

### 5. Responsible Decision Support

The platform is designed to support leadership decisions, not replace human judgement.

Forecasts and alerts should be interpreted as directional signals, not final decisions.
