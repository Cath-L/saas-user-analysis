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

**`saas_customer_info.csv`**

| Column         | Type   | Description                                  |
|----------------|--------|----------------------------------------------|
| `customer_id`  | STRING | Unique 10-digit customer ID                  |
| `industry`     | STRING | Industry type (e.g., Finance, Healthcare)   |
| `region`       | STRING | Region (North America, EMEA, APAC)          |
| `account_tier` | STRING | Commercial, SMB, or Enterprise              |
| `contact_email`| STRING | Customer contact email address              |

**`saas_sites.csv`**

| Column        | Type   | Description                              |
|---------------|--------|------------------------------------------|
| `site_id`     | STRING | Unique 12-digit alphanumeric site ID    |
| `customer_id` | STRING | Customer ID linked to this site         |

**`saas_storage.csv`**

| Column         | Type   | Description                           |
|----------------|--------|---------------------------------------|
| `customer_id`  | STRING | Customer ID                           |
| `site_id`      | STRING | Site ID                               |
| `date`         | DATE   | Daily timestamp                       |
| `storage_bytes`| INTEGER| Amount of storage used (in bytes)     |

**`saas_users.csv`**

| Column             | Type   | Description                                  |
|--------------------|--------|----------------------------------------------|
| `customer_id`      | STRING | Customer ID                                  |
| `site_id`          | STRING | Site ID where user is assigned               |
| `user_email`       | STRING | User email address                           |
| `registration_date`| DATE   | Date of user registration                    |
| `license_type`     | STRING | License type (Viewer, Explorer, Creator)     |

**`saas_user_activity.csv`**

| Column         | Type   | Description                                  |
|----------------|--------|----------------------------------------------|
| `customer_id`  | STRING | Customer ID                                  |
| `user_email`   | STRING | User identifier                              |
| `site_id`      | STRING | Site where activity occurred                 |
| `date`         | DATE   | Date of the activity                         |
| `activity_type`| STRING | Access, Create, View, or Publish             |
| `event_count`  | INTEGER| Number of times the activity occurred        |

**`saas_background_jobs.csv`**

| Column              | Type   | Description                                 |
|---------------------|--------|---------------------------------------------|
| `customer_id`       | STRING | Customer ID                                 |
| `site_id`           | STRING | Site ID                                     |
| `date`              | DATE   | Execution date                              |
| `background_job_type`| STRING| Job category (e.g. flow run, alert)         |
| `background_job_min`| INTEGER| Duration of the job in minutes              |

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
