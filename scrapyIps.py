#coding:utf-8
'''
Created on 2016年3月30日
从代理网址中取ip ， 写入ip.txt文件，ip已失效，代理ip需要重新写入，代理网
@author: sx
'''
import urllib2,urllib

from bs4 import BeautifulSoup
import time
import os
from urllib2 import HTTPError
def parseIps():
    url="http://www.xicidaili.com/nn/"
    wdir=os.getcwd()+"/ip.txt"
    Header={      
        'Host': 'www.xicidaili.com',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'If-None-Match':'W/\"405ef7e04f57c249b6ef99a41b80ff49\"'
        }
    req=urllib2.Request(url=url,
        headers=Header
        )
    resp=None
    try:
        resp=urllib2.urlopen(req)
    except HTTPError as e:
        time.sleep(5)
        resp=urllib2.urlopen(req)
    html=resp.read()
    print html
    soup=BeautifulSoup(html)
    trs=soup.select(".odd" or ".")
    ipports=[]
    f=open(wdir,"w")
    for i in range(len(trs)):
        #print trs[i]
        tds=trs[i].findAll("td")
        #print tds
        ip=tds[2].string.strip()
        port=tds[3].string.strip()
        ipport=ip+":"+port
        print ipport
        #f.write(ipport)
        f.write(ipport)
        f.write("\r\n")
        ipports.extend(ipport)
    print ipports
    
if __name__=='__main__':
    parseIps()
