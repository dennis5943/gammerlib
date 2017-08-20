import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from bs4.element import Tag
import re
import json

def getCommendList(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html5lib")

    #print(soup.prettify())
    
    #取得快速留言區
    mainPost = soup.find('div',class_ = re.compile('c-section__main c-post[\s]*'))
    #print(mainPost)
    commandlist = [s.find('span').contents[0].strip() for s in mainPost.find_all("article",attrs = {"class":re.compile("reply-content__article c-article[\s]*")})
                  if mainPost and s.find('span')]
    #print(commandlist)
    

    articles = [s for s in soup.find_all("div",class_ = "c-article__content")]    
    #print(articles)

    for tag in ('a','font','br','img'):
        for s in [s.find_all(tag) for s in articles if s.find(tag)]:
            for ss in s:
                ss.extract()

    for tag in ('div','p','h1'):
        for s in [s.find_all(tag) for s in articles if s.find(tag)]:
            for ss in s:
                ss.unwrap()
    #print([a.text.strip() for a in articles if a.text.isspace() == False])

    return  commandlist + [a.text.strip() for a in articles if a.text.isspace() == False]

if __name__ == '__main__':
    url = "https://forum.gamer.com.tw/C.php?bsn=60076&snA=4117228&tnum=7"
    cmds = getCommendList(url)
    print(cmds)