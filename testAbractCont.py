#coding:utf-8
# textParserReader的测试文件
import urllib
from bs4 import BeautifulSoup
#html=urllib.urlopen("http://www.baidu.com")
#content=html.read()
#print content
#text=content.decode("utf-8").encode("utf-8")
#print "***********************************"
f=open("C:/Users/shixiong/Desktop/niu1.txt",'r')
content=f.read()
soup=BeautifulSoup(content)
id=soup.find("span",class_="current").string.strip()
id=id.split("[")[0].strip()
titlecont=soup.select(".fmbt")
title=titlecont[0].string.split("--")[1].strip()
print title
descont=soup.select(".content")

des=descont[0].getText().strip()
print des  
divcont=soup.select("#abstractItemList")

trs=divcont[0].findAll("tr",recursive=True)
tds=divcont[0].findAll("td",recursive=True)
tdkey=[]
tdvalue=[]
for i in range(len(trs)):
    tdcont=trs[i].contents
    for t in range(len(tdcont)):
        str=tdcont[t].string.strip()
        print str,t
    tdkey.append(tdcont[1].string.strip())
    tdvalue.append(tdcont[3].string.strip())
dicts={}
for i in range(len(tdkey)):
    
    print tdkey[i]
    print tdvalue[i]
    dicts[tdkey[i]]=tdvalue[i]

#for child in tbody.chidren:
 #   print child

        #return pid,title,des
print "title ,des；"
print title,des

dicts[u'发明名称']=title
dicts[u'摘要']=des
for d,x in dicts.items():
    print type(d),type(x)
    if type(d)=="str":
        d=d.decode("utf-8")
    if type(x)=="str":
        x=x.decode("utf-8")
    print "key:"+d+",value:"+x


f.close()
#print text
