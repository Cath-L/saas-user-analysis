
import pandas as pd

# Load data
customers = pd.read_csv('saas_customer_info.csv')
site_df = pd.read_csv('saas_sites.csv')  
storage = pd.read_csv('saas_storage.csv')
users = pd.read_csv('saas_users.csv')
activity = pd.read_csv('saas_user_activity.csv')
jobs = pd.read_csv('saas_background_jobs.csv')

# Convert date columns to datetime and extract month
storage['date'] = pd.to_datetime(storage['date'])
jobs['date'] = pd.to_datetime(jobs['date'])
activity['date'] = pd.to_datetime(activity['date'])

storage['month'] = storage['date'].dt.to_period('M')
jobs['month'] = jobs['date'].dt.to_period('M')
activity['month'] = activity['date'].dt.to_period('M')

# --- Monthly Aggregation ---

# 📦 Storage in GB
storage_agg = storage.groupby(['site_id', 'month'])['storage_bytes'].sum().reset_index()
storage_agg['storage_gb'] = (storage_agg['storage_bytes'] / (1024**3)).round(2)
storage_agg.drop(columns='storage_bytes', inplace=True)

# ⚙️ Background Job Time
jobs_agg = jobs.groupby(['site_id', 'month'])['background_job_min'].sum().reset_index()

# 📊 Activity Count
activity_agg = activity.groupby(['site_id', 'month'])['event_count'].sum().reset_index()

# 👥 User count per license type (site-level only, not month-aware)
users['month'] = activity['month'].max()  # Use latest activity month
user_agg = users.groupby(['site_id', 'license_type']).size().unstack(fill_value=0).reset_index()

# Start with activity as the base
monthly_summary = activity_agg.copy()

# Merge in storage and job time
monthly_summary = pd.merge(monthly_summary, storage_agg, on=['site_id', 'month'], how='left')
monthly_summary = pd.merge(monthly_summary, jobs_agg, on=['site_id', 'month'], how='left')

# Fill missing values
monthly_summary[['storage_gb', 'background_job_min']] = monthly_summary[['storage_gb', 'background_job_min']].fillna(0)

# Merge metadata
monthly_summary = pd.merge(monthly_summary, site_df, on='site_id', how='left')
monthly_summary = pd.merge(monthly_summary, customers, on='customer_id', how='left')

# Merge user license type breakdown
monthly_summary = pd.merge(monthly_summary, user_agg, on='site_id', how='left')

# Export
monthly_summary.to_csv('monthly_site_summary.csv', index=False)
print("✅ monthly_site_summary.csv has been saved to your folder.")
display(monthly_site_summary.head(10))
