#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as psg

stopwords = [line.strip() for line in open("data/stopwords.txt", encoding='UTF-8').readlines()]

dataSet = {"怎", "怎么", "怎么着", "为什么", "如何", "什么", "哪", "哪里", "哪儿", "多会儿", "怎么样", "几", "多少", "吗", "么", "?", "？", "呢", '么',
           '请问', '嘛',"能否", "能不能", "是否", "如何", "请教"}

isSentenceDataSet = {"可以", "能否", "是否", "能否", "吗", "能不能"}


# 过滤停用词
def filter_stop(words):
    return list(filter(lambda x: x not in stopwords, words))


def filter_sentence(sentence):
    sentence_depart = jieba.cut(sentence.strip())
    outstr = ''
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
    return outstr


# 提取问题
def isQuestion(sentence):

    if len(sentence) <= 3:
        return False
    seg_list = jieba.cut(sentence, cut_all=False)
    for word in seg_list:
        if word in dataSet:
            return True
    return False


# 提取问题
def extractQuestions(segments):
    ques = {}
    del_ques = []
    flag_imkf = 0

    # 1、没有客服回答的直接返回空
    for seg in segments:
        if 'imkf' in seg['fromuid'] or 'imebk' in seg['fromuid']:
            flag_imkf = 1
            break
    if flag_imkf == 0:
        return {}

    # 2、存在客服回答, 客户连续问或两个问之间有客服回答，提取出这个问题
    for key, seg in enumerate(segments):
        if seg['fromuid'] == 'user':
            ques[key] = seg['message']
    if ques:
        pre = -1
        for key in ques.keys():
            if pre == -1:
                pre = key
                continue
            else:
                if key - pre == 1:
                    pre = key
                    continue
                else:
                    flag = 0
                    new_segments = segments[pre:key]
                    for new_segment in new_segments:
                        if 'imkf' in new_segment['fromuid'] or 'imebk' in new_segment['fromuid']:
                            pre = key
                            flag = 1
                            break
                    if flag == 0:
                        del_ques.append(key)
    if del_ques:
        for del_que in del_ques:
            ques.pop(del_que)
    return ques


# 提取第一个业务问题
def extractFirstBusinessQuestion(questions):
    question = {}
    if questions:
        for key, value in questions.items():
            if isQuestion(value):
                question[key] = value
                return question
    return question


if __name__ == '__main__':
    # seg_list = jieba.cut("你好我定了17-21 四晚的住宿", cut_all=False)
    # print(list(seg_list))
    nouns = ['ni', 'nl' 'ns', 'nt', 'n', 'nd', 'nh']
    seg_list1 = psg.cut("你好我定了17-21 四晚的住宿")
    seg_list2 = psg.cut("四晚的住宿")
    # print(list(seg_list1))
    map1 = {}
    map2 = {}
    for word in seg_list1:
        if filter_sentence(word.word):
            map1[word.word] = word.flag
    for word in seg_list2:
        if filter_sentence(word.word):
            map2[word.word] = word.flag
    # print(map1)
    # print(map2)
    map_inters = map1.items() & map2.items()
    print(map_inters)
    for key, value in enumerate(map_inters):
        if nouns.__contains__(value[-1]):
            print(value)

    # a = filter_stop(seg_list)
    # b = filter_stop(seg_list1)
    # print(seg_list)

#第一个问题处理
#如果中间有提问要去除距离的影响
#如果是是否疑问句，则要去除词语的影响

#第二个问题处理
#如果find第一个问题， 上下文是非疑问句,那么将上下文拼接