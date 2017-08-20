import requests
from bs4 import BeautifulSoup
import json
import threading
import logging
import re

logger = logging.getLogger(__name__)

def getPageTitles(url='https://forum.gamer.com.tw/B.php?bsn=60076&subbsn=0'):
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html5lib")
    
    pp = soup.find('p',class_ = 'BH-pagebtnA')
    lastPage = [{'page':a.contents[0],'link':a['href']} for a in pp.find_all('a') if 'href' in a.attrs][-1]
        
    titleList = [{'id':re.match('.*?snA=([\d]+)',s['href']).group(1),'title':s.contents[0],'link':'https://forum.gamer.com.tw/' + s['href']} 
             for s in soup.find_all("a",class_ = "b-list__main__title")]

    logger.debug('標題數量:%d 最後一頁:%s' %(len(titleList),lastPage))
    return lastPage,titleList

def exportFile(titleList = [],filename = 'titlelist.txt'):
    with open(filename,'w') as outfile:
        json.dump(titleList, fp = outfile,ensure_ascii=False)

if __name__ == '__main__':
    lp,tl = getPageTitles()
    urls = ["https://forum.gamer.com.tw/B.php?bsn=60076&subbsn=0&page=" + str(page) for page in range(1,int(lp['page']))]
    
    titles = []
    for u in urls:
        lp,tl = getPageTitles(u)
        titles.extend(tl)
        
    exportFile(titles)
    print(titles)
