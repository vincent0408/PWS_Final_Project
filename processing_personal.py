#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os



def importdata():
    path = r'C:/Users/Vincent/Desktop/PWS Homework//'
    df = pd.DataFrame()
    for filename in os.listdir(path):
        hw = pd.read_csv(path + filename, header=None)
        df = pd.concat([df, hw])
    df.columns = ["When", "ID", "Status", "Problem", "Time", "Memory", "Language", "Author", "HW"]
    df.set_index('When', inplace=True)
    
    df['Problem'] = df['Problem'].astype(str)
    df['Problem Code'] = 'HW' + df['HW'].str.get(-1) + '-' + df['Problem'].str.get(-1)
    
    df = df.reset_index()
    df.When = df.When.apply(pd.to_datetime)
    df = df.sort_values(by = 'When')

    return df

def del_invalid(df):
    output = pd.DataFrame()
    for stu in df.Author.unique():
        student = df.loc[df.Author == stu]
        for p in student['Problem Code'].unique():
            student_problem = student.loc[student['Problem Code'] == p]
            for d in student_problem.index:
                if df.Status[d] == 'Accepted':
                    output = output.append(student_problem.loc[d])
                    break
                else:
                    output = output.append(student_problem.loc[d])
    output = output.loc[~output.Author.isin(['hyusterr', 'yeutong00', 'jeffery12697'])]
    return output

def get_dataframe():
    df = importdata()
    df = del_invalid(df)
    df = df.reset_index().drop('index', axis = 1)
    return df

df = get_dataframe()

def adj_PAC(select, adj_minute):
    #調整 PAC 嘗試次數: 假說: 高頻率的測試 多為測試測資 不希望影響我們對實際作答狀況評估
    if len(select) == 0:
        return select
    else:
        time_since_lx_PAC = [dt.timedelta(minutes = 0)]

        for i in range(1, len(select)):
            tmp = select.When.iloc[i] - select.When.iloc[i-1]
            time_since_lx_PAC.append(tmp)

        select.loc[:, 'timegap'] = time_since_lx_PAC
        return select.loc[(select.timegap > adj_minute) | (select.timegap == time_since_lx_PAC[0])]
    
    return select.loc[(select.timegap > adj_minute) | (select.timegap == time_since_lx_PAC[0])]

def sorted_columns(df, timegap):
    columns = list()
    for p in sorted(df['Problem Code'].unique()):
        for rate in [' AC rate_', ' PAC rate_', ' WA rate_', ' Other rate_', ' Submit count_']:
            for t in timegap:
                columns.append(p + rate + str(t))
    return columns

def get_rates(df):
    author = df.Author.unique(); problem_code = df['Problem Code'].unique()
    AnswerRate = pd.DataFrame(author, columns = ['Author'])
    timegap = [0,3,5,15]
    
    #計算每一題內每個學生之答對率、部分答對率、答錯率
    for adj_minute in timegap:
        for P in problem_code:
            case = df.loc[df['Problem Code'] == P]
            AC, PAC, WA, Other, Submit = [],[],[],[],[]

            for stu in author:
                record = case.loc[case.Author == stu]

                if len(record) != 0:
                    ac = len(record.loc[record.Status == 'Accepted'])
                    pac = len(adj_PAC(record.loc[record.Status == 'Partial Accepted'].copy(), dt.timedelta(minutes = adj_minute)))
                    wa = len(record.loc[record.Status == 'Wrong Answer'])
                    other = len(record.loc[~record.Status.isin(['Accepted', 'Partial Accepted', 'Wrong Answer'])])
                    submit = ac + pac + wa + other
                    AC.append(ac/submit); PAC.append(pac/submit); WA.append(wa/submit); Other.append(other/submit)
                    Submit.append(submit)
                else:
                    #如果沒有提交此題
                    ac, pac, wa,other, submit = 0, 0, 0, 0, 0
                    AC.append(ac); PAC.append(pac); WA.append(wa); Other.append(other)
                    Submit.append(submit)


            AnswerRate[P + ' AC rate_' + str(adj_minute)] = AC
            AnswerRate[P + ' PAC rate_' + str(adj_minute)] = PAC
            AnswerRate[P + ' WA rate_' + str(adj_minute)] = WA
            AnswerRate[P + ' Other rate_' + str(adj_minute)] = Other
            AnswerRate[P + ' Submit count_' + str(adj_minute)] = Submit
            
    AnswerRate = AnswerRate.set_index('Author')
    AnswerRate = AnswerRate[sorted_columns(df, timegap)]
    AnswerRate = AnswerRate.reset_index()
    return AnswerRate

def get_dist_plot(AnswerRate):
    pro = []
    for col in AnswerRate.columns:
        if 'Submit count' in col:
            pro.append(col)
    hw_name = [x.split()[0] +'_'+ x.split('_')[-1] for x in pro]
    output = []
    for i in range(len(pro)):
        col, hw_col = pro[i], hw_name[i]
        select = AnswerRate[col]
        interval = (select.max() - select.min())/10
        tmp = [hw_col]
        for n in range(1, 11):
            down, up, count =(n-1)*interval, n*interval, 0
            for submit in select:
                if n != 10:
                    if (submit >= down) and (submit < up):
                        count += 1
                else:
                    if (submit >= down) and (submit <= up):
                        count += 1
            tmp.append(count)
        tmp.append(interval)
        output.append(tmp)
    output = pd.DataFrame(output).set_index(0)
    output.index.name = None
    output.columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'interval']
    return output

def get_FinishedACrate(df):
    features = ['Problem_code', 'AC_count', 'attempt_student']
    output = {}
    for f in features:
        output[f] = []
    for P in sorted(df['Problem Code'].unique()):
        case = df.loc[df['Problem Code'] == P]
        Problem_code = P
        AC_count = len(case.loc[case.Status == 'Accepted'])
        attempt_student = case.Author.nunique()
        for f in features:
            output[f].append(eval(f))
    output = pd.DataFrame(output)
    return output

def get_histogram(df):
    AnswerRate = get_rates(df)
    FinishedACrate = get_FinishedACrate(df)
    histogram = get_dist_plot(AnswerRate)
    AnswerRate = AnswerRate.set_index('Author')
    AnswerRate.index.name = None
    AnswerRate.rename(index={'b06302345@ntu.edu.tw':'b06302345'}, inplace=True)
    return AnswerRate, FinishedACrate, histogram

def find_best_working(search, df):
    df.When = df.When.apply(pd.to_datetime)
    df = df.sort_values(by = 'When')
    select = df.loc[df.Author == search].copy()
    
    time_gap = [dt.timedelta(hours = 0)]
    for hw in df.HW.unique():
        hw_select = select.loc[select.HW == hw]
        for i in range(1, len(hw_select)):
            time_gap.append(hw_select.When.iloc[i] - hw_select.When.iloc[i-1])
    max_interval = max(time_gap)
    
    select.loc[:, 'hr'] = [x.hour for x in select.When]
    performance = []

    for t in sorted(select.hr.unique()):
        start = t; end = (t+2)%24
        tmp_period = (start, end)
        if end > start:
            select_period = select.loc[(select.hr >= start) & (select.hr < end)]
        elif end < start:
            select_period = select.loc[(select.hr >= start) | (select.hr < end)]
        
        count = len(select_period)
        AC = len(select_period.loc[select_period.Status == 'Accepted'])
        tmp_rate = AC / count
        performance.append([count, AC, tmp_rate, tmp_period])
        
    performance = sorted(performance, reverse = True)
    most_submission_period = performance[0][3]
    
    if performance[0][0] >= 5:
        tmp_rate = performance[0][2]
        for row in performance:
            if row[0] >= 5 and row[2] >= tmp_rate:
                tmp_rate = row[2]
                best_working_time = row[3]
                ACtoSubmit = '{}/{}'.format(row[1], row[0])
    else:
        tmp_rate = performance[0][2]
        for row in performance:
            if row[2] >= tmp_rate:
                tmp_rate = row[2]
                best_working_time = row[3]
                ACtoSubmit = '{}/{}'.format(row[1], row[0])
            
    return best_working_time, ACtoSubmit, most_submission_period, max_interval

def get_personalRecord(df):
    output = {}
    features = ['Author', 'best_working_time', 'ACtoSubmit', 'most_submission_period', 'total_submission', 'total_AC_count', 'avg_SubmitToAC', 'max_interval']

    for f in features:
        output[f] = []

    for search in df.Author.unique():
        Author = search
        select = df.loc[df.Author == search]
        best_working_time, ACtoSubmit, most_submission_period, max_interval = find_best_working(search, df)
        total_submission = len(select)
        complete_question = select.loc[select.Status == 'Accepted', 'Problem Code'].tolist()
        total_AC_count = len(complete_question)
        if total_AC_count == 0:
            avg_SubmitToAC = '無限多'
        else:
            avg_SubmitToAC = len(select.loc[select['Problem Code'].isin(complete_question)])/total_AC_count
        for f in features:
            output[f].append(eval(f))
    PR_output = pd.DataFrame(output)
    return PR_output

def get_Debugtime(df):
    output = {}
    col = ['Author', 'PWS Homework 1', 'PWS Homework 2', 'PWS Homework 3', 'PWS Homework 4', 'PWS Homework 5', 'PWS Homework 6']
    for f in col:
        output[f] = []

    df = df.sort_values(by = 'When')
    for search in df.Author.unique():
        output['Author'].append(search)
        select = df.loc[df.Author == search]
        for hw in col[1:]:
            select_hw = select.loc[select.HW == hw]
            if hw[-1] in ['1', '2']:
                adj_hours = dt.timedelta(hours = 1)
            else:
                adj_hours = dt.timedelta(hours = 2)
            debug = []
            for i in range(len(select_hw)):
                if i == 0:
                    debug.append([(select_hw.When.iloc[i])])
                else:
                    if select_hw.When.iloc[i] - debug[-1][-1] < adj_hours:
                        debug[-1].append(select_hw.When.iloc[i])
                    else:
                        debug.append([(select_hw.When.iloc[i])])

            tot_time = dt.timedelta(hours = 0)
            for cluster in debug:
                if len(cluster) == 1:
                    tot_time += adj_hours
                else:
                    tot_time += (cluster[-1] - cluster[0])
            output[hw].append(tot_time)

    Debugtime = pd.DataFrame(output)
    Debugtime.columns = ['Author', 'HW1_debugtime', 'HW2_debugtime', 'HW3_debugtime', 'HW4_debugtime', 'HW5_debugtime', 'HW6_debugtime']
    return Debugtime

def get_personal_page(df):
    personalRecord = get_personalRecord(df)
    Debugtime = get_Debugtime(df)
    personalpage = personalRecord.merge(Debugtime, how = 'left', on = 'Author')
    personalpage = personalpage.set_index('Author')
    personalpage.index.name = None
    personalpage.rename(index={'b06302345@ntu.edu.tw':'b06302345'}, inplace=True)
    personalpage = personalpage.applymap(lambda x:str(x))
    return personalpage


def get_finish_time(df):
    output = {}
    col = ['Author'] + sorted(df['Problem Code'].unique())
    for f in col:
        output[f] = []
    
    for search in df.Author.unique():
        output['Author'].append(search)
        personal = df.loc[df.Author == search]
        for p in col[1:]:
            try:
                tmp = personal.loc[(personal['Problem Code'] == p) & (personal.Status == 'Accepted'), 'When'].iloc[0]
            except IndexError:
                tmp = dt.datetime(2021,7,1)
            output[p].append(tmp)
    
    output = pd.DataFrame(output)
    return output

def get_EfficientRank(df):
    finish_time = get_finish_time(df)
    author = finish_time.Author
    features = finish_time.columns
    output = {}
    for f in features:
        output[f] = []

    for search in finish_time.Author:
        output['Author'].append(search)
        select = finish_time.loc[finish_time.Author == search]
        for f in features[1:]:
            output[f].append(sorted(finish_time[f]).index(select.iloc[0, select.columns.get_loc(f)]))
    
    EfficientRank = pd.DataFrame(output)
    EfficientRank.loc[:, 'sum_total'] = 0
    for col in EfficientRank.columns[1:-1]:
        EfficientRank.loc[:, 'sum_total'] += EfficientRank.loc[:,col]
    EfficientRank = EfficientRank.sort_values(by = 'sum_total', ascending = True).reset_index().drop('index', axis = 1)
    
    EfficientRank.loc[:, 'Rank'] = 0
    for d in EfficientRank.index:
        EfficientRank.loc[d, 'Rank'] = list(EfficientRank.sum_total).index(EfficientRank.loc[d, 'sum_total'])
    
    EfficientRank = EfficientRank.loc[:,['Author', 'sum_total']].set_index('Author')
    EfficientRank.index.name = None
    return EfficientRank

def get_Accuracy(df):
    features = ['Author', 'total_AC', 'total_submit']
    output = {}
    for f in features:
        output[f] = []
    
    for search in df.Author.unique():
        Author = search
        total_submit = len(df.loc[df.Author == search])
        total_AC = len(df.loc[(df.Author == search) & (df.Status == 'Accepted')])
        for f in features:
            output[f].append(eval(f))
    Accuracy = pd.DataFrame(output)
    Accuracy.loc[:, 'AC_rate'] = Accuracy.total_AC / Accuracy.total_submit
    Accuracy = Accuracy.sort_values(by = 'AC_rate', ascending = False).reset_index().drop('index', axis = 1)
    
    Accuracy.loc[:, 'Rank'] = 0
    for d in Accuracy.index:
        Accuracy.loc[d, 'Rank'] = list(Accuracy.AC_rate).index(Accuracy.loc[d, 'AC_rate'])
    
    Accuracy = Accuracy.loc[:,['Author', 'AC_rate']].set_index('Author')
    Accuracy.index.name = None
    
    return Accuracy

def get_CompleteRate(df):
    features = ['Author', 'finished', 'total', 'CompleteRate']
    output = {}
    for f in features:
        output[f] = []
    
    for search in df.Author.unique():
        Author = search
        total = df['Problem Code'].nunique()
        finished = len(df.loc[(df.Author == search) & (df.Status == 'Accepted')])
        CompleteRate = round(finished/total, 2)
        for f in features:
            output[f].append(eval(f))
    CompleteRate = pd.DataFrame(output)
    CompleteRate = CompleteRate.sort_values(by = 'CompleteRate', ascending = False).reset_index().drop('index', axis = 1)
    
    CompleteRate.loc[:, 'Rank'] = 0
    for d in CompleteRate.index:
        CompleteRate.loc[d, 'Rank'] = list(CompleteRate.CompleteRate).index(CompleteRate.loc[d, 'CompleteRate'])
    
    CompleteRate = CompleteRate.loc[:,['Author', 'CompleteRate']].set_index('Author')
    CompleteRate.index.name = None
    
    return CompleteRate

def get_PACdismissed(AnswerRate):
    output = pd.DataFrame(index = AnswerRate.index)
    for P in df['Problem Code'].unique():
        tmp = AnswerRate.loc[:, P + ' PAC rate_0']*AnswerRate.loc[:,P + ' Submit count_0'] - AnswerRate.loc[:,P + ' PAC rate_5']*AnswerRate.loc[:,P + ' Submit count_5']
        tmp = pd.DataFrame(tmp, columns = [P])
        output = output.merge(tmp, left_index = True, right_index = True)
    output.loc[:, 'PACdismissed'] = 0
    for col in output.columns[:-1]:
        output.loc[:, 'PACdismissed'] += output[col]
    output = output.sort_values(by = 'PACdismissed').reset_index().rename(columns = {'index': 'Author'})
    output.loc[:, 'Rank'] = 0
    for d in output.index:
        output.loc[d, 'Rank'] = list(output.PACdismissed).index(output.loc[d, 'PACdismissed'])
    
    output = output.loc[:, ['Author', 'PACdismissed']].set_index('Author')
    output.index.name = None
    return output

def get_challengeRate(df, FinishedACrate):
    output = pd.DataFrame(index = df.Author.unique())
    challenge_list = ['HW4-2', 'HW4-4', 'HW5-5', 'HW3-4', 'HW5-3']
    for hard in challenge_list:
        output.loc[:, hard] = 0
        for search in output.index:
            output.loc[search, hard] = len(df.loc[(df.Author == search) & (df['Problem Code'] == hard) & (df.Status == 'Accepted')])
    output.loc[:, 'sum_total'] = 0
    for col in output.columns[:-1]:
        output.sum_total += output[col]

    output.loc[:, 'challengeRate'] = round(output.sum_total/5, 2)
    output = output.sort_values(by = 'challengeRate', ascending = False)
    output = output.loc[:, ['challengeRate']]
    return output

def ConvertToPctg(chart):
    for col in ['sum_total', 'PACdismissed']:
        for d in chart.index:
            chart.loc[d, col] = (chart.loc[d, col] - chart[col].min())/(chart[col].max() - chart[col].min())
    
    for col in ['CompleteRate', 'challengeRate']:
        chart[col] = (-1*chart[col] + 1)
    
    for col in ['AC_rate']:
        chart[col] = 1 - chart[col]/chart[col].max()
    
    return chart

def get_RadarChart(df, AnswerRate, FinishedACrate):
    EfficientRank = get_EfficientRank(df)
    Accuracy = get_Accuracy(df)
    CompleteRate = get_CompleteRate(df)
    PACdismissed = get_PACdismissed(AnswerRate)
    challengeRate = get_challengeRate(df, FinishedACrate)
    RadarChart = pd.concat([EfficientRank, Accuracy, CompleteRate, PACdismissed, challengeRate], axis = 1)
    RadarChart = ConvertToPctg(RadarChart)
    RadarChart.columns = ['speed_pctg', 'AC_rate', 'complete_rate', 'PAC_saved_pctg', 'challenge_rate']    
    RadarChart.rename(index={'b06302345@ntu.edu.tw':'b06302345'}, inplace=True)
    RadarChart = RadarChart.applymap(lambda x: str(x))    
    return RadarChart

