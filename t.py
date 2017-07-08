#-*- coding:utf-8 -*-
'''
Created on 2016年6月6日

@author: sx
'''
import os
if __name__ == '__main__':
    filename = raw_input('please input file name:')
    PatentClass="手机  and B23"
    patCls=PatentClass.decode("utf-8")
    y=10
    x=2
    patclass=patCls
    if patCls.find('/'):
        patclass=patCls.replace('/','-')
    path="C:/Users/shixiong/Desktop/downloadsss/patent"+patclass
    os.mkdir(path)     
    f=open(path+"/class"+str(y)+"page_"+str(x)+"item.txt",'w')
    f.write("sda")
    f.close()
    if filename=='hello':
        raise TypeError('input file name error !')
    print "hello"