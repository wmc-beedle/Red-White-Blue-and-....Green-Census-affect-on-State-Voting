import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# Import data
income = pd.read_excel('Census_median_income_1984_2019.ods', engine='odf',header=[59])
president = pd.read_csv('1976-2016-president.csv')

# Merge and reset index to create main dataframe
president_income = president.merge(income, left_on='state', right_on='State', how='left')
president_income = president_income.reset_index().set_index(['year','state'])

# Isolate [year] Median Income and [year] Standard Error data
median_col = income.columns.str.contains('Median')
Median_Income = income.iloc[:,median_col]
error_col = income.columns.str.contains('Error')
Standard_Error = income.iloc[:,error_col]

# Change Median and Error data to have 'State', 'year', and Median/Error in specified columns
median = pd.melt(income, id_vars='State',value_vars=income.columns[median_col],var_name='year')
error = pd.melt(income, id_vars='State',value_vars=income.columns[error_col],var_name='year')

# Edit column names to match data change above
median['year'] = median['year'].str.replace('Median Income','')
median = median.rename(columns = {'value':'Median Income'})
error['year'] = error['year'].str.replace('Standard Error','')
error = error.rename(columns = {'value':'Standard Error'})

#Edit 'State' to match 'state' in main dataframe
median = median.rename(columns = {'State':'state'})
error = error.rename(columns = {'State':'state'})

median['year'] = pd.to_numeric(median['year'])
error['year'] = pd.to_numeric(median['year'])

median = median.set_index(['year','state'])
error = error.set_index(['year','state'])

president_income = president_income.reset_index()
politics = president_income[['year','state','office','candidate', 'party', 'writein', 'candidatevotes', 'totalvotes']].copy()


median = median.reset_index()
error = error.reset_index()

# Merge Median Income and Standard Error columns into main dataframe
income_politics_table = politics.merge(median, on=['year','state'], how='outer')
income_politics_table = income_politics_table.merge(error, on=['year','state'], how='outer')

# state_list = president['state']

#income_politics_table.to_excel('Income_vs_Politics.xlsx')
# income_politics_table = income_politics_table.reset_index().set_index(['year','state'])


ipt = income_politics_table

ipt_c = ipt[ipt['state']=='California']
ipt_c =ipt_c[ipt_c['year'] >= 1984]
mi = ipt_c.groupby(['year']).mean()['Median Income']


max_v = ipt_c.groupby('year')['candidatevotes'].transform(func=max)
ipt_c.groupby(['year'])


cali_win_party = ipt_c[ipt_c['candidatevotes']==max_v]
mi_c = cali_win_party.groupby('year').mean()['Median Income']
cali_mi_win_party = mi_c[mi_c.index >= 1984]
cali_democrat = cali_win_party[cali_win_party['party'] == 'democrat']
cdi = cali_democrat['Median Income']
cali_republican = cali_win_party[cali_win_party['party'] == 'republican']
cri = cali_republican['Median Income']

fig, ax = plt.subplots()
ax.set_title("Median Income over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Median Income")


ax.scatter(cali_democrat.iloc[:,0],cdi,c='blue',label='democrat')
ax.scatter(cali_republican.iloc[:,0],cri,c='red',label='republican')


ax.legend(loc='best')
plt.show()

