#! /usr/bin/env python3
# -*- coding: utf-8 -*-

modal_partial = ['你好', '您好']
str_ninhao = '很高兴为您服务'


# 提取预选答案
def extractAnswers(firstBusinessQuestion, questions, segments):
    answers = []
    questionsKeys = list(questions.keys())
    firstQuestionKey = list(firstBusinessQuestion.keys())[0]
    if questions.__contains__(firstQuestionKey):
        length = len(questions)
        # 获取这个key对应的index
        firstIndex = questionsKeys.index(firstQuestionKey)
        nextIndex = firstIndex + 1
        # 存在下一个问题
        if nextIndex < length:
            nextQuestionKey = questionsKeys[nextIndex]
            firstSegments = segments[firstQuestionKey:nextQuestionKey]
            if firstSegments:
                firstIndex = firstQuestionKey
                for parseSegment in firstSegments:
                    if 'imkf' in parseSegment['fromuid'] or 'imebk' in parseSegment['fromuid']:
                        answer_message = parseSegment['message']
                        if modal_partial.__contains__(answer_message.replace(" ", "")) or answer_message.__contains__(str_ninhao):
                            continue
                        else:
                            answerBody = {'answer': answer_message, 'quality': True, 'answerIndex': firstIndex}
                            answers.append(answerBody)
                    firstIndex += 1

            nextSegments = segments[nextQuestionKey:]
            if nextSegments:
                nextIndex = nextQuestionKey
                for nextSegment in nextSegments:
                    if 'imkf' in nextSegment['fromuid'] or 'imebk' in nextSegment['fromuid']:
                        answer_message = nextSegment['message']
                        if modal_partial.__contains__(answer_message.replace(" ", "")) or answer_message.__contains__(str_ninhao):
                            continue
                        else:
                            answerBody = {'answer': nextSegment['message'], 'quality': False, 'answerIndex': nextIndex}
                            answers.append(answerBody)
                    nextIndex += 1
        # 不存在下一个问题
        else:
            allSegments = segments[firstQuestionKey:]
            if allSegments:
                allIndex = firstQuestionKey
                for allSegment in allSegments:
                    if 'imkf' in allSegment['fromuid'] or 'imebk' in allSegment['fromuid']:
                        answer_message = allSegment['message']
                        if modal_partial.__contains__(answer_message.replace(" ", "")) or answer_message.__contains__(str_ninhao):
                            continue
                        else:
                            answerBody = {'answer': allSegment['message'], 'quality': True, 'answerIndex': allIndex}
                            answers.append(answerBody)
                    allIndex += 1

    return answers

