import numpy as np
import pandas as pd

# import data
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
politics = president_income[['year','state','state_po', 'state_fips', 'state_cen', 'state_ic', 'office','candidate', 'party', 'writein', 'candidatevotes', 'totalvotes', 'version',
 'notes', 'State']].copy()


median = median.reset_index()
error = error.reset_index()

# Merge Median Income and Standard Error columns into main dataframe
income_politics_table = politics.merge(median, on=['year','state'], how='outer')
income_politics_table = income_politics_table.merge(error, on=['year','state'], how='outer')

print(income_politics_table.reset_index()[income_politics_table['year']==2000])