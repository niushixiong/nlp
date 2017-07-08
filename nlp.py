
# -*- coding: utf-8 -*-

import sys
import os
from textpre import TextPreprocess  # 第一个是文件名，第二个是类名

BASE_DIR = u"C:\\Users\Administrator\Desktop\lunwen_crawler\lunwen\\train_data"
# 配置utf-8输出环境
reload(sys)
#sys.setdefaultencoding('utf-8')
# 实例化这个类
tp = TextPreprocess()
tp.corpus_path =u"C:\\Users\Administrator\Desktop\lunwen_crawler\lunwen\\train_data\origal_data"  #原始语料路径
tp.pos_path = os.path.join(BASE_DIR,"preprocessed")       #预处理后语料路径
tp.segment_path = os.path.join(BASE_DIR,"segment")    #分词后语料路径
tp.wordbag_path = os.path.join(BASE_DIR,"wordbag")   #词袋模型路径
tp.stopword_path ="stop_words"   #停止词路径
tp.trainset_name = "trainset.dat"      #训练集文件名
tp.wordbag_name = "wordbag.dat"       #词包文件名
tp.preprocess()
tp.segment()
tp.train_bag()
tp.tfidf_bag()#if 要weight 设置 tp.tfidf_bag(True)



