import pandas as pd

# ---------- Load ----------
customers = pd.read_csv('saas_customer_info.csv')   # may include purchase_date, active_date, is_internal
sites     = pd.read_csv('saas_sites.csv')
storage   = pd.read_csv('saas_storage.csv')
users     = pd.read_csv('saas_users.csv')
activity  = pd.read_csv('saas_user_activity.csv')
jobs      = pd.read_csv('saas_background_jobs.csv')

# ---------- Parse dates + month ----------
for df, col in [(storage,'date'), (activity,'date'), (jobs,'date')]:
    df[col] = pd.to_datetime(df[col], errors='coerce')
    df['month'] = df[col].dt.to_period('M')

# ---------- Monthly aggregations (no filtering) ----------
# Activity (events per site × month)
activity_agg = (
    activity.groupby(['site_id','month'], as_index=False)['event_count']
            .sum()
            .rename(columns={'event_count':'activity_events'})
)

# Storage (sum bytes → GB per site × month)
storage_agg = (
    storage.groupby(['site_id','month'], as_index=False)['storage_bytes']
           .sum()
           .assign(storage_gb=lambda d: (d['storage_bytes']/(1024**3)).round(2))
           .drop(columns='storage_bytes')
)

# Background jobs (minutes per site × month)
jobs_agg = jobs.groupby(['site_id','month'], as_index=False)['background_job_min'].sum()

# ---------- Users by license (site-level, not month-aware) ----------
# rename license buckets
license_map = {
    'Viewer':   'View-Only Users',
    'Explorer': 'Standard Users',
    'Creator':  'Power Users'
}
users['license_type_renamed'] = users['license_type'].map(license_map).fillna(users['license_type'])

user_agg = (
    users.groupby(['site_id','license_type_renamed'])
         .size()
         .unstack(fill_value=0)
         .reset_index()
)

# ensure all 3 columns exist
for col in ['View-Only Users','Standard Users','Power Users']:
    if col not in user_agg.columns:
        user_agg[col] = 0

# ---------- Build monthly site summary ----------
monthly = activity_agg.copy()
monthly = monthly.merge(storage_agg, on=['site_id','month'], how='outer')
monthly = monthly.merge(jobs_agg, on=['site_id','month'], how='outer')

# fill NaNs for metrics
for col in ['activity_events','storage_gb','background_job_min']:
    if col in monthly.columns:
        monthly[col] = monthly[col].fillna(0)

# attach site + customer metadata (no filtering)
monthly = monthly.merge(sites, on='site_id', how='left')
monthly = monthly.merge(customers, on='customer_id', how='left')

# attach user license breakdown (site-level)
monthly = monthly.merge(user_agg, on='site_id', how='left')

# helpful timestamps for BI
monthly['month_start'] = monthly['month'].dt.to_timestamp()
monthly['month_end']   = monthly['month'].dt.to_timestamp('M')

# export one file
monthly.to_csv('monthly_site_summary.csv', index=False)
print(" monthly_site_summary.csv saved.")
