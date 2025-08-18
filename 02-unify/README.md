# 02 – Build Monthly Summary

## Overview
This step takes the six raw data tables generated in **Step 01** and merges them into a unified, analysis-ready dataset called **`monthly_site_summary.csv`**.

The final dataset includes:
- **Monthly user activity** per site (`activity_events`)
- **Total storage used (GB)** per site (`storage_gb`)
- **Total background job minutes** per site (`background_job_min`)
- **License type breakdown** per site (View-Only, Standard, Power Users)
- **Customer & site metadata** (region, industry, tier, lifecycle dates)

This summary supports executive dashboards, onboarding cohort tracking, and GPT-powered segment summaries.

---

## Inputs (from `01-generate/`)
- `saas_customer_info.csv`
- `saas_sites.csv`
- `saas_storage.csv`
- `saas_users.csv`
- `saas_user_activity.csv`
- `saas_background_jobs.csv`

---

## What the Script Does

### 1) Parse dates & extract month
- Parses `date` in **storage**, **activity**, and **jobs**
- Creates a **`month`** column using `dt.to_period('M')`

### 2) Aggregate to site × month
- **Activity**: sum of `event_count` → `activity_events`
- **Storage**: sum of `storage_bytes`, convert to GB → `storage_gb`
- **Background jobs**: sum of `background_job_min`

### 3) Users by license (site-level)
Renames license buckets and counts users per site:
- `Viewer` → **View-Only Users**
- `Explorer` → **Standard Users**
- `Creator` → **Power Users**

Ensures all three columns exist even if zero.

### 4) Merge everything
- Outer-merges monthly aggregates on `site_id` + `month`
- Fills missing metrics with `0`
- Joins **site** and **customer** metadata (incl. `purchase_date`, `active_date`, `is_internal`)
- Adds helpful timestamps: **`month_start`** and **`month_end`**

---

## Output
- **File:** `monthly_site_summary.csv`
- **Location:** same folder as the script

### Expected Columns (excerpt)
- Keys: `site_id`, `month`, `month_start`, `month_end`
- Metrics: `activity_events`, `storage_gb`, `background_job_min`
- License breakdown: `View-Only Users`, `Standard Users`, `Power Users`
- Metadata: `customer_id`, `industry`, `region`, `account_tier`, `purchase_date`, `active_date`, `is_internal`

> Note: License counts are **site-level (static)**, not month-aware.

---

## How to Run

From the `02-unify/` directory (or adjust paths accordingly):

```bash
python build_monthly_summary.py
