# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 20:45
# @Author  : Alan
# @Email   : xiezhengwen2013@163.com
# @File    : analysis1.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from wordcloud import WordCloud


df = pd.read_csv('../data/company/DataAnalyst2.csv', encoding='utf-8')

'''进行对数据快速的浏览'''
print(df.info())
print(df.head())
print(df.columns.tolist())
# ['city', 'companyFullName', 'companyId', 'companyLabelList', 'companyShortName', 'companySize', 'businessZones',
# 'firstType', 'secondType', 'education', 'industryField', 'positionId', 'positionAdvantage', 'positionName',
# 'positionLables', 'salary', 'workYear']

'''positionId是职位ID，值唯一, 查看是否有重复的数据'''
print(len(df.positionId.unique()))
df_duplicates = df.drop_duplicates(subset='positionId', keep='first')
print(df_duplicates.head(5))
print(df_duplicates.info())


# 定义了个word_cut函数，它查找「-」符号所在的位置，并且截取薪资范围开头至K之间的数字
def cut_word(word, method):
    position = word.find('-')
    length = len(word)
    if position != -1:
        bottomSalary = word[:position-1]
        topSalary = word[position+1: length-1]
    else:
        bottomSalary = word[:word.upper().find('K')]
        topSalary = bottomSalary
    if method == 'bottom':
        return bottomSalary
    else:
        return topSalary


'''提取薪资上限和下限'''
df_duplicates['topSalary'] = df_duplicates.salary.apply(cut_word, method = 'top')
df_duplicates['bottomSalary'] = df_duplicates.salary.apply(cut_word, method= 'bottom')
# 将bottomSalary转换为数字，如果转换成功，说明所有的薪资数字都成功截取了。
df_duplicates.topSalary = df_duplicates.topSalary.astype('int')
df_duplicates.bottomSalary = df_duplicates.bottomSalary.astype('int')
print(df_duplicates.topSalary)
print(df_duplicates.bottomSalary)


'''求解平均薪资'''
# apply是针对Series，现在则是DataFrame, axis=1则是列
df_duplicates['avgSalary'] = df_duplicates.apply(lambda x: (x.bottomSalary + x.topSalary)/2, axis=1)
print(df_duplicates.avgSalary)

'''选出想要的内容进行分析'''
df_clean = df_duplicates[['city', 'companyShortName', 'companySize', 'education', 'industryField', 'positionName',
                         'positionLables', 'workYear', 'avgSalary']]
print(df_clean.head())

'''统计所有非零元素的个数，以降序的方式输出Series'''
print(df_clean.city.value_counts())
print(df_clean.describe())

'''绘图'''
df_clean.avgSalary.hist()
plt.show()
ax = df_clean.boxplot(column='avgSalary', by='city', figsize=(9, 7))
plt.show()

'''清除无用数据'''
print(df_clean.positionLables)
# str方法允许我们针对列中的元素，进行字符串相关的处理，这里的[1:-1]不再是DataFrame和Series的切片，而是对字符串截取，这里把[]都截取掉了。
# 使用完str后，它返回的仍旧是Series，当我们想要再次用replace去除空格。还是需要添加str的
word = df_clean.positionLables.str[1: -1].str.replace(' ', '')
print(word)

# dropna()将所有含有NaN项的行删除
df_word = word.dropna().str.split(',').apply(pd.value_counts)
# reset_index可以还原索引，重新变为默认的整型索引。
# 用groupby计算出标签出现的次数
df_word_counts = df_word.unstack().dropna().reset_index().groupby('level_0').count()
print(df_word_counts)

'''词云展示'''
print(df_word_counts.index)
df_word_counts.index = df_word_counts.index.str.replace("'","")
wordcloud = WordCloud(font_path='C:\Windows\Fonts\simsun.ttc', background_color='white')
wordcloud.fit_words(df_word_counts.level_1)
axs = plt.imshow(wordcloud)
plt.axis("off")
plt.show()
