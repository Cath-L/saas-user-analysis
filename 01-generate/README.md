# SaaS User Activity Analysis Project

## Overview
This project demonstrates an **end-to-end analytics workflow** — starting with generating realistic synthetic SaaS data in **Python**, and moving into structured SQL-based analysis using **Google BigQuery**.  

The goal: simulate **usage data across customer sites** to understand user engagement, storage behavior, and background job performance within a hypothetical SaaS platform.  

---

## Business Problem
A SaaS company wants to analyze:  
- How users interact with the platform  
- How much storage is consumed  
- Which customers rely heavily on background processing  

Insights from this analysis can:  
- Surface **early onboarding signals**  
- Inform **pricing and licensing strategies**  
- Optimize **resource usage and support operations**  

---

## Data Generation (Python)
Synthetic data was created using:  
- **Faker** → realistic fake names, domains, dates  
- **Pandas** → structuring, transformation, CSV export  
- **Random / datetime** → activity & date generation with daily variability  
- **Seasonality model** → usage peaks in April & October, troughs in December & January  

The script `generate_saas_data.py` creates **6 raw tables (CSV exports):**

| File | Description |
|------|-------------|
| `saas_customer_info.csv` | Customer metadata with lifecycle dates |
| `saas_sites.csv` | Mapping of sites to customers |
| `saas_storage.csv` | Daily storage usage per site |
| `saas_users.csv` | Users with license types & registration dates |
| `saas_user_activity.csv` | Daily user activity by site and type |
| `saas_background_jobs.csv` | Background job execution logs per site |

Each file simulates realistic **growth**, **seasonal activity**, and **relationships across entities**.  

---

## Database Schema Summary

### `saas_customer_info.csv`
| Column | Type | Description |
|--------|------|-------------|
| customer_id | STRING | Unique 10-digit ID (first 8 = internal accounts) |
| industry | STRING | One of 10 industries (Technology, Finance, Healthcare, etc.) |
| region | STRING | North America, EMEA, or APAC |
| account_tier | STRING | Commercial, SMB, or Enterprise |
| contact_email | STRING | Customer contact email |
| is_internal | BOOLEAN | Whether account is internal |
| purchase_date | DATE | Customer purchase date |
| active_date | DATE | Activation date (onboarding start) |

---

### `saas_sites.csv`
| Column | Type | Description |
|--------|------|-------------|
| site_id | STRING | Unique 12-character ID (`A` + alphanumeric) |
| customer_id | STRING | Customer ID |
| active_date | DATE | Site activation date |

---

### `saas_storage.csv`
| Column | Type | Description |
|--------|------|-------------|
| customer_id | STRING | Customer ID |
| site_id | STRING | Site ID |
| date | DATE | Daily timestamp |
| storage_bytes | INTEGER | Scaled storage consumption per active site-day (seasonal + noisy) |

---

### `saas_users.csv`
| Column | Type | Description |
|--------|------|-------------|
| customer_id | STRING | Customer ID |
| site_id | STRING | Site ID |
| user_email | STRING | User email (`username@domain`) |
| registration_date | DATE | Date of registration (after activation date) |
| license_type | STRING | Viewer, Explorer, Creator |

---

### `saas_user_activity.csv`
| Column | Type | Description |
|--------|------|-------------|
| customer_id | STRING | Customer ID |
| user_email | STRING | User identifier |
| site_id | STRING | Site ID |
| date | DATE | Date of activity |
| activity_type | STRING | Access, Create, View, Publish |
| event_count | INTEGER | Aggregated activity count per user-day |

---

### `saas_background_jobs.csv`
| Column | Type | Description |
|--------|------|-------------|
| customer_id | STRING | Customer ID |
| site_id | STRING | Site ID |
| date | DATE | Job execution date |
| background_job_type | STRING | extract, subscription, flow run, alert, bridge |
| background_job_min | INTEGER | Job duration (1–80 mins) |

---

## Data Analysis (BigQuery)
After uploading into **BigQuery**, SQL was used to:  
- Join & unify tables at the **site-month level**  
- Aggregate **event counts, storage GB, background job minutes**  
- Track **user licensing & onboarding patterns**  
- Segment behavior by **region, tier, and industry**  
- Isolate **internal accounts** for filtering  
- Apply **seasonality trends** to analyze demand cycles  

Detailed SQL logic is in **`README-analysis.md`**  

---

## ⚙️ Tools Used
- **Python** → Data generation (`Faker`, `Pandas`, `Dateutil`)  
- **Google BigQuery** → Scalable SQL analysis  
- **SQL** → Joins, aggregation, segmentation  
- **Google Site** → Visual case study presentation  
- **GitHub** → Version control, documentation  

---

## Conclusion
This project demonstrates:  
- How to simulate **realistic SaaS data** with growth, seasonality, and onboarding  
- Translating **raw events into business-ready insights**  
- A full **analytics workflow**: generation → modeling → SQL → business strategy  

It reflects both **technical fluency** and **strategic thinking**, highlighting the value I bring as a data & ops analyst.  
