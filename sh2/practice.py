# -*- coding: utf-8 -*-
# @Time    : 2019/4/1 20:31
# @Author  : Alan
# @Email   : xiezhengwen2013@163.com
# @File    : practice.py
# @Software: PyCharm


import pandas as pd
import numpy as np

df = pd.DataFrame({'total_bill': [16.99, 10.34, 23.68, 23.68, 24.59],
                   'tip': [1.01, 1.66, 3.50, 3.31, 3.61],
                   'sex': ['Female', 'Male', 'Male', 'Male', 'Female']})
df2 = pd.DataFrame({'total_bill': [16.99, 10.34, 23.68, 23.68, 24.59],
                   'tip': [1.01, 1.66, 3.50, 3.31, 3.61],
                   'sex': ['Female', 'Male', 'Male', 'Male', 'Female']})
df3 = pd.DataFrame({'total_bill': [16, 10, 23, 23, 24],
                   'tip': [1.1, 1.6, 3.5, 3.3, 3.6],
                   'sex': ['Female', 'Male', 'Male', 'Male', 'Female']})
'''查看数据类型等'''
print(df)
print(df.dtypes)
print(df.index)
print(df.columns)


'''构建一个完整的dataframe'''
da = pd.DataFrame([[1,2,3],[1,3,4],[2,4,3]],index = ['one','two','three'],columns = ['A','B','C'])
print(da)
# va可以看成是个列表
va = df.values
print(va)


'''取行列的3种方法'''
# loc，基于列label，可选取特定行（根据行index）；
# iloc，基于行/列的position；
# ix，为loc与iloc的混合体，既支持label也支持position；
print(df.loc[1:3, ['total_bill', 'tip']])  # 1，3是行的label
print(df.iloc[1:3, [1, 2]])  # 1，3是行的position
print(df.ix[1:3, [1, 2]])


'''Pandas实现where filter以及逻辑语句'''
print(df['sex'] == 'Female')  # 返回布尔值
print(df[df['sex'] == 'Female'])
print(df[df['total_bill'] > 20])
# and
print(df[(df['sex'] == 'Female') & (df['total_bill'] > 20)])
# or
print(df[(df['sex'] == 'Female') | (df['total_bill'] > 20)])
# in
print(df[df['total_bill'].isin([21.01, 23.68, 24.59])])
# not
print(df[-(df['sex'] == 'Male')])  # 用个负号表示“非”
print(df[-df['total_bill'].isin([21.01, 23.68, 24.59])])


'''对where条件筛选后只有一行的dataframe取其中某一列的值'''
print(df[df['tip'] == 1.66])
print(df.loc[df['tip'] == 1.66])
total = df.loc[df['tip'] == 1.66, 'total_bill'].values
print(total[0])


'''数据去重'''
# drop_duplicates根据某列对dataframe进行去重
# subset，为选定的列做distinct，默认为所有列
# keep，值选项{'first', 'last', False}，保留重复元素中的第一个、最后一个，或全部删除
# inplace ，默认为False，返回一个新的dataframe；若为True，则返回去重后的原dataframe
print('-------------')
# print(df.drop_duplicates(subset=['sex'], keep='first', inplace=True))
print('-------------')
print(df)
print('-------------')
print(df.drop_duplicates(subset=['sex'], keep='first'))


'''group'''
# size()计算自身的size，count()计算其他元素的size
print(df.groupby('sex').size())
print(df.groupby('sex').count())
# 对于多合计函数，挑出多个元素
print(df.groupby('sex').agg({'tip':np.max, 'total_bill': np.sum}))
# count(distinct **)
print(df.groupby('tip').agg({'sex': pd.Series.nunique}))


'''修改列的别名'''
ren = df.rename(columns = {'total_bill': 'total', 'tip': 'pit', 'sex': 'xes'})
print(ren)


'''进行全局修改'''
# df.replace(to_replace, value) 前面是需要替换的值，后面是替换后的值。要改变源数据需要使用inplace = True
print('进行全局修改')
# 对dataframe中所有是Female的进行修改
print(df.replace(to_replace='Female', value='Sansa'))
# 对某列进行修改
print(df.replace({'sex': {'Female': 'Sansa', 'Male': 'Leone'}}, inplace=True))


'''合并df'''
# 按DataFrame的index进行join,即按行合并
# print(df2.join(df3, how='left'))
# 按on指定的列做join
print(df3)
# how='inner' 参数指的是当左右两个对象中存在不重合的键时，取结果的方式：inner 代表交集；outer 代表并集；left 和 right 分别为取一边。
print(pd.merge(df3, df2, how='left', left_on='tip', right_on='tip'))
print(pd.merge(df3, df2, how='right', left_on='tip', right_on='tip'))
print(pd.merge(df3, df2,  left_on='tip', right_on='tip'))
print(pd.merge(df3, df2,  on='tip'))


'''排序'''
# tip是在total_bill中相同行进行排序
print(df.sort_values(['total_bill', 'tip'], ascending=[False, True]))
print(df.sort_values(['total_bill', 'tip'], ascending=[False, False]))


'''取前k个值'''
top_k = df.nlargest(4, columns=['total_bill'])
print(top_k)
# 取某一列
print(top_k.iloc[:, [0]])
# 取某一行
print(top_k.iloc[0])


'''自定义'''
# map(func)，为Series的函数，DataFrame不能直接调用，需取列后再调用；
# apply(func)，对DataFrame中的某一行/列进行func操作；
# applymap(func)，为element-wise函数，对每一个元素做func操作
print(df['tip'].map(lambda x: x - 1))
print(df[['total_bill', 'tip']])
# 对列求和
# 对行求和
print(df[['total_bill', 'tip']].apply(sum, axis=0))
print(df[['total_bill', 'tip']].apply(sum, axis=1))
# 处理null值
df['total_bill'] = df['total_bill'].map(lambda x:0.0 if pd.isnull(x) else x)
print(df)

