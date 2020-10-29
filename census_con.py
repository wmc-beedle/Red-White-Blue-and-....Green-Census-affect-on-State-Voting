import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


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
# income_politics_table.to_excel('Income_vs_Politics.xlsx')
# income_politics_table = income_politics_table.reset_index().set_index(['year','state'])
# cali_mi_win_party = median_income_state[median_income_state.index >= 1984]

ipt = income_politics_table
fig, ax = plt.subplots()

for state in pd.unique(ipt['state']):
    #Median Income by State between 1984 and 2016
    ipt_state = ipt[ipt['state']==state]
    ipt_state = ipt_state[ipt_state['year'] >= 1984]
    ipt_state.groupby(['year']).mean()['Median Income']

    #Winner Table
    max_v = ipt_state.groupby('year')['candidatevotes'].transform(func=max)
    ipt_state.groupby(['year'])

    #Winner of each State
    state_winning_party = ipt_state[ipt_state['candidatevotes']==max_v]
    median_income_state = state_winning_party.groupby('year').mean()['Median Income']

    #Political Party Plotting
    democrat = state_winning_party[state_winning_party['party'] == 'democrat']
    democrat_median_income = democrat['Median Income']
    republican = state_winning_party[state_winning_party['party'] == 'republican']
    republican_median_income = republican['Median Income']

    ax.scatter(democrat.iloc[:,0],democrat_median_income,c='blue')
    ax.scatter(republican.iloc[:,0],republican_median_income,c='red')



red_patch = mpatches.Patch(color='red', label='Republican Won State')
blue_patch = mpatches.Patch(color='blue', label='Democrat Won State')

plt.legend(handles=[red_patch, blue_patch], loc='best')

ax.set_title("States' Political Preference over Time compared to Median Household Income")
ax.set_xlabel("Year")
ax.set_ylabel("Median Income")
plt.show()

