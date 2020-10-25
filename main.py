#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import preProcess.preProcessData as p
import preProcess.calCharacter as c
import answer.xunlian as a


if __name__ == '__main__':
    ''' 
    1、从excel中提取部分数据作为训练集原始数据，包括提取第一个业务问题，获取这个业务问题所有预选答案
       对应数据data/preTrainData.txt 
    '''
    p.preProcessTrainData()
    print()

    '''
    2、从excel中提取部分数据作为测试集原始数据
       对应数据data/preTestData.txt
    '''
    p.preProcessTestData()
    print()

    '''
    3、提取训练集特征向量
       对应xunlian_data_x.txt
    '''
    c.calTrainCharacters()
    print()

    '''
    4、提取测试集特征向量
       对应test_data_x.txt
    '''
    c.calTestCharacters()
    print()

    '''
    5、根据训练集特征向量训练模型,
    '''
    model = a.train()
    print()

    '''
    6、用模型验证测试集结果
    '''
    a.precess(model)














