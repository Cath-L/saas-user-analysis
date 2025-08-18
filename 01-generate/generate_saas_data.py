import pandas as pd
import random
import string
from datetime import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker
fake = Faker()

# ----------------------- Time Window -----------------------
START_DATE = datetime(2023, 1, 1)
END_DATE   = datetime(2024, 12, 31)
DATE_RANGE = pd.date_range(start=START_DATE, end=END_DATE, freq='D')

# ----------------------- Seasonality -----------------------
# Peaks: Apr (4), Oct (10). Lows: Dec (12), Jan (1).
SEASONALITY = {
    1: 0.80, 2: 0.90, 3: 1.00, 4: 1.20, 5: 1.05, 6: 1.00,
    7: 0.95, 8: 0.90, 9: 1.00, 10: 1.20, 11: 1.05, 12: 0.80
}
def month_mult(dt): return SEASONALITY[dt.month]

# ----------------------- Population Dynamics -----------------------
INITIAL_CUSTOMERS         = 40                # start cohort at START_DATE month
BASE_NEW_CUSTOMERS_MONTH  = (2, 6)            # baseline new signups per month (scaled by seasonality)

# ----------------------- Sites / Users -----------------------
SITES_PER_CUSTOMER        = (1, 3)
USERS_PER_CUSTOMER        = (3, 12)
LICENSE_TYPES             = ['Viewer', 'Explorer', 'Creator']
POSSIBLE_DOMAINS          = ['example.com', 'sample.org', 'demo.net', 'contoso.com', 'acme.org']

# ----------------------- Activity / Jobs -----------------------
USER_ACTIVE_PROB_BASE     = 0.30              # baseline user active prob per site-day
ACTIVITIES_PER_ACTIVE_DAY = (1, 4)
WEEKDAY_JOB_BASE_P        = 0.60
WEEKEND_JOB_BASE_P        = 0.30
JOBS_PER_JOB_DAY          = (1, 3)

# ----------------------- Storage -----------------------
STORAGE_BYTES_RANGE       = (1_000_000, 100_000_000)  # per site per active day

# ----------------------- Business Dimensions -----------------------
INDUSTRIES = [
    "Technology", "Finance", "Healthcare", "Retail", "Education",
    "Manufacturing", "Transportation & Logistics", "Media & Entertainment",
    "Professional Services", "Government & Public Sector"
]
REGIONS = ['North America', 'EMEA', 'APAC']
ACCOUNT_TIERS = ['Commercial', 'SMB', 'Enterprise']

ACTIVITY_TYPES = ['Access', 'Create', 'View', 'Publish']
BACKGROUND_JOB_TYPES = ['extract', 'subscription', 'flow run', 'alert', 'bridge']

# ----------------------- Helpers -----------------------
def gen_site_id():
    # 'A' + 11 uppercase alphanumerics
    return 'A' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=11))

def next_customer_id(idx):
    # 10-digit string starting 1000000001
    return str(10**9 + idx)

def daily_noise(low=0.9, high=1.1):
    # ±10% random factor
    return random.uniform(low, high)

# ----------------------- Build Customer Population (purchase + active dates) -----------------------
customers = []   # dict: id, attrs, purchase_date, active_date, domain
customer_idx = 0

month_cursor = datetime(START_DATE.year, START_DATE.month, 1)
end_month_cursor = datetime(END_DATE.year, END_DATE.month, 1)

# Initial cohort (Jan 2023)
for _ in range(INITIAL_CUSTOMERS):
    customer_idx += 1
    purchase_date = month_cursor.date()                      # purchase this month
    # ensure active_date is AFTER purchase_date, within the same or later month window up to END_DATE
    active_dt = datetime.combine(purchase_date, datetime.min.time()) + relativedelta(days=random.randint(1, 30))
    if active_dt.date() < purchase_date:
        active_dt = active_dt + relativedelta(days=1)
    if active_dt > END_DATE:
        active_dt = END_DATE
    customers.append({
        'customer_id': next_customer_id(customer_idx),
        'industry': random.choice(INDUSTRIES),
        'region': random.choice(REGIONS),
        'account_tier': random.choice(ACCOUNT_TIERS),
        'contact_email': fake.company_email(),
        'domain': random.choice(POSSIBLE_DOMAINS),
        'purchase_date': purchase_date,
        'active_date': active_dt.date()  # reuse as signup date
    })

# First 8 customers are internal
internal_ids = set([c['customer_id'] for c in customers[:8]])

# Month-by-month: add new customers (scaled by seasonality); no churn
while month_cursor <= end_month_cursor:
    if month_cursor > datetime(START_DATE.year, START_DATE.month, 1):
        base_min, base_max = BASE_NEW_CUSTOMERS_MONTH
        scale = month_mult(month_cursor)
        add_n = max(0, int(random.randint(base_min, base_max) * scale))
        for _ in range(add_n):
            customer_idx += 1
            purchase_date = month_cursor.date()
            active_dt = month_cursor + relativedelta(days=random.randint(1, 30))
            if active_dt > END_DATE:
                active_dt = END_DATE
            customers.append({
                'customer_id': next_customer_id(customer_idx),
                'industry': random.choice(INDUSTRIES),
                'region': random.choice(REGIONS),
                'account_tier': random.choice(ACCOUNT_TIERS),
                'contact_email': fake.company_email(),
                'domain': random.choice(POSSIBLE_DOMAINS),
                'purchase_date': purchase_date,
                'active_date': active_dt.date()
            })
    month_cursor += relativedelta(months=1)

customer_info_df = pd.DataFrame(customers)
customer_info_df['is_internal'] = customer_info_df['customer_id'].isin(internal_ids)

# ----------------------- Sites (created at active_date) -----------------------
site_rows = []
seen_site_ids = set()
for _, c in customer_info_df.iterrows():
    num_sites = random.randint(*SITES_PER_CUSTOMER)
    for _ in range(num_sites):
        sid = gen_site_id()
        while sid in seen_site_ids:
            sid = gen_site_id()
        seen_site_ids.add(sid)
        site_rows.append({
            'customer_id': c['customer_id'],
            'site_id': sid,
            'active_date': c['active_date']  # site exists from active_date
        })
site_df = pd.DataFrame(site_rows)

# ----------------------- Users (post-active_date; assigned to each site) -----------------------
users_rows = []
for _, c in customer_info_df.iterrows():
    cid = c['customer_id']
    domain = c['domain']
    cust_sites = site_df.loc[site_df['customer_id'] == cid, 'site_id'].tolist()

    num_unique = random.randint(*USERS_PER_CUSTOMER)
    pool = []
    # registration_date cannot be before active_date
    start_reg = datetime.combine(pd.to_datetime(c['active_date']).date(), datetime.min.time())
    for _ in range(num_unique):
        uname = f"{fake.user_name()}{random.randint(0,9999)}"
        reg_date = fake.date_between(start_date=start_reg, end_date=END_DATE)
        pool.append({
            'customer_id': cid,
            'user_email': f"{uname}@{domain}",
            'registration_date': reg_date.strftime('%Y-%m-%d'),
            'license_type': random.choice(LICENSE_TYPES)
        })

    for sid in cust_sites:
        num_site_users = random.randint(1, len(pool))
        assigned = random.sample(pool, num_site_users)
        for u in assigned:
            users_rows.append({
                'customer_id': cid,
                'site_id': sid,
                'user_email': u['user_email'],
                'registration_date': u['registration_date'],
                'license_type': u['license_type']
            })
users_df = pd.DataFrame(users_rows)

# ----------------------- Active Check -----------------------
def is_customer_active_on(cid: str, day) -> bool:
    row = customer_info_df.loc[customer_info_df['customer_id'] == cid].iloc[0]
    a = pd.to_datetime(row['active_date']).date()
    return day >= a  # active from active_date onward (no churn)

# ----------------------- Storage (per site, per active day) -----------------------
storage_rows = []
for _, s in site_df.iterrows():
    cid, sid = s['customer_id'], s['site_id']
    for dt in DATE_RANGE:
        if not is_customer_active_on(cid, dt.date()):
            continue
        base = random.randint(*STORAGE_BYTES_RANGE)
        value = int(base * month_mult(dt) * daily_noise())
        storage_rows.append({
            'customer_id': cid,
            'site_id': sid,
            'date': dt.strftime('%Y-%m-%d'),
            'storage_bytes': max(value, 0)
        })
storage_df = pd.DataFrame(storage_rows)

# ----------------------- User Activity (aggregated) -----------------------
ua_rows = []
for _, s in site_df.iterrows():
    cid, sid = s['customer_id'], s['site_id']
    site_users = users_df[(users_df['customer_id'] == cid) & (users_df['site_id'] == sid)]['user_email'].tolist()
    for dt in DATE_RANGE:
        if not is_customer_active_on(cid, dt.date()):
            continue
        active_prob = min(1.0, max(0.0, USER_ACTIVE_PROB_BASE * month_mult(dt) * daily_noise(0.95, 1.05)))
        for email in site_users:
            if random.random() < active_prob:
                for _ in range(random.randint(*ACTIVITIES_PER_ACTIVE_DAY)):
                    ua_rows.append({
                        'customer_id': cid,
                        'user_email': email,
                        'site_id': sid,
                        'date': dt.strftime('%Y-%m-%d'),
                        'activity_type': random.choice(ACTIVITY_TYPES)
                    })
ua_df = pd.DataFrame(ua_rows)
if not ua_df.empty:
    activity_counts_df = ua_df.groupby(
        ['customer_id','user_email','site_id','date','activity_type'],
        as_index=False
    ).size().rename(columns={'size': 'event_count'})
else:
    activity_counts_df = pd.DataFrame(columns=['customer_id','user_email','site_id','date','activity_type','event_count'])

# ----------------------- Background Jobs (probabilistic) -----------------------
bj_rows = []
for _, s in site_df.iterrows():
    cid, sid = s['customer_id'], s['site_id']
    for dt in DATE_RANGE:
        if not is_customer_active_on(cid, dt.date()):
            continue
        weekday = dt.weekday()
        base_p = WEEKDAY_JOB_BASE_P if weekday < 5 else WEEKEND_JOB_BASE_P
        job_p = min(1.0, max(0.0, base_p * month_mult(dt) * daily_noise(0.95, 1.05)))
        if random.random() < job_p:
            for _ in range(random.randint(*JOBS_PER_JOB_DAY)):
                bj_rows.append({
                    'customer_id': cid,
                    'site_id': sid,
                    'date': dt.strftime('%Y-%m-%d'),
                    'background_job_type': random.choice(BACKGROUND_JOB_TYPES),
                    'background_job_min': random.randint(1, 80)
                })
background_job_df = pd.DataFrame(bj_rows)

# ----------------------- Write CSVs -----------------------
# Customer export includes purchase & active dates and internal flag
customer_export = customer_info_df[['customer_id','industry','region','account_tier','contact_email','is_internal',
                                    'purchase_date','active_date']].copy()

customer_export.to_csv('saas_customer_info.csv', index=False)
site_df[['customer_id','site_id']].to_csv('saas_sites.csv', index=False)
storage_df.to_csv('saas_storage.csv', index=False)
users_df.to_csv('saas_users.csv', index=False)
activity_counts_df.to_csv('saas_user_activity.csv', index=False)
background_job_df.to_csv('saas_background_jobs.csv', index=False)
