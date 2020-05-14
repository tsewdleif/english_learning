#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time : 2020/5/12 0012 下午 23:02
# @Author : West Field
# @File : word.py

import nltk
import re
from collections import Counter
import os
import itertools

def words_statistic(file_path):
    '''
    统计每套听力真题中每个单词个数
    :param file_path: 每套听力真题的原材料路径
    :return: 单词个数的字典，key为单词，value为单词个数
    '''
    with open(file_path, 'r', encoding='utf-8') as file:
        sentence_str = file.read()
    # 将非字母、数字、空格的字符替换为''
    word_str = re.sub('[^\w ]', ' ', sentence_str)
    # 单词转化成小写
    words = word_str.lower()
    # 分词
    word_list = nltk.word_tokenize(words)
    # 统计每个单词的频次
    counts = Counter(word_list)
    return dict(counts)

def all_words_statistic():
    '''
    统计所有听力真题中每个单词的频次
    :return:
    '''
    # 读取每套听力材料的的文件路径
    path = '../data/listening/'
    filenames = os.listdir(path)
    # 总的词频统计字典
    all_statistic_dict = {}
    # 遍历每个文件
    for filename in filenames:
        statistic_dict = words_statistic(path + filename)
        # 两个字典相加：相同key则value相加后赋值给all_statistic_dict中的key，否则将key加入到all_statistic_dict中
        for key, value in statistic_dict.items():
            if key in all_statistic_dict:
                all_statistic_dict[key] += value
            else:
                all_statistic_dict[key] = value
    return all_statistic_dict

def words_filter():
    '''
    过滤掉长度不大于3的单词，并按照value值从大到小排序
    :return:
    '''
    all_statistic_dict = all_words_statistic()
    print("单词总数：",len(all_statistic_dict))
    # 过滤掉长度不大于3的单词
    filter_dict = {k: v for k, v in all_statistic_dict.items() if len(k) > 3}
    print("长度大于3的单词总数：",len(filter_dict))
    # 词频排序
    # sorted_dict = sorted(filter_dict.items(), key=lambda x:x[1], reverse=True)
    # print("词频排序：",sorted_dict)
    return filter_dict

def lemmatization():
    '''
    根据词频字典和词形字典进行词形还原，然后再统计词频
    :return:
    '''
    filter_dict = words_filter()
    # 读取词形还原字典
    with open('../lemmatization-lists/lemmatization-en.txt', 'r', encoding='utf-8') as f:
        res = f.read()
    word_list = [d.split('\t') for d in res.split('\n')]
    word_list[0][0] = '1'
    # 词形字典，key是词的变形，value是词的原形，key不包括词的原形本身
    lemmatization_dict = {d[1]:d[0] for d in word_list}
    # 先把词频字典转化为元组组成的列表，再将元组的key根据词形字典转化为词的原形
    tuple_list = [(k, v) for k, v in filter_dict.items()]
    lem_tuple_list = [(lemmatization_dict[v[0]], v[1]) if v[0] in lemmatization_dict else v for v in tuple_list]
    print(len(lem_tuple_list), lem_tuple_list)
    # 词频统计，相同的词的个数相加
    final_statistic = [(key, sum(i[1] for i in group)) for key, group in
              itertools.groupby(sorted(lem_tuple_list, key=lambda x: x[0]), key=lambda x: x[0])]
    print(len(final_statistic), final_statistic)
    result = sorted(final_statistic, key=lambda x:x[1], reverse=True)
    print(result)
    return result

def result_save():
    '''
    将词频统计结果写入到听力单词文件中，单词长度均大于3
    :return:
    '''
    result = lemmatization()
    with open('../result/listening_words.txt', 'a', encoding='UTF-8') as f:
        for d in result:
            f.write("%s: %s\n"%(d[0], d[1]))


if __name__ == '__main__':
    result_save()
