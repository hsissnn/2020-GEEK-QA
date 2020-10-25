#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import jieba
import question.question as q
import jieba.posseg as psg

# 总距离
TOTAL_DIS = 10
# 总相似度
TOTAL_REP = 5
# 距离权重
DIS_WEIGHT = 0.5
# 相似度权重
REP_WEIGHT = 0.5

# 名词集合
nouns = ['ni', 'nl' 'ns', 'nt', 'n', 'nd', 'nh']


# 提取训练集特征向量
def calTrainCharacters():
    with open('data/preTrainData.txt', 'r', encoding='utf-8') as f:
        f_train = open('data/train_data_x.txt', 'w+', encoding='utf-8')
        print('-------------开始提取训练集特征向量-----------------')
        for line in f.readlines():
            # 转为原始类型 dict
            segments = ast.literal_eval(line)
            if segments:
                ques = segments.get('question')
                ans = segments.get('answers')
                listVectors = []
                # 问题和对应的答案集合都非空
                if ques and ans:
                    # 定义特征向量
                    distance = 1
                    # filter_question = set(q.filter_stop(jieba.cut(ques, cut_all=False)))
                    filter_question = {}
                    psg_ques = psg.cut(ques)
                    for psg_que in psg_ques:
                        if q.filter_stop(psg_que.word):
                            filter_question[psg_que.word] = psg_que.flag
                    maxValue = 0.00
                    for answerObject in ans:
                        listVector = []
                        # 计算每一个answer的距离特征值
                        re_distance = (TOTAL_DIS - distance)/TOTAL_DIS
                        # 计算问题和答案之间的相关性特征值（比较answer和question重复词的数量）
                        answer = answerObject.get('answer')
                        # filter_answer = set(q.filter_stop(jieba.cut(answer, cut_all=False)))
                        filter_answer = {}
                        psg_ans = psg.cut(answer)
                        for pgs_an in psg_ans:
                            if q.filter_stop(pgs_an.word):
                                filter_answer[pgs_an.word] = pgs_an.flag
                        filter_inter = filter_question.items() & filter_answer.items()
                        countn = 0
                        counts = 0
                        for key, value in enumerate(filter_inter):
                            if nouns.__contains__(value[-1]):
                                countn += 1
                            else:
                                counts += 1
                        re_repeat = (countn * 1.5 + counts) / TOTAL_REP
                        # 计算值
                        weight = re_distance * DIS_WEIGHT + re_repeat * REP_WEIGHT
                        if weight > maxValue:
                            maxValue = weight
                        distance += 1
                        listVector.append(re_distance)
                        listVector.append(re_repeat)
                        listVector.append(weight)
                        listVectors.append(listVector)
                    if listVectors:
                        for item in listVectors:
                            if item[-1] == maxValue:
                                item[-1] = 1
                            else:
                                item[-1] = 0
                            f_train.write(str(item) + '\n')
                else:
                    continue
            else:
                continue
        f_train.close()
        print('-------------结束提取训练集特征向量-----------------')
    f.close()


# 提取测试集特征向量
def calTestCharacters():
    with open('data/preTestData.txt', 'r', encoding='utf-8') as f:
        f_test = open('data/test_data_x.txt', 'w+', encoding='utf-8')
        print('-------------开始提取测试集特征向量-----------------')
        for line in f.readlines():
            # 转为原始类型 dict
            segments = ast.literal_eval(line)
            if segments:
                ques = segments.get('question')
                ans = segments.get('answers')
                questionRows = segments.get('excelRows')
                question_index = segments.get('questionIndex')
                listVectors = []
                # 问题和对应的答案集合都非空
                if ques and ans:
                    # 定义特征向量
                    distance = 1
                    filter_question = set(q.filter_stop(jieba.cut(ques, cut_all=False)))
                    # maxValue = 0.00
                    for answerObject in ans:
                        listVector = []
                        # 计算每一个answer的距离特征值
                        re_distance = (TOTAL_DIS - distance)/TOTAL_DIS
                        # 计算问题和答案之间的相关性特征值（比较answer和question重复词的数量）
                        answer = answerObject.get('answer')
                        answer_index = answerObject.get('answerIndex')
                        filter_answer = set(q.filter_stop(jieba.cut(answer, cut_all=False)))
                        re_repeat = len(filter_answer & filter_question) / TOTAL_REP
                        distance += 1
                        listVector.append(re_distance)
                        listVector.append(re_repeat)
                        listVector.append(questionRows)
                        listVector.append(answer_index)
                        listVector.append(question_index)
                        listVectors.append(listVector)
                    if listVectors:
                        for item in listVectors:
                            f_test.write(str(item) + '\n')
                else:
                    continue
            else:
                continue
        f_test.close()
        print('-------------结束提取训练集特征向量-----------------')
    f.close()
