# saas-user-analysis

# SaaS User Activity Analysis Project

## Overview

This project demonstrates an end-to-end data analysis workflow, from generating realistic synthetic data using Python to performing insightful analysis using SQL joins and complex queries in Google BigQuery. The focus is on understanding user behavior, storage patterns, and background job activity within a hypothetical SaaS platform.

## Business Problem (Example)

A SaaS company wants to gain insights into how users are interacting with their platform, how much storage they are consuming, and the performance of background jobs. This analysis can help identify areas for product improvement, optimize resource allocation, and understand user engagement levels.

## Data Generation (Python)

The synthetic data for this project was generated using Python and the following libraries:

* **Faker:** For creating realistic fake data (e.g., user names, emails, dates).
* **Pandas:** For structuring the generated data into DataFrames and exporting to CSV files.
* **NumPy:** For numerical operations and generating random values.
* **Random:** For random selections (e.g., activity types).
* **datetime:** For handling date and time ranges.

You can find the Python script used for data generation in this repository: [`generate_saas_data.py`](generate_saas_data.py)

```python
from faker import Faker
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# --- Configuration ---
num_customers = 50
num_sites_per_customer = 3
users_per_customer = 5
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 3, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
activity_types = ['Access', 'Create', 'View', 'Publish']
background_job_types = ['extract', 'subscription', 'flow run', 'alert', 'bridge']

# --- 1. Customer Info Table ---
customer_info_data = []
for customer_id in range(1, num_customers + 1):
    industry = random.choice(['Tech', 'Finance', 'Healthcare', 'Retail'])
    region = random.choice(['North America', 'EMEA', 'APAC'])
    account_tier = random.choice(['Standard', 'Premium', 'Enterprise'])
    contact_email = fake.company_email()
    customer_info_data.append({
        'customer_id': customer_id,
        'industry': industry,
        'region': region,
        'account_tier': account_tier,
        'contact_email': contact_email
    })
customer_info_df = pd.DataFrame(customer_info_data)

# --- 2. Storage Table ---
storage_data = []
for customer_id in range(1, num_customers + 1):
    for site_id in range(1, num_sites_per_customer + 1):
        for date in date_range:
            storage_bytes = random.randint(1_000_000, 100_000_000)  # 1MB to 100MB
            storage_data.append({
                'customer_id': customer_id,
                'site_id': f'site_{customer_id}_{site_id}',
                'date': date.strftime('%Y-%m-%d'),
                'storage_bytes': storage_bytes
            })
storage_df = pd.DataFrame(storage_data)

# --- 3. Users Table ---
users_data = []
for customer_id in range(1, num_customers + 1):
    for i in range(1, users_per_customer + 1):
        user_email = fake.email()
        registration_date = fake.date_between(start_date='-2y', end_date='-1m')
        users_data.append({
            'customer_id': customer_id,
            'user_email': user_email,
            'registration_date': registration_date.strftime('%Y-%m-%d')
        })
users_df = pd.DataFrame(users_data)

# --- 4. User Activity Table ---
user_activity_data = []
for customer_id in range(1, num_customers + 1):
    customer_users = users_df[users_df['customer_id'] == customer_id]['user_email'].tolist()
    for site_id in range(1, num_sites_per_customer + 1):
        for date in date_range:
            for user_email in customer_users:
                num_activities = random.randint(0, 5)
                for _ in range(num_activities):
                    activity_type = random.choice(activity_types)
                    user_activity_data.append({
                        'customer_id': customer_id,
                        'user_email': user_email,
                        'site_id': f'site_{customer_id}_{site_id}',
                        'date': date.strftime('%Y-%m-%d'),
                        'activity_type': activity_type
                    })
user_activity_df = pd.DataFrame(user_activity_data)
activity_counts_df = user_activity_df.groupby(
    ['customer_id', 'user_email', 'site_id', 'date', 'activity_type']
).size().reset_index(name='event_count')

# --- 5. Background Job Table ---
background_job_data = []
for customer_id in range(1, num_customers + 1):
    for site_id in range(1, num_sites_per_customer + 1):
        site_identifier = f'site_{customer_id}_{site_id}'
        for date in date_range:
            for job_type in background_job_types:
                job_minutes = random.randint(1, 30)
                background_job_data.append({
                    'customer_id': customer_id,
                    'site_id': site_identifier,
                    'date': date.strftime('%Y-%m-%d'),
                    'background_job_type': job_type,
                    'background_job_min': job_minutes
                })
background_job_df = pd.DataFrame(background_job_data)

# --- Output to CSV Files ---
customer_info_df.to_csv('saas_customer_info.csv', index=False)
storage_df.to_csv('saas_storage.csv', index=False)
users_df.to_csv('saas_users.csv', index=False)
activity_counts_df.to_csv('saas_user_activity.csv', index=False)
background_job_df.to_csv('saas_background_jobs.csv', index=False)

print("Synthetic SaaS data generated and saved to 5 CSV files:")
print("- saas_customer_info.csv")
print("- saas_storage.csv")
print("- saas_users.csv")
print("- saas_user_activity.csv")
print("- saas_background_jobs.csv")
```

## Database Schema
The project utilizes four tables to represent the SaaS user activity data:

**saas_storage:**

| Column Name   | Data Type | Description                     |
|---------------|-----------|---------------------------------|
| `customer_id` | INTEGER   | Unique identifier for the customer |
| `site_id`     | VARCHAR   | Identifier for the customer's site |
| `date`        | DATE      | Date of the storage record        |
| `storage_bytes`| INTEGER   | Storage used in bytes             |

**saas_user_activity:**

| Column Name   | Data Type | Description                       |
|---------------|-----------|-----------------------------------|
| `customer_id` | INTEGER   | Unique identifier for the customer  |
| `user_email`  | VARCHAR   | Email address of the user         |
| `site_id`     | VARCHAR   | Identifier for the site of activity |
| `date`        | DATE      | Date of the activity              |
| `activity_type`| VARCHAR   | Type of user activity (e.g., Access)|
| `event_count` | INTEGER   | Number of times the activity occurred |

**saas_background_jobs:**

| Column Name          | Data Type | Description                       |
|----------------------|-----------|-----------------------------------|
| `site_id`            | VARCHAR   | Identifier for the site of the job  |
| `date`               | DATE      | Date of the job execution         |
| `background_job_type`| VARCHAR   | Type of background job (e.g., extract)|
| `background_job_min` | INTEGER   | Duration of the job in minutes      |

**saas_users:**

| Column Name       | Data Type | Description                     |
|-------------------|-----------|---------------------------------|
| `customer_id`     | INTEGER   | Unique identifier for the customer |
| `user_email`      | VARCHAR   | Email address of the user         |
| `registration_date`| DATE      | Date when the user registered      |

## Data Analysis (Google BigQuery)
The generated CSV files were uploaded to Google BigQuery for scalable storage and in-depth analysis using SQL. The analysis involved:

* Aggregating data to a monthly level.
* Joining tables to combine information across different entities.
* Calculating key metrics like storage usage, user activity, active users, and background job performance.
* Filtering out specific background job types for focused analysis.
* Presenting the results in a structured format for insights.
* Detailed documentation of the BigQuery SQL queries and the resulting analysis can be found in [README-analysis.md](https://github.com/Cath-L/saas-user-analysis/blob/main/README-analysis.md)

## Tools Used
* **Python**: For synthetic data generation.
*  **Pandas**: For data manipulation and export.
*  **Faker**: For generating realistic fake data.
*  **Google BigQuery**: For scalable data storage and analysis.
*  **SQL**: For querying and analyzing the data in BigQuery.
*  **Google Site Portfolio**
Screenshots and a description of how this project is presented on my [Google Site portfolio](https://sites.google.com/view/cathy-leung/home). The Google Site provides a visual overview of the project, including the business context, data schema, key findings from the BigQuery analysis, and links to the code repositories.

## Conclusion
This project demonstrates my ability to generate realistic data using Python and perform comprehensive data analysis using SQL in Google BigQuery. The end-to-end workflow highlights the process of creating data and then extracting valuable insights for a SaaS platform.
