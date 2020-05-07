# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import csv
import datetime
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import pandas as pd


# %%
# https://catalog.data.metro.tokyo.lg.jp/dataset/t000010d0000000068
# 東京都 新型コロナウイルス陽性患者発表詳細
raw_log_url = 'https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv'
df_tokyo_log = pd.read_csv(raw_log_url, parse_dates=['公表_年月日'])
df_tokyo_log


# %%
df_by_gender = df_tokyo_log.groupby(['公表_年月日', '患者_性別']).count()[
    '都道府県名'].reset_index()
df_by_gender = df_by_gender.rename(
    columns={'公表_年月日': 'date', '患者_性別': 'gender', '都道府県名': 'count'})
df_by_gender = df_by_gender.pivot_table('count', 'date', 'gender').fillna(0)
df_by_gender = df_by_gender.rename(columns={'男性': 'M', '女性': 'F'})
df_by_gender


# %%
window = 7
title = "Daily confirmed number of positive patients by gender ({} day rolling ave)".format(
    window)
ax = df_by_gender[['M', 'F']].rolling(window).mean().plot(
    title=title, grid=True, cmap=plt.get_cmap("tab10"))
ax.legend(bbox_to_anchor=(0.05, 1), loc='upper left')
ax.xaxis.set_major_locator(mdates.MonthLocator())

reference_dates = pd.to_datetime([
    '2020-02-04',
    '2020-03-03',
    '2020-03-31',
    '2020-04-28'
])
plt.ylabel("Confirmed number of positive patients")
plt.vlines(reference_dates, 0, 100, "red", linestyles='dashed')
plt.savefig(os.path.join('plots', title))
# plt.show()


# %%
df_by_age = df_tokyo_log.groupby(['公表_年月日', '患者_年代']).count()[
    '都道府県名'].reset_index()
df_by_age = df_by_age.rename(
    columns={'公表_年月日': 'date', '患者_年代': 'age', '都道府県名': 'count'})
df_by_age = df_by_age.pivot_table('count', 'date', 'age').fillna(0)
df_by_age = df_by_age.rename(columns={
    '10代': '15',
    '20代': '20',
    '30代': '30',
    '40代': '40',
    '50代': '50',
    '60代': '60',
    '70代': '70',
    '80代': '80',
    '90代': '90',
    '100歳以上': '100',
})
# df_by_age['70'] = df_by_age.apply(lambda x: x['70'] + x['80'] + x['90'] + x['100'], axis=1)
df_by_age = df_by_age.drop(
    columns=['-', '10歳未満', '不明', '80', '90', '100'], axis=1)
df_by_age


# %%
title = "Daily confirmed number of positive patients by age ({} day rolling ave)".format(
    window)
ax = df_by_age.rolling(window).mean().plot(
    title=title, grid=True, cmap=plt.get_cmap("tab10"))
ax.legend(bbox_to_anchor=(0.05, 1), loc='upper left')
ax.xaxis.set_major_locator(mdates.MonthLocator())

plt.ylabel("Confirmed number of positive patients")
plt.vlines(reference_dates, 0, 30, "red", linestyles='dashed')
plt.savefig(os.path.join('plots', title))
# plt.show()


# %%
# TODO calcurate positive ratio by age class
# https://www.toukei.metro.tokyo.lg.jp/dyosoku/dy-data.htm
# https://www.toukei.metro.tokyo.lg.jp/dyosoku/dy17ra0901.xls
