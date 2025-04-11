from faker import Faker
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

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

# --- 1. Storage Table ---
storage_data = []
for customer_id in range(1, num_customers + 1):
    for site_id in range(1, num_sites_per_customer + 1):
        for date in date_range:
            storage_bytes = random.randint(1_000_000, 100_000_000)  # 1MB to 100MB
            storage_data.append({'customer_id': customer_id,
                                 'site_id': f'site_{site_id}',
                                 'date': date.strftime('%Y-%m-%d'),
                                 'storage_bytes': storage_bytes})
storage_df = pd.DataFrame(storage_data)

# --- 4. Users Table ---
users_data = []
for customer_id in range(1, num_customers + 1):
    for i in range(1, users_per_customer + 1):
        user_email = fake.email()
        registration_date = fake.date_between(start_date='-2y', end_date='-1m')
        users_data.append({'customer_id': customer_id,
                           'user_email': user_email,
                           'registration_date': registration_date.strftime('%Y-%m-%d')})
users_df = pd.DataFrame(users_data)

# --- 2. User Activity Table ---
user_activity_data = []
for customer_id in range(1, num_customers + 1):
    customer_users = users_df[users_df['customer_id'] == customer_id]['user_email'].tolist()
    for site_id in range(1, num_sites_per_customer + 1):
        for date in date_range:
            for user_email in customer_users:
                num_activities = random.randint(0, 5)  # Up to 5 activities per user per site per day
                for _ in range(num_activities):
                    activity_type = random.choice(activity_types)
                    user_activity_data.append({'customer_id': customer_id,
                                                'user_email': user_email,
                                                'site_id': f'site_{site_id}',
                                                'date': date.strftime('%Y-%m-%d'),
                                                'activity_type': activity_type})
user_activity_df = pd.DataFrame(user_activity_data)
activity_counts_df = user_activity_df.groupby(['customer_id', 'user_email', 'site_id', 'date', 'activity_type']).size().reset_index(name='event_count')

# --- 3. Background Job Table ---
background_job_data = []
for site_id_index in range(1, num_customers * num_sites_per_customer + 1):
    customer_id = (site_id_index - 1) // num_sites_per_customer + 1
    site_id = (site_id_index - 1) % num_sites_per_customer + 1
    site_identifier = f'site_{site_id}'
    for date in date_range:
        for job_type in background_job_types:
            job_minutes = random.randint(1, 30)  # Background job duration in minutes
            background_job_data.append({'site_id': site_identifier,
                                         'date': date.strftime('%Y-%m-%d'),
                                         'background_job_type': job_type,
                                         'background_job_min': job_minutes})
background_job_df = pd.DataFrame(background_job_data)

# --- Output to CSV Files ---
storage_df.to_csv('saas_storage.csv', index=False)
activity_counts_df.to_csv('saas_user_activity.csv', index=False)
background_job_df.to_csv('saas_background_jobs.csv', index=False)
users_df.to_csv('saas_users.csv', index=False)

print("Synthetic SaaS user activity data generated and saved to 4 CSV files:")
print("- saas_storage.csv")
print("- saas_user_activity.csv")
print("- saas_background_jobs.csv")
print("- saas_users.csv")