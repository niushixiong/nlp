
# -*- coding: utf-8 -*-

import sys
import os
import jieba
import jieba.analyse
#引入Bunch类
from sklearn.datasets.base import Bunch
#引入持久化类
import pickle
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

##############################################################
# 分类语料预处理的类
# 语料目录结构：
# corpus
#   |-catergory_A
#     |-01.txt
#     |-02.txt
#   |-catergory_B
#   |-catergory_C
#   ...
##############################################################

# 配置utf-8输出环境
reload(sys)
#sys.setdefaultencoding('utf-8')

#文本预处理类
class TextPreprocess:
        data_set = Bunch(target_name=[],label=[],filenames=[],contents=[])
        # 定义词袋对象:data_set
        # Bunch类提供一种key,value的对象形式
        # target_name:所有分类集名称列表
        # label:每个文件的分类标签列表
        # filenames:文件名称
        # contents:文件内容
        wordbag = Bunch(target_name=[],label=[],filenames=[],tdm=[],vocabulary={})
        def __int__(self):  #构造方法
                        self.corpus_path = ""    #原始语料路径
                        self.pos_path = ""       #预处理后语料路径
                        self.segment_path = ""   #分词后语料路径
                        self.wordbag_path = ""   #词袋模型路径
                        self.stopword_path = ""  #停止词路径
                        self.trainset_name = ""      #训练集文件名
                        self.wordbag_name = ""       #词包文件名
                        self.titlelis=[]
                        self.weight=[1,10]    # 权重（调节标题的权重多少合适），内容1，标题10，（可扩展加入版号 权重， 需扩展weight 加入 numPub结构 ）
                        #self.numPub=[]
        # 对输入语料进行基本预处理，删除语料的换行符，并持久化。
        # 处理后在pos_path下建立与corpus_path相同的子目录和文件结构
        def preprocess(self):
                if(self.corpus_path=="" or self.pos_path==""):
                        print "corpus_path或pos_path不能为空"
                        return
                dir_list = os.listdir(self.corpus_path) # 获取每个目录下所有的文件
                for mydir in dir_list:
                        class_path = self.corpus_path+"/"+mydir+"/" # 拼出分类子目录的路径
                        file_list = os.listdir(class_path)  # 获取class_path下的所有文件
                        for file_path in file_list:   # 遍历所有文件
                                file_name = class_path + file_path  # 拼出文件名全路径
                                file_read = open(file_name, 'rb')   # 打开一个文件
                                raw_corpus = file_read.read()       # 读取未处理的语料
                                if raw_corpus=='""':
                                    print file_name
                                    file_read.close();
                                    os.remove(file_name)
                                    continue
                                # 按行切分字符串为一个数组
                                corpus_array = raw_corpus.splitlines()
                                raw_corpus = ""
                                lis=[]
                                for line in corpus_array:
                                        line=line.strip()
                                        # raw_corpus = self.simple_pruneLine(line,raw_corpus)
                                        """  存储 title  ，如果想加入版号，"""
                                        
                                         
                                        raw_corpus = self.custom_pruneLine(line,raw_corpus)
                                # lis[0] 为title ，lis[1]为作者
                                
                                lis=self.getAbstract(raw_corpus)     
                                #self.titlelis.append(jieba.analyse.extract_tags(lis[0],5))
                                self.titlelis.append(lis)
                                #拼出分词后语料分类目录
                                
                                pos_dir = self.pos_path+"/"+mydir+"/"
                                if not os.path.exists(pos_dir):    #如果没有创建
                                        os.makedirs(pos_dir)
                                file_write = open ( pos_dir + file_path, 'wb' )
                                file_write.write(raw_corpus)
                                file_write.close()  #关闭写入的文件
                                file_read.close()
                print "中文语料修改处理成功！！！"

        # 对行的简单修剪
        def simple_pruneLine(self,line,raw_corpus):
                if line != "":
                        raw_corpus += line
                return raw_corpus
        #返回 标题，作者，版号，简要信息lis[]
        def getAbstract(self,raw_corpus):
            t=raw_corpus.split("\",")
            t2=[]
            for i in range(len(t)):
                #print "text",i,":"    
                te=t[i].strip().strip("\"")
    
                if te!="" and i!=0 and te.find("]")==-1:
                    
                    t2.append(te)
            key=" ".join(t2)
            t2.append(key)
            return t2
            
            
            
            
      
        # 自定义行处理
        def custom_pruneLine(self,line,raw_corpus):
                if line.find("【 日  期 】")!=-1:
                        line = ""
                elif line.find("【 版  号 】")!=-1:
                        line = ""
                elif line.find("【 作  者 】")!=-1:
                        line = ""
                elif line.find("【 正  文 】")!=-1:
                        line = ""
                elif line.find("【 标  题 】")!=-1:
                        line = ""
                if line != "":
                        raw_corpus += line
                return raw_corpus

        # 对预处理后语料进行分词,并持久化。
        # 处理后在segment_path下建立与pos_path相同的子目录和文件结构
        def segment(self):
                if(self.segment_path=="" or self.pos_path==""):
                        print "segment_path或pos_path不能为空"
                        return
                dir_list = os.listdir(self.pos_path)
                # 获取每个目录下所有的文件
                for mydir in dir_list:
                        class_path = self.pos_path+"/"+mydir+"/" # 拼出分类子目录的路径
                        file_list = os.listdir(class_path)  # 获取class_path下的所有文件
                        for file_path in file_list:   # 遍历所有文件
                                file_name = class_path + file_path  # 拼出文件名全路径
                                file_read = open(file_name, 'rb')   # 打开一个文件
                                raw_corpus = file_read.read()       # 读取未分词语料
                                seg_corpus = jieba.cut(raw_corpus)  # 结巴分词操作
                                #拼出分词后语料分类目录
                                seg_dir = self.segment_path+"/"+mydir+"/"
                                if not os.path.exists(seg_dir):    #如果没有创建
                                        os.makedirs(seg_dir)
                                file_write = open ( seg_dir + file_path, 'wb' ) #创建分词后语料文件，文件名与未分词语料相同
                                file_write.write(" ".join(seg_corpus))  #用空格将分词结果分开并写入到分词后语料文件中
                                file_read.close()  #关闭打开的文件
                                file_write.close()  #关闭写入的文件
                print "中文语料分词成功完成！！！"

  #打包分词后训练语料
        def train_bag(self):
                if(self.segment_path=="" or self.wordbag_path=="" or self.trainset_name==""):
                        print "segment_path或wordbag_path,trainset_name不能为空"
                        return
                # 获取corpus_path下的所有子分类
                dir_list = os.listdir(self.segment_path)
                self.data_set.target_name  = dir_list
                # 获取每个目录下所有的文件
                for mydir in dir_list:
                        class_path = self.segment_path+"/"+mydir+"/" # 拼出分类子目录的路径
                        file_list = os.listdir(class_path)  # 获取class_path下的所有文件
                        for file_path in file_list:   # 遍历所有文档
                                file_name = class_path + file_path# 拼出文件名全路径

                                self.data_set.filenames.append(file_name) #把文件路径附加到数据集中
                                self.data_set.label.append(self.data_set.target_name.index(mydir)) #把文件分类标签附加到数据集中
                                file_read = open(file_name, 'rb')   # 打开一个文件
                                seg_corpus = file_read.read()       # 读取语料
                                self.data_set.contents.append(seg_corpus) # 构建分词文本内容列表
                                
                                
                                
                                
                                file_read.close()
    #词袋对象持久化
                if not os.path.exists(self.wordbag_path):
                        os.makedirs(self.wordbag_path)
                file_obj = open(self.wordbag_path+"/" + self.trainset_name, "wb")
                pickle.dump(self.data_set,file_obj)
                file_obj.close()
                print "分词语料打包成功完成！！！"

  #计算训练语料的tfidf权值并持久化为词袋, 要增加权重 需设置在调用此函数时，set weightSet=True
        def tfidf_bag(self,weightSet=False):
                if(self.wordbag_path=="" or self.wordbag_name=="" or self.stopword_path==""):
                        print "wordbag_path，word_bag或stopword_path不能为空"
                        return
                #读取持久化后的训练集对象
                file_obj = open(self.wordbag_path+'/'+self.trainset_name, "rb")
                self.data_set = pickle.load(file_obj)
                file_obj.close()
                # 定义词袋数据结构: tdm:tf-idf计算后词袋
                self.wordbag.target_name = self.data_set.target_name
                self.wordbag.label = self.data_set.label
                self.wordbag.filenames = self.data_set.filenames
                # 构建语料
                corpus = self.data_set.contents
                stpwrdlst = self.getStopword(self.stopword_path)
                # 使用TfidfVectorizer初始化向量空间模型--创建词袋
                vectorizer = TfidfVectorizer(stop_words=stpwrdlst,sublinear_tf = True,max_df = 0.5)
                # 该类会统计每个词语的tf-idf权值
                transformer=TfidfTransformer()
                # 文本转为词频矩阵
                self.wordbag.tdm = vectorizer.fit_transform(corpus)
                #保存词袋词典文件
                self.wordbag.vocabulary = vectorizer.vocabulary_
                """  增加权重值 设置
                """
                vector=self.wordbag.tdm
                veArray=vector.toarray()
                
                word=vector.get_feature_names()
                if weightSet:
                    #for i in range(len(veArray)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
                     #  # print u"-------这里第",i,u"类文本的词语tf-idf权重------"
                      #  for j in range(len(word)):
                       #     for k in range(len(self.list[i])):
                        #        if word[j]==self.list[i][k]:
                         #           veArray[i][j]*self.weight[1]
                          #      else:
                           #         veArray[i][j]*self.weight[0]
                   # for i in range(len(veArray)):
                    #    for k in range(len(self.titlelis[i])):
                     #       t=self.wordbag.vocabulary.get(self.titlelis[k])
                      #      veArray[i][t]=veArray[i][t]*10
                    #self.wordbag.tdm=veArray
                    for i in range(len(veArray)):
                        for k in range(len(self.titlelis[i])):
                            temp=vector.data[self.wordbag.vocabulary.get(self.titlelis[k])]
                            vector.data[self.wordbag.vocabulary.get(self.titlelis[k])]=temp*10
                
                # 创建词袋的持久化
                file_obj = open(self.wordbag_path+"/" + self.wordbag_name, "wb")
                pickle.dump(self.wordbag,file_obj)
                file_obj.close()
                print "if-idf词袋创建成功！！！"

  #导入获取停止词列表
        def getStopword(self,stopword_path):
                #从文件导入停用词表
                stpwrd_dic = open(stopword_path, 'rb')
                stpwrd_content = stpwrd_dic.read()
                #将停用词表转换为list
                stpwrdlst = stpwrd_content.splitlines()
                stpwrd_dic.close()
                return stpwrdlst

  #验证持久化结果：
        def verify_trainset(self):
                file_obj = open(self.wordbag_path+self.trainset_name,'rb')
                #读取持久化后的对象
                self.data_set = pickle.load(file_obj)
                file_obj.close()
                #输出数据集包含的所有类别
                print self.data_set.target_name
                #输出数据集包含的所有类别标签数
                print len(self.data_set.label)
                #输出数据集包含的文件内容数
                print len(self.data_set.contents)

        def verify_wordbag(self):
                file_obj = open(self.wordbag_path+"/"+self.wordbag_name,'rb')
                #读取持久化后的对象
                self.wordbag = pickle.load(file_obj)
                file_obj.close()
                #输出数据集包含的所有类别
                print self.wordbag.target_name
                #输出数据集包含的所有类别标签数
                print len(self.wordbag.label)
                #输出数据集包含的文件内容数
                print self.wordbag.tdm.shape

        #只进行tfidf权值计算：stpwrdlst:停用词表;myvocabulary:导入的词典
        def tfidf_value(self,test_data,stpwrdlst,myvocabulary,weightSet=False):
                vectorizer = TfidfVectorizer(vocabulary=myvocabulary)
                transformer=TfidfTransformer()
                vector=vectorizer.fit_transform(test_data)
                """  增加权重值 设置
                """
                #vector=self.wordbag.tdm
                veArray=vector.toarray()
                
                word=vector.get_feature_names()
                if weightSet:
                    for i in range(len(veArray)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
                        # print u"-------这里第",i,u"类文本的词语tf-idf权重------"
                        for j in range(len(word)):
                            for k in range(len(self.list[i])):
                                if word[j]==self.list[i][k]:
                                    veArray[i][j]*self.weight[1]
                                else:
                                    veArray[i][j]*self.weight[0]
                    vector=veArray
                
                
                
                return vector

        #导出词袋模型：
        def load_wordbag(self):
                file_obj = open(self.wordbag_path+'/'+self.wordbag_name,'rb')
                self.wordbag = pickle.load(file_obj)
                file_obj.close()
        #导出训练语料集
        def load_trainset(self):
                file_obj = open(self.wordbag_path+'/'+self.trainset_name,'rb')
                self.data_set = pickle.load(file_obj)
                file_obj.close()

