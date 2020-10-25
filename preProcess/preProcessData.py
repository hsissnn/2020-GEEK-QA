#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import ast
import question.question as q
import answer.extractAnswers as a


# 从excel中提取部分数据作为训练集原始数据
def preProcessTrainData():
    data = pd.read_excel(io=r'data/im_plus_data_train.xlsx', sheet_name='Sheet1', usecols=[3])
    index = 2
    f = open('data/preTrainData.txt', 'w+', encoding='utf-8')
    print('-------------开始生成训练集原始数据------------------')
    readExcelData(data, f, index)
    print('-------------结束生成训练集原始数据------------------')
    f.close()


# 从excel中提取部分数据作为测试集原始数据
def preProcessTestData():
    data = pd.read_excel(io=r'data/im_plus_data_test.xlsx', sheet_name='Sheet1', usecols=[3])
    data.reset_index(drop=True)
    index = 2
    f = open('data/preTestData.txt', 'w+', encoding='utf-8')
    print('-------------开始生成测试集原始数据------------------')
    readExcelData(data, f, index)
    print('-------------结束生成测试集原始数据------------------')
    f.close()


def readExcelData(data, f, index):
    for msg in data['会话消息列表']:
        # 1、转为原始类型（list<dict>）
        new_msg = ast.literal_eval(msg)
        # 2、获取问题
        questions = q.extractQuestions(new_msg)
        # 3、抽取第一个业务问题
        firstBusinessQuestion = q.extractFirstBusinessQuestion(questions)
        # 4、抽取这个问题之后所有的答案，以及excel对应的index
        pre = {'excelRows': index}
        if firstBusinessQuestion:
            pre['question'] = list(firstBusinessQuestion.values())[0]
            pre['questionIndex'] = list(firstBusinessQuestion.keys())[0]
            pre['answers'] = a.extractAnswers(firstBusinessQuestion, questions, new_msg)
        else:
            pre['question'] = ''
            pre['answers'] = []
        f.write(str(pre) + '\n')
        index += 1