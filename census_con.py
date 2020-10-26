import numpy as np
import pandas as pd
import psycopg2

income = pd.read_excel("Census_median_income_1984_2019.ods", engine="odf")
income_t = income.T
president = pd.read_csv("1976-2016-president.csv")


conn = psycopg2.connect("dbname=income user=wbeedle")
cur = conn.cursor

president_income_t = income.merge(president, left_on='state')

print(president_income_t.head())