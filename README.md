# SaaS User Activity Analysis Project

## Overview
This project demonstrates an end-to-end analytics workflow—starting with generating realistic synthetic SaaS data in Python, and moving into structured SQL-based analysis using Google BigQuery.

The goal: simulate usage data across customer sites to understand user engagement, storage behavior, and background job performance within a hypothetical SaaS platform.

---

## Business Problem
A SaaS company wants to analyze how users interact with the platform, how much storage is consumed, and which customers rely heavily on background processing.

Insights from this analysis can:
- Surface early onboarding signals
- Inform pricing and licensing strategies
- Optimize resource usage and support operations

---

## Data Generation (Python)

Synthetic data was created using:
- **Faker:** Realistic fake names, domains, and dates
- **Pandas:** Data structuring and export to CSV
- **Random / datetime:** Value generation and date ranges

The Python script [`generate_saas_data.py`](generate_saas_data.py) creates 6 raw tables:

| File | Description |
|------|-------------|
| `saas_customer_info.csv` | Customer metadata (region, tier, industry) |
| `saas_sites.csv` | Mapping of sites to customers |
| `saas_storage.csv` | Daily storage usage per site |
| `saas_users.csv` | Users with license types and registration dates |
| `saas_user_activity.csv` | Daily user activity by site and type |
| `saas_background_jobs.csv` | Background job execution logs per site |

Each file simulates realistic activity patterns and relationships among entities.

---

## 🗂️ Database Schema Summary

### `saas_storage.csv`

| Column | Type | Description |
|--------|------|-------------|
| `customer_id` | STRING | Customer ID |
| `site_id` | STRING | Site ID |
| `date` | DATE | Daily timestamp |
| `storage_bytes` | INTEGER | Bytes stored |

### `saas_user_activity.csv`

| Column | Type | Description |
|--------|------|-------------|
| `customer_id` | STRING | Customer ID |
| `user_email` | STRING | User identifier |
| `site_id` | STRING | Site of activity |
| `date` | DATE | Activity date |
| `activity_type` | STRING | Type of event (e.g. Access, Create) |
| `event_count` | INTEGER | Count per activity type |

### `saas_background_jobs.csv`

| Column | Type | Description |
|--------|------|-------------|
| `site_id` | STRING | Site ID |
| `date` | DATE | Execution date |
| `background_job_type` | STRING | Job category (e.g. flow run, alert) |
| `background_job_min` | INTEGER | Duration in minutes |

### `saas_users.csv`

| Column | Type | Description |
|--------|------|-------------|
| `customer_id` | STRING | Customer ID |
| `site_id` | STRING | Site ID |
| `user_email` | STRING | User email |
| `registration_date` | DATE | Registration date |
| `license_type` | STRING | Viewer / Explorer / Creator |

---

## 🧠 Data Analysis (BigQuery)

After uploading the CSVs into Google BigQuery, I used SQL to:
- Join and unify tables at the **site-month** level
- Aggregate event counts, storage, background job minutes
- Track user license types and registration patterns
- Filter for onboarding signals (e.g. high activity, no storage)
- Segment by customer tier, region, and industry

📄 Detailed SQL logic is documented in [`README-analysis.md`](https://github.com/Cath-L/saas-user-analysis/blob/main/README-analysis.md)

---

## 🛠️ Tools Used
- **Python**: Data generation (Faker, Pandas)
- **Google BigQuery**: Scalable SQL analysis
- **SQL**: Data joins, aggregations, segmentation
- **Google Site**: Visual case study presentation  
- **GitHub**: Version control, documentation

Explore the project visually on my [Google Site Portfolio](https://sites.google.com/view/cathy-leung/home).

---

## ✅ Conclusion

This project showcases:
- My ability to simulate SaaS user behavior and usage data
- How I translate raw data into business-ready metrics
- A full workflow from data creation to executive-level insights

It reflects both **technical fluency** and **strategic thinking**, which I bring to every analytics role I pursue.
