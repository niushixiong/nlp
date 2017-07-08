# -*- coding: utf-8 -*-
'''
Created on 2016年6月6日

@author: sx
'''
import urllib
import re
import io
import gzip
def decodegzip(rawtext):   
    bi = io.BytesIO(rawtext)
    gf = gzip.GzipFile(fileobj=bi, mode="rb")
    textdecode=gf.read()
    return textdecode
url='http://www.pss-system.gov.cn/sipopublicsearch/search/searchHome-searchIndex.shtml?params=991CFE73D4DF553253D44E119219BF31366856FF4B152226CAE4DB031259396A'
html = urllib.urlopen(url).read()
text=decodegzip(html)
print type(text)
#print text
#print html
#text=''' <title> Apple 
#</title>'''
m = re.search(r"\<title\>[\s\S]*\</title\>", text)
print m
print m.group(0) # 这里输出结果 <title>Apple</title>
t=m.group().strip("\<?/title>").strip()
print t
if t=="访问受限":
    print "match sucess"