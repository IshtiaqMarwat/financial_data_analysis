# Financial Data Analysis using Python
### To understand the characteristics of customers who accepted personal loans and to identify patterns that can help the bank convert more liability customers into personal loan customers
## Table of Contents

1. [About](#about)
2. [Purpose of Project](#purpose-of-project)
3. [About Data](#about-data)
4. [Questions Answered](#questions-answered)
5. [Summary of Findings](#summary-of-findings)
6. [Python Code](#python-code)
7. [Conclusion](#conclusion)

## About
This project involves analyzing bank customer data using Python to gain insights into customer demographics, relationships with the bank, and their responses to personal loan campaigns. The analysis aims to inform targeted marketing strategies to increase the success rate of future loan campaigns.

## Purpose of Project
The primary goal of this project is to understand the characteristics of customers who accepted personal loans and to identify patterns that can help the bank convert more liability customers into personal loan customers. By analyzing this data, the project addresses questions related to customer demographics, account holdings, and campaign responses. The insights derived will guide the marketing department in crafting more effective campaigns with optimized targeting and minimal budget expenditure.

## About Data
The dataset used in this analysis contains information on 5000 customers, including:
- Customer demographics: age, income, etc.
- Customer relationship with the bank: mortgage, securities account, etc.
- Customer response to the last personal loan campaign: accepted or not.

## Data Fields

| Field               | Type |
|---------------------|------|
| Age                 | int  |
| Experience          | int  |
| Income              | int  |
| Family              | int  |
| Education           | int  |
| Mortgage            | int  |
| Securities Account  | int  |
| CD Account          | int  |
| Online              | int  |
| CreditCard          | int  |
| Personal Loan       | int  |


## Questions Answered
- What are the demographic characteristics of customers who accepted personal loans?
- What is the income distribution among customers with and without personal loans?
- How does account holding (securities, CD accounts) relate to personal loan acceptance?
- What is the effect of customer demographics on personal loan acceptance?
- How do online banking and credit card usage influence personal loan decisions?

## Summary of Findings
- A small percentage (9.6%) of customers accepted the personal loan.
- Higher income and educational levels correlate with higher acceptance rates.
- Customers with securities and CD accounts are more likely to accept personal loans.
- The majority of personal loan acceptors are middle-aged with substantial banking relationships.
- Marketing efforts can be fine-tuned to target specific customer segments more effectively.


## Python Code
```python
# Importing essential libraries for data analysis and visualization
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Reading the data from an Excel file into a DataFrame
df = pd.read_excel('Bank_Personal_Loan_Modelling.xlsx')

# Initial data exploration
print(df.head())
print(df.shape)
print(df.isnull().sum())
print(df.columns)

# Data cleaning and transformation
df.drop(['ID', 'ZIP Code'], axis=1, inplace=True)
print(df.columns)

# Visualization
fig = px.box(df, y=['Age', 'Experience', 'Income', 'Family', 'Education'])
fig.show()

# Data analysis
print(df.dtypes)
print(df.skew())
df.hist(figsize=(20, 20))
sns.distplot(df['Experience'])
print(df['Experience'].mean())

# Handling negative 'Experience' values
data = df.copy()
data['Experience'] = np.where(data['Experience'] < 0, 
                              data['Experience'].mean(), 
                              data['Experience'])

# Correlation analysis
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True)

# Transforming 'Education' column
data['Edu'] = data['Education'].apply(lambda x: 'Undergrad' if x == 1 else 'Graduate' if x == 2 else 'Professional')

# Visualizations
fig = px.pie(data, names='Edu', title='Distribution of Education Levels')
fig.show()

# Account holder categories
data['Account_Holder_Cat'] = data.apply(
    lambda y: 'Holds Security and Deposit Account' if (y['Securities Account'] == 1) & (y['CD Account'] == 1)
    else 'No Security and Deposit Account' if (y['Securities Account'] == 0) & (y['CD Account'] == 0)
    else 'Holds Security But No Deposit Account' if (y['Securities Account'] == 1) & (y['CD Account'] == 0)
    else 'No Security Account but holds Deposit Account', axis=1
)
fig = px.pie(data, names='Account_Holder_Cat', title='Account Holders Categories')
fig.show()

# Income and loan analysis
sns.distplot(data[data['Personal Loan'] == 0]['Income'], hist=False, label='Income without Personal Loan')
sns.distplot(data[data['Personal Loan'] == 1]['Income'], hist=False, label='Income with Personal Loan')
plt.legend()

# Further analysis
def plot_distribution(col1, col2, label1, label2, title):
    sns.distplot(data[data[col2] == 0][col1], hist=False, label=label1)
    sns.distplot(data[data[col2] == 1][col1], hist=False, label=label2)
    plt.legend()
    plt.title(title)

plot_distribution('Income', 'Personal Loan', 'Income without Personal Loan', 'Income with Personal Loan', 'Income vs Personal Loan')
plot_distribution('CCAvg', 'Personal Loan', 'Credit Card avg with no personal loan', 'Credit Card avg with Personal loan', 'Credit Card Avg distribution')

# Count plots for categorical features
for feature in ['Securities Account', 'Online', 'Account_Holder_Cat', 'CreditCard']:
    plt.figure(figsize=(10, 6))
    sns.countplot(x=feature, data=data, hue='Personal Loan')

# Handling skewness using Power Transformer
from sklearn.preprocessing import PowerTransformer
pt = PowerTransformer(method='yeo-johnson', standardize=False)
data['Income'] = pt.fit_transform(data['Income'].values.reshape(-1, 1))

sns.distplot(data['Income'])
plt.show()

With this closing line, the rest of the text can be formatted in its own style.

## Conclusion
This project provides insights into customer behavior regarding personal loans, highlighting the importance of demographic and financial characteristics. By understanding these patterns, the bank can design more effective marketing strategies, targeting the right customer segments to maximize loan acceptance rates while retaining existing customers.
