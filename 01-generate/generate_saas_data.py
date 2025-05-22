import pandas as pd
import random
from datetime import datetime

# Initialize Faker
fake = Faker()

# --- Configuration ---
num_customers = 65
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Fixed lists
industries = [
    "Technology", "Finance", "Healthcare", "Retail", "Education",
    "Manufacturing", "Transportation & Logistics", "Media & Entertainment",
    "Professional Services", "Government & Public Sector"
]
regions = ['North America', 'EMEA', 'APAC']
account_tiers = ['Commercial', 'SMB', 'Enterprise']
activity_types = ['Access', 'Create', 'View', 'Publish']
background_job_types = ['extract', 'subscription', 'flow run', 'alert', 'bridge']

# --- 1. Customer Info Table ---
customer_info_data = []
for i in range(1, num_customers + 1):
    customer_id = str(10**9 + i)  # 10-digit ID
    industry = random.choice(industries)
    region = random.choice(regions)
    account_tier = random.choice(account_tiers)
    contact_email = fake.company_email()
    customer_info_data.append({
        'customer_id': customer_id,
        'industry': industry,
        'region': region,
        'account_tier': account_tier,
        'contact_email': contact_email
    })
customer_info_df = pd.DataFrame(customer_info_data)

# Define internal accounts (first 8 customers)
internal_accounts = customer_info_df['customer_id'].iloc[:8].tolist()

# --- 2. Site Info Table ---
site_ids = set()
site_data = []
for customer_id in customer_info_df['customer_id']:
    num_sites = random.randint(1, 3)
    for _ in range(num_sites):
        while True:
            site_id = "A" + ''.join(random.choices('0123456789', k=11))
            if site_id not in site_ids:
                site_ids.add(site_id)
                break
        site_data.append({
            'customer_id': customer_id,
            'site_id': site_id
        })
site_df = pd.DataFrame(site_data)

# --- 3. Storage Table ---
storage_data = []
for _, row in site_df.iterrows():
    for date in date_range:
        storage_bytes = random.randint(1_000_000, 100_000_000)
        storage_data.append({
            'customer_id': row['customer_id'],
            'site_id': row['site_id'],
            'date': date.strftime('%Y-%m-%d'),
            'storage_bytes': storage_bytes
        })
storage_df = pd.DataFrame(storage_data)

# --- 4. Users Table ---
users_data = []
for customer_id in customer_info_df['customer_id']:
    domain = random.choice(['.com', '.org', '.net'])
    customer_sites = site_df[site_df['customer_id'] == customer_id]['site_id'].tolist()
    
    # Create a pool of unique users for this customer
    num_unique_users = random.randint(1, 10)
    user_pool = []
    for _ in range(num_unique_users):
        username = fake.user_name()
        user_email = f"{username}@{fake.domain_name()}{domain}"
        registration_date = fake.date_between(start_date='-2y', pd.Timedelta(days=1))
        license_type = random.choice(['Viewer', 'Explorer', 'Creator'])
        user_pool.append({
            'customer_id': customer_id,
            'user_email': user_email,
            'registration_date': registration_date.strftime('%Y-%m-%d'),
            'license_type': license_type
        })

    # Assign users randomly to sites
    for site_id in customer_sites:
        num_site_users = random.randint(1, len(user_pool))
        assigned_users = random.sample(user_pool, num_site_users)
        for user in assigned_users:
            users_data.append({
                'customer_id': user['customer_id'],
                'site_id': site_id,
                'user_email': user['user_email'],
                'registration_date': user['registration_date'],
                'license_type': user['license_type']
            })
users_df = pd.DataFrame(users_data)

# --- 5. User Activity Table ---
user_activity_data = []
for _, row in site_df.iterrows():
    customer_users = users_df[users_df['customer_id'] == row['customer_id']]['user_email'].tolist()
    for date in date_range:
        for user_email in customer_users:
            num_activities = random.randint(1, 4)
            for _ in range(num_activities):
                activity_type = random.choice(activity_types)
                user_activity_data.append({
                    'customer_id': row['customer_id'],
                    'user_email': user_email,
                    'site_id': row['site_id'],
                    'date': date.strftime('%Y-%m-%d'),
                    'activity_type': activity_type
                })
user_activity_df = pd.DataFrame(user_activity_data)
activity_counts_df = user_activity_df.groupby(
    ['customer_id', 'user_email', 'site_id', 'date', 'activity_type']
).size().reset_index(name='event_count')

# --- 6. Background Job Table ---
background_job_data = []
for _, row in site_df.iterrows():
    for date in date_range:
        for job_type in background_job_types:
            job_minutes = random.randint(1, 80)
            background_job_data.append({
                'customer_id': row['customer_id'],
                'site_id': row['site_id'],
                'date': date.strftime('%Y-%m-%d'),
                'background_job_type': job_type,
                'background_job_min': job_minutes
            })
background_job_df = pd.DataFrame(background_job_data)

# --- Output CSVs ---
customer_info_df.to_csv('saas_customer_info.csv', index=False)
site_df.to_csv('saas_sites.csv', index=False)
storage_df.to_csv('saas_storage.csv', index=False)
users_df.to_csv('saas_users.csv', index=False)
activity_counts_df.to_csv('saas_user_activity.csv', index=False)
background_job_df.to_csv('saas_background_jobs.csv', index=False)

# --- Summary of Generated Categories ---
print(" Synthetic SaaS data saved. Files:")
print("- saas_customer_info.csv")
print("- saas_sites.csv")
print("- saas_storage.csv")
print("- saas_users.csv")
print("- saas_user_activity.csv")
print("- saas_background_jobs.csv")

print("\n Sample Activity Types:", activity_types)
print(" Sample Background Job Types:", background_job_types)
print(" Internal Customer IDs:", internal_accounts)
