#!/usr/bin/env python
# coding: utf-8

# # Finance Project

# - **Data Description:** The file Bank.xls contains data on 5000 customers. The data include customer demographic information (age, income, etc.), the customer's relationship with the bank (mortgage, securities account, etc.), and the customer response to the last personal loan campaign (Personal Loan). Among these 5000 customers, only 480 (= 9.6%) accepted the personal loan that was offered to them in the earlier campaign.
# - **Context:** This case is about a bank (Thera Bank) whose management wants to explore ways of converting its liability customers to personal loan customers (while retaining them as depositors). A campaign that the bank ran last year for liability customers showed a healthy conversion rate of over 9% success. This has encouraged the retail marketing department to devise campaigns with better target marketing to increase the success ratio with minimal budget.

# In[ ]:


# Importing essential libraries for data analysis and visualization
import pandas as pd  # Data manipulation and analysis
import numpy as np  # Numerical operations and array handling
import seaborn as sns  # Statistical data visualization
import matplotlib.pyplot as plt  # Plotting and visualization

# Reading the data from an Excel file into a DataFrame
df = pd.read_excel('Bank_Personal_Loan_Modelling.xlsx')

# Displaying the first few rows of the DataFrame to check the data
df.head()

# Checking the dimensions of the DataFrame (rows, columns)
df.shape

# Counting the number of missing values in each column
df.isnull().sum()

# Listing all column names in the DataFrame
df.columns

# Dropping the 'ID' and 'ZIP Code' columns from the DataFrame
df.drop(['ID', 'ZIP Code'], axis=1, inplace=True)

# Listing all column names in the DataFrame
df.columns

# Importing Plotly Express for creating interactive visualizations
import plotly.express as px

# Generating a box plot to get the summary for 5 specified columns
fig = px.box(df, y=['Age', 'Experience', 'Income', 'Family', 'Education'])

# Displaying the box plot
fig.show()

# Checking the data types of each column in the DataFrame
df.dtypes


# Calculating the skewness for each numerical column in the DataFrame
df.skew()

# Generating histograms for each numerical column in the DataFrame
df.hist(figsize=(20, 20))

# Creating a distribution plot for the 'Experience' column using Seaborn
sns.distplot(df['Experience'])

# Calculating the mean of the 'Experience' column
df['Experience'].mean()

# Filtering rows where 'Experience' is negative
neg_experience = df[df['Experience'] < 0]
neg_experience

# Checking the dimensions of the DataFrame containing negative 'Experience' values
neg_experience.shape

# Creating a distribution plot for the 'Age' column in the subset with negative 'Experience' values using Seaborn
sns.distplot(neg_experience['Age'])

# Calculating the mean of the 'Experience' column in the subset with negative 'Experience' values
neg_experience['Experience'].mean()

# Calculating the total number of elements in the DataFrame containing negative 'Experience' values
neg_experience.size

# Printing the number of records with negative 'Experience' values as a percentage of the total DataFrame size
print('There are {} records which have negative values for experience, approximately {:.2f}%'.format(neg_experience.size, (neg_experience.size / df.size) * 100))

# Creating a copy of the DataFrame to retain the original data integrity
data = df.copy()

# Displaying the first few rows of the copied DataFrame
data.head()

data.dtypes
data.shape

# Handling negative 'Experience' values by replacing them with the mean of non-negative values
data['Experience'] = np.where(data['Experience'] < 0, 
                              data['Experience'].mean(), 
                              data['Experience'])

# Checking for any remaining negative values in the 'Experience' column after handling
data[data['Experience'] < 0]

# Calculating the correlation matrix for all numerical columns in the DataFrame
data.corr()

# Visualizing the correlation matrix using a heatmap with annotations
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True)

# Dropping the 'Experience' column from the DataFrame
data = data.drop(['Experience'], axis=1)

# Displaying the first few rows of the updated DataFrame
data.head()
data.shape

# Checking the unique values in the 'Education' column
data['Education'].unique()

# Defining a function to categorize education levels based on numerical codes
def experience(x):
    if x == 1:
        return 'Undergrad'
    if x == 2:
        return 'Graduate'
    if x == 3:
        return 'Professional'

# Applying the 'experience' function to create a new column 'Edu' based on education levels
data['Edu'] = data['Education'].apply(experience)

data.head()

# Checking the unique values in the newly created 'Edu' column
data['Edu'].unique()

# Calculating the distribution of education levels based on the 'Edu' column
education_dist = data.groupby('Edu')['Age'].count()

# Creating a pie chart to visualize the distribution of education levels
fig = ps.pie(data, values=education_dist, names=education_dist.index, title='Pie Chart to distribute Education')

# Displaying the pie chart
fig.show()

data.columns

# Checking the unique values in the 'Income' & Securities Account column
data['Income'].unique()
data['Securities Account'].unique()

# Counting the number of occurrences of each value in the 'Securities Account' column
data['Securities Account'].value_counts()


# Counting the number of occurrences of each value in the 'CD Account' column
data['CD Account'].value_counts()

# Defining a function to categorize account holder categories based on 'Securities Account' and 'CD Account'
def security(y):
    if (y['Securities Account'] == 1) & (y['CD Account'] == 1):
        return 'Holds Security and Deposit Account'
    if (y['Securities Account'] == 0) & (y['CD Account'] == 0):
        return 'No Security and Deposit Account'
    if (y['Securities Account'] == 1) & (y['CD Account'] == 0):
        return 'Holds Security But No Deposit Account'
    if (y['Securities Account'] == 0) & (y['CD Account'] == 1):
        return 'No Security Account but holds Deposit Account'

# Applying the function to create a new column 'Account_Holder_Cat' based on account holder categories
data['Account_Holder_Cat'] = data.apply(security, axis=1)

# Generating counts for each category in the 'Account_Holder_Cat' column
account_hold_dis = data.groupby('Account_Holder_Cat')['Securities Account'].count()

# Creating a pie chart to visualize the distribution of account holder categories
fig = ps.pie(data, values=account_hold_dis, names=account_hold_dis.index, title='Pie chart - Account Holders Categories')
fig.show()

# Listing column names in the DataFrame
data.columns

# Creating box plots of 'Income' vs 'Personal Loan' faceted by 'Education'
ps.box(data, x='Edu', y='Income', facet_col='Personal Loan')

# Creating distribution plots of 'Income' with and without 'Personal Loan'
sns.distplot(data[data['Personal Loan'] == 0]['Income'], hist=False, label='Income without Personal Loan')
sns.distplot(data[data['Personal Loan'] == 1]['Income'], hist=False, label='Income with Personal Loan')
plt.legend()

# Defining a function to plot distributions of two columns based on a target column
def plot(col1, col2, label1, label2, title):
    sns.distplot(data[data[col2] == 0][col1], hist=False, label=label1)
    sns.distplot(data[data[col2] == 1][col1], hist=False, label=label2)
    plt.legend()
    plt.title(title)

# Plotting distribution of 'Income' vs 'Personal Loan'
plot('Income', 'Personal Loan', 'Income without Personal Loan', 'Income with Personal Loan', 'Income vs Personal Loan')

# Plotting distribution of 'CCAvg' vs 'Personal Loan'
plot('CCAvg', 'Personal Loan', 'Credit Card avg with no personal loan', 'Credit Card avg with Personal loan', 'Credit Card Avg distribution')

# Listing column names in the DataFrame
data.columns

# Plotting count plots for selected columns faceted by 'Personal Loan' status
col = ['Securities Account', 'Online', 'Account_Holder_Cat', 'CreditCard']
for i in col:
    plt.figure(figsize=(10, 6))
    sns.countplot(x=i, data=data, hue='Personal Loan')

# Data handling - to handle skewness
from scipy.stats import zscore

# Displaying data types of columns in the DataFrame
data.dtypes

# Selecting numerical columns
numeric_data = data.select_dtypes(include='number')

# Calculating interquartile range (IQR) for numerical columns
q1 = numeric_data.quantile(0.25)
q3 = numeric_data.quantile(0.75)
IQR = q3 - q1
print(IQR)

# Log Normal Transformation for selected columns
data_1 = data[['Income', 'CCAvg']]
data_1 = np.log(data_1 + 1)

# Power Transformer for 'Income'
from sklearn.preprocessing import PowerTransformer

pt = PowerTransformer(method='yeo-johnson', standardize=False)
pt.fit(data['Income'].values.reshape(-1, 1))
Income = pt.transform(data['Income'].values.reshape(-1, 1))
sns.distplot(Income)
plt.show()

