#coding=utf-8
import nltk
def print_arg(str):
    print str

def add(a,b):
    print 'a=', a
    print 'b=', b
    return a + b
def pos_word(word):
    wordlist=[]
    wordlist.append(word)
    wordTag=nltk.pos_tag(wordlist)
    return wordTag[0]+" "+wordTag[1]
add(1,2)
