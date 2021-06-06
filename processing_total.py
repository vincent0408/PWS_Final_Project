import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
HW_NO = 6

def get_df(i):  # 第幾次作業的df(刪除第一次ac後的資料)
  # Step1. 讀入資料&加入欄位
  raw_data = pd.read_csv('C:/Users/Vincent/Desktop/PWS Homework/PWS Homework {}.csv'.format(i), header=None, parse_dates = [0])
  raw_data.columns = ['When', 'ID', 'Status', 'Problem', 'Time', 'Memory', 'Language', 'Author', 'HW']
  raw_data.sort_values("When", ascending=True, inplace=True)
  raw_data['Problem'] = raw_data['Problem'].astype(str)
  raw_data['Problem Code'] = 'HW' + raw_data['HW'].str.get(-1) + '-' + raw_data['Problem'].str.get(-1)
  # Step2. 刪去AC後的Submission
  data_list = raw_data.values.tolist()
  ac_list = []
  df_list = []
  for data in data_list:
    if [data[9], data[7]] not in ac_list:  # 這題還沒AC過
      df_list.append(data)
      if data[2] == "Accepted":  # 代表這題AC過了，之後的繳交資料都會刪掉
        ac_list.append([data[9], data[7]])
  # Step3. 將List轉成pandas dataframe
  df = pd.DataFrame.from_dict(df_list)
  df.columns = ['When', 'ID', 'Status', 'Problem', 'Time', 'Memory', 'Language', 'Author', 'HW', 'Problem Code']
  df = df[~df['Author'].isin(['b06302345@ntu.edu.tw', 'hyusterr', 'jeffery12697', 'yeutong00'])]
  df.set_index('ID', inplace=True)
  return df

def get_ac_df(df):
  ac_df = df[df['Status'] == "Accepted"]
  return ac_df

def get_first_df(df):
  first_df = df.drop_duplicates(subset=['Problem Code', 'Author'])
  return first_df

def get_whole_data(target_dfs):  # 得到哪種資料、幾次作業
  return pd.concat([target_dfs[i] for i in range(1, HW_NO+1)], ignore_index=False)

def get_dfs():
    dfs = [None]  # 1~6分別裝每次作業的df
    ac_dfs = [None]  # 1~6分別裝每次作業的ac_df
    first_dfs = [None]  # 1~6分別裝每次作業的first_df

    for i in range(1, HW_NO + 1):  
        hw_i = get_df(i)
        dfs.append(hw_i)
        ac_dfs.append(get_ac_df(hw_i))
        first_dfs.append(get_first_df(hw_i))
        
    return dfs, ac_dfs, first_dfs

dfs, ac_dfs, first_dfs = get_dfs()

df = get_whole_data(dfs)
ac_df = get_whole_data(ac_dfs)
first_df = get_whole_data(first_dfs)


def get_status():
  HW_Status = pd.crosstab(df['Status'], df['HW']).reset_index()
  Problem_Status = pd.crosstab(df['Status'], df['Problem Code']).reset_index()
  Status_df = HW_Status.merge(Problem_Status, on='Status')
  Status_df.set_index('Status', inplace=True)
  Status_df.index.name = None
  return Status_df

def get_time_data(df, time='hour'):
  # get_time_data(df)  # 總作業得到幾點的資料
  # get_time_data(dfs[1], 'date')  # 第一次作業幾月幾號的資料
  if time == 'hour':
    df = pd.crosstab(df['When'].dt.hour, df['Status'])
  elif time == 'date':
    df = pd.crosstab(df['When'].dt.date, df['Status'])
  df['Submission'] = df.sum(axis=1)
  df['Wrong Answer'] = df['Submission'] - df['Accepted']
  df['AC Rate'] = df['Accepted'] / (df['Wrong Answer'] + df['Accepted'])
  df = df.loc[:,['Accepted', 'Wrong Answer', 'Submission', 'AC Rate']]
  df.reset_index(inplace=True)
  df.columns.name = None
  df.set_index('When', inplace=True)
  df.index.name = None
  return df

def get_date_data():
  date_data_list = [None]
  for n in range(1, HW_NO + 1):
    date_data_list.append(get_time_data(dfs[n], 'date'))
  date_merge = date_data_list[1].merge(date_data_list[2], on='When', suffixes=('_HW1','_HW2'), how='outer')
  date_merge = date_merge.merge(date_data_list[3], on='When', how='outer')
  date_merge = date_merge.merge(date_data_list[4], on='When', suffixes=('_HW3','_HW4'), how='outer')
  date_merge = date_merge.merge(date_data_list[5], on='When', how='outer')
  date_merge = date_merge.merge(date_data_list[6], on='When', suffixes=('_HW5','_HW6'), how='outer')
  date_merge = date_merge.fillna(-1)
  date_merge['When'] = date_merge['When'].apply(lambda x: str(x))
  date_merge.columns.name = None
  date_merge = date_merge.T
  date_merge.columns = date_merge.iloc[0]
  date_merge = date_merge[1:]
  date_merge.columns.name = None
  return date_merge.T

def get_ac_num():
  ac_date = [None]
  for i in range(1, HW_NO + 1):
    ac_date.append(pd.crosstab(ac_dfs[i]['When'].dt.date, ac_dfs[i]['Problem Code']).cumsum())
  date_merge = ac_date[1].merge(ac_date[2], on='When', how='outer')  
  for a in range(3, HW_NO + 1):
    date_merge = date_merge.merge(ac_date[a], on='When', how='outer')
  date_merge = date_merge.reset_index()
  date_merge = date_merge.fillna(-1)
  date_merge.iloc[35, 6:11] = date_merge.iloc[33, 6:11]
  date_merge.columns.name = None  
  date_merge['When'] = date_merge['When'].apply(lambda x:str(x))
  date_merge.set_index('When', inplace=True) 
  date_merge.index.name = None
  return date_merge



