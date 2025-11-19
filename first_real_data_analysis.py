import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime 
df = pd.read_csv('/content/sample_data/matched_dataset.csv')
print("Data Shape :",df.shape)
print("\nColumns:", df.columns.tolist())


df['TRAN_DATE'] = pd.to_datetime(df['TRAN_DATE'], format='%d/%m/%Y')

df['TRAN_AMT'] = pd.to_numeric(df['TRAN_AMT'], errors='coerce')

df['MONTH'] = df['TRAN_DATE'].dt.month

df['DAY'] = df['TRAN_DATE'].dt.day

df['DAY_NAME'] = df['TRAN_DATE'].dt.day_name()

df['WEEK'] = df['TRAN_DATE'].dt.isocalendar().week


print(f"Date range: {df['TRAN_DATE'].min()} to {df['TRAN_DATE'].max()}")
print(f"Total transactions: {len(df)}") 
print(f"Total amount: GHS {df['TRAN_AMT'].sum():,.2f}")  


print("=== SUMMARY STATISTICS ===")
print(df[['TRAN_AMT']].describe())  


print("\n=== TRANSACTION CATEGORIES ===")
print(df['Transaction_Category'].value_counts())

print("\n=== DEBIT vs CREDIT ===")
print(df['PART_TRAN_TYPE'].value_counts())

print("\n=== TRANSACTION TYPES ===")
print(df['RPT_CODE'].value_counts())





plt.rcParams['figure.figsize'] = [12, 8]  
plt.rcParams['font.size'] = 10  


fig, axes = plt.subplots(2, 2, figsize=(15, 12))



category_counts = df['Transaction_Category'].value_counts().head(10)


axes[0,0].barh(range(len(category_counts)), category_counts.values)


axes[0,0].set_yticks(range(len(category_counts)))
axes[0,0].set_yticklabels(category_counts.index)

axes[0,0].set_title('Top 10 Transaction Categories (by Count)')
axes[0,0].set_xlabel('Number of Transactions')

for i, v in enumerate(category_counts.values):
    axes[0,0].text(v + 3, i, str(v), va='center')

category_amounts = df.groupby('Transaction_Category')['TRAN_AMT'].sum()
category_amounts = category_amounts.sort_values(ascending=False).head(10)

axes[0,1].barh(range(len(category_amounts)), category_amounts.values)
axes[0,1].set_yticks(range(len(category_amounts)))
axes[0,1].set_yticklabels(category_amounts.index)
axes[0,1].set_title('Top 10 Transaction Categories (by Amount)')
axes[0,1].set_xlabel('Total Amount')

for i, v in enumerate(category_amounts.values):
    axes[0,1].text(v + 1000, i, f'GHS{v:,.0f}', va='center')


daily_counts = df.groupby('TRAN_DATE').size()


axes[1,0].plot(daily_counts.index, daily_counts.values, marker='o', linewidth=2)
axes[1,0].set_title('Daily Transaction Volume')
axes[1,0].set_xlabel('Date')
axes[1,0].set_ylabel('Number of Transactions')
axes[1,0].tick_params(axis='x', rotation=45)

debit_credit = df['PART_TRAN_TYPE'].value_counts()
axes[1,1].pie(debit_credit.values, labels=debit_credit.index, autopct='%1.1f%%', startangle=90)
axes[1,1].set_title('Debit vs Credit Transactions')

plt.tight_layout() 
plt.show() 
