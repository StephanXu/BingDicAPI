import sys
import urllib
import urllib.request as request
import json
import http.cookiejar
import requests

from bs4 import BeautifulSoup


def VPrint(content):
    print(json.dumps(content, ensure_ascii=False, indent=1))

def getWord(word_txt):
    try:
        word = word_txt
    except IndexError:
        print("None word")
        exit(0)

    default_cookie = {
        "_EDGE_CD": "m=zh-cn&u=zh-cn",
        "_EDGE_V": "1"
        }

    cookie = http.cookiejar.CookieJar()
    cookie = requests.utils.cookiejar_from_dict(default_cookie,cookie)

    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)

    req = opener.open('http://cn.bing.com/dict/search?q=' + word)
    web_con = req.read().decode('utf-8')

    soup = BeautifulSoup(web_con,"html5lib")
    wordinfo = {}

    #head word
    headword = soup.find(id="headword").string
    wordinfo["headword"] = str(headword)

    #pronunciation
    pronunciation = []
    for strs in soup.find(attrs={"class":"hd_tf_lh"}).strings:
        pronunciation.append(strs.replace('\xa0',''))
    if len(pronunciation)>0:
        wordinfo["pronunce"] = pronunciation

    #meanings
    meanings_ori = []
    for strs in soup.find(id="headword").parent.parent.find("ul").strings:
        meanings_ori.append(strs)
    meanings = dict(zip(meanings_ori[::2],meanings_ori[1::2]))
    wordinfo["meanings"] = meanings

    #samples
    sample = {}
    try:
        for sample_ori in soup.find(id="sentenceSeg").find_all(attrs={"class":"se_li"}):
            sample_en = ""
            for strs in sample_ori.find(attrs={"class":"sen_en"}).strings:
                sample_en = sample_en + " " + strs.replace(" ","")
            sample_cn = ""
            for strs in sample_ori.find(attrs={"class":"sen_cn"}).strings:
                sample_cn = sample_cn + strs.replace(" ","")
            sample_en = sample_en[1:]
            sample[sample_en] = sample_cn
        wordinfo["sample"] = sample
    except AttributeError:
        sample = {}

    #tabs
    tabs = {}
    try:
        tab_titles = []
        tab_content = []
        for tab in soup.find(attrs={"class":"wd_div"}).find(attrs={"class":"tb_div"}).strings:
            tab_titles.append(tab)
        for tabsub in soup.find(attrs={"class":"wd_div"}).find(attrs={"id":"thesaurusesid"}).children:
            tabcon = []
            for strs in tabsub.strings:
                tabcon.append(strs)
            tab_content.append(tabcon)
        tabs = dict(zip(tab_titles,tab_content))
        wordinfo["tabs"] = tabs
    except AttributeError:
        tabs = {}

    return (json.dumps(wordinfo, ensure_ascii=False, indent=1))
