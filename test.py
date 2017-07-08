#encoding=utf-8
#-*- coding:utf-8 -*-
'''
Created on 2016年6月7日

@author: sx
'''

import jieba.analyse
import jieba
from numpy import inf
"""text = "结巴中文分词模块是一个非常好的Python分词组件"
lis=[]
lis.append(text)
print lis
tags= list(jieba.cut(text))
print type(tags)

print tags[1]
weight=[1,2]
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
"""
texts='''[
    "\n\n\n摘要：\n\n根据Oldham RC链分抗逼近电路的电路特征与数学特征,采用理论推导和MAT-LAB编程两种方法实现四类Oldham RC链分抗逼近电路的零极点的求解.针对Oldham RC链的规则级联结构特点,由简化电路求出传输矩阵、迭代矩阵,并求出阻抗函数的一般数学表达式.使用特征值分解法和Hamilton-Cayley展开法求出迭代矩阵幂而获得各类OldhamRC链分抗的简洁数学表达式,并给出特殊初始阻抗情形下各类Oldham RC链分抗的零极点的解析解.利用MATLAB中的\"solve\"和\"roots\"函数编程实现任意简单初始阻抗下零极点的数值求解.验根结果表明,实现了电路零极点的精确求解.\n\n", 
    "分数阶微积分", 
    "", 
    "电路与系统", 
    "", 
    "零极点", 
    "", 
    "迭代矩阵", 
    "", 
    "阻抗", 
    "", 
    "多项式的根", 
    ""
]'''
t=texts.split("\",")
t2=[]
for i in range(len(t)):
    #print "text",i,":"    
    te=t[i].strip().strip("\"")
    
    if te!="" and i!=0 and te.find("]")==-1:
        t2.append(te)
key=" ".join(t2)
print key
"""
documents=['The dog ate a sandwich and I ate a sandwich','The wizard transfigured a sandwich']
lists=[[1,2,3],[2,3,4]]
#test=set(lists)
#print test
Tfidefvector=TfidfVectorizer(stop_words='english')
tfidfStruct=Tfidefvector.fit_transform(documents)
print type(tfidfStruct.data)


TfidifvectorArray=Tfidefvector.fit_transform(documents).toarray()
print "toarray:",TfidifvectorArray
#print Tfidefvector
Vocabulary=Tfidefvector.vocabulary_
weith=[1,1.5]
for i in range(len(TfidifvectorArray)):
    t=Vocabulary.get("sandwich")
    print t
    if t!=None:
        print TfidifvectorArray[i][t]




"""

tdata=tfidfStruct.data

print "vocabulary:",Vocabulary
print "tfidfstruct:",tfidfStruct
print "tfidfstruct　data:",tdata
FeatureWord=Tfidefvector.get_feature_names()
print "featureWord:",FeatureWord
for i in range(len(TfidifvectorArray)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    #print u"-------这里输出第",i,u"类文本的词语tf-idf权重------"
    for j in range(len(Vocabulary)):
        print FeatureWord[j],TfidifvectorArray[i][j]
        TfidifvectorArray[i][j]=TfidifvectorArray[i][j]*2
print type(tfidfStruct)
#print tfidfStruct.tocsr()
tfidfStruct=csr_matrix(TfidifvectorArray)
print "tfidifstruct data:",tfidfStruct.data
"""