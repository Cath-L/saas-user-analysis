# 02 – Build Monthly Summary

## Overview
This step takes the six raw data tables generated in Step 01 and merges them into a unified, analysis-ready dataset called `monthly_site_summary.csv`.

The final dataset includes:
- Monthly user activity per site
- Total storage used (in GB)
- Total background job minutes
- License type breakdown per site
- Customer metadata (region, industry, tier)

This unified summary supports executive dashboards, onboarding cohort tracking, and GPT-powered segment summaries.

---

## Input Files
These six CSVs are expected as inputs (from `01-generate/`):

- `saas_customer_info.csv`  
- `saas_sites.csv`  
- `saas_storage.csv`  
- `saas_users.csv`  
- `saas_user_activity.csv`  
- `saas_background_jobs.csv`

---

## Steps Performed

### 📅 1. Convert to Monthly Format
- All date columns are parsed to datetime
- `month` column is extracted using `.dt.to_period('M')`

### 📦 2. Aggregate by Site/Month
- **Storage usage**: Sum of `storage_bytes`, converted to GB
- **Background jobs**: Sum of `background_job_min`
- **Activity**: Sum of `event_count`

### 👥 3. Count Users by License Type
- Viewer, Explorer, Creator breakdown (site-level only)

### 🔁 4. Merge All Tables
- Joins are performed using `site_id` and `month`
- Fills in missing values for storage and jobs as `0`
- Metadata fields are joined from `sites` and `customers`

---

## Output

The result is saved as: monthly_site_summary.csv


This file includes:
- `site_id`, `month`
- `event_count`, `storage_gb`, `background_job_min`
- License breakdown (Viewer, Explorer, Creator)
- `customer_id`, `region`, `industry`, `account_tier`

---

## Run This Script

If you're in the `/02-unify/` folder, run:

```bash
python build_monthly_summary.py

Output file: monthly_site_summary.csv
Output location: saved to the same folder

## Notes

The aggregation assumes month is the granularity for tracking SaaS engagement
User license counts are static (based on last month of activity)
