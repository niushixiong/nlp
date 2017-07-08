# -*- coding: utf-8 -*-
'''
Created on 2016年6月8日

@author: sx
'''

if __name__ == '__main__':
    lists = [['foo bar'],['asd ad']]
    
    fl=open('list.txt', 'w')
    
    for i in range(len(lists)):
        
        fl.write("".join(lists[i]))
        fl.write("\n")
    fl.close()
    result=[]  
    fd = file( "list.txt", "r" )  
  
    for line in fd.readlines():
        temp=" ".join(list(line.split('\n'))).strip()
        templist=[]
        templist.append(temp)
        result.append(templist)  
    print(result)  
    fd.close()
    print "write finally"