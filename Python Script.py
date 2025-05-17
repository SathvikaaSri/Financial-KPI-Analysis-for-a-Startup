import pandas as pd


file_path = 'C:/Users/Sathvikaa Sri Kumar/Downloads/Spotify Quarterly.csv'
df = pd.read_csv(file_path)
print(df)
print("\n" + "="*50 + "\n")

 
df = df.rename(columns={
     'Date': 'Quarter',
     'Total Revenue': 'Total Revenue (EUR Millions)',
     'Cost of Revenue': 'Cost of Revenue (EUR Millions)',
     'Premium Revenue': 'Premium Revenue (EUR Millions)',
     'Ad Revenue': 'Ad Revenue (EUR Millions)' ,
     'Premium MAUs': 'Premium MAUs (Millions)',
     'Ad MAUs': 'Ad MAUs (Millions)'
 })

 
eur_to_usd = 1.12

 
df['Total Revenue (USD Millions)'] = df['Total Revenue (EUR Millions)'] * eur_to_usd
df['Cost of Revenue (USD Millions)'] = df['Cost of Revenue (EUR Millions)'] * eur_to_usd
df['Premium Revenue (USD Millions)'] = df['Premium Revenue (EUR Millions)'] * eur_to_usd
df['Ad Revenue (USD Millions)'] = df['Ad Revenue (EUR Millions)'] * eur_to_usd

 
df['Total MAUs (Millions)'] = df['Premium MAUs (Millions)'] + df['Ad MAUs (Millions)']

df['New Premium Subscribers (Millions)'] = df['Premium MAUs (Millions)'].diff().fillna(df['Premium MAUs (Millions)'].iloc[0])

 
months_per_quarter = 3
df['Monthly Revenue (USD Millions)'] = df['Total Revenue (USD Millions)'] / months_per_quarter
df['Monthly Cost of Revenue (USD Millions)'] = df['Cost of Revenue (USD Millions)'] / months_per_quarter

 
marketing_sales_proportion = 0.3  
df['Marketing & Sales Expenses (USD Millions)'] = df['Monthly Cost of Revenue (USD Millions)'] * marketing_sales_proportion

 
df['CAC (USD)'] = (df['Marketing & Sales Expenses (USD Millions)'] * 1000000) / (df['New Premium Subscribers (Millions)'] * 1000000)

 
df['ARPU (USD/Month)'] = (df['Monthly Revenue (USD Millions)'] * 1000000) / (df['Total MAUs (Millions)'] * 1000000)

 
df['Previous Quarter Premium MAUs'] = df['Premium MAUs (Millions)'].shift(1).fillna(df['Premium MAUs (Millions)'].iloc[0])
df['Estimated Churn (Millions)'] = df['Previous Quarter Premium MAUs'] - (df['Premium MAUs (Millions)'] - df['New Premium Subscribers (Millions)'])
df['Monthly Churn Rate'] = df['Estimated Churn (Millions)'] / df['Previous Quarter Premium MAUs'] / months_per_quarter
df.loc[df['Monthly Churn Rate'] < 0, 'Monthly Churn Rate'] = 0

 
df['Customer Lifetime (Months)'] = 1 / df['Monthly Churn Rate']
df.replace([float('inf'), float('-inf')], 0, inplace=True)

df['LTV (USD)'] = df['ARPU (USD/Month)'] * df['Customer Lifetime (Months)']

 
df['LTV:CAC Ratio'] = df['LTV (USD)'] / df['CAC (USD)']
df.replace([float('inf'), float('-inf')], 0, inplace=True)

 
df['Monthly Burn Rate (USD Millions)'] = df['Monthly Cost of Revenue (USD Millions)']
df['Net Monthly Burn Rate (USD Millions)'] = df['Monthly Burn Rate (USD Millions)'] - df['Monthly Revenue (USD Millions)']

 
last_month_revenue = df['Monthly Revenue (USD Millions)'].iloc[-1]
annual_revenue_run_rate = last_month_revenue * 12
last_month_expenses = df['Monthly Burn Rate (USD Millions)'].iloc[-1]
annual_expense_run_rate = last_month_expenses * 12

print("\nCalculated Metrics:")
print(df)
print("\n" + "="*50 + "\n")
print(f"Annual Revenue Run Rate (based on latest quarter): ${annual_revenue_run_rate:.2f} Million")
print(f"Annual Expense Run Rate (based on latest quarter): ${annual_expense_run_rate:.2f} Million")


print("\nKey Metrics Summary:")
print(f"  Latest LTV:CAC Ratio: {df['LTV:CAC Ratio'].iloc[-1]:.2f}")
print(f"  Latest Monthly Burn Rate: ${df['Monthly Burn Rate (USD Millions)'].iloc[-1]:.2f} Million")
print(f"  Latest Net Monthly Burn Rate: ${df['Net Monthly Burn Rate (USD Millions)'].iloc[-1]:.2f} Million")
print(f"  Annual Revenue Run Rate: ${annual_revenue_run_rate:.2f} Million")
print(f"  Annual Expense Run Rate: ${annual_expense_run_rate:.2f} Million")

 
