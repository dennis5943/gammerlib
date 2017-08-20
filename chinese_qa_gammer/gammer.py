from grab_answer_list import *
from grab_title_list import *
import os
import sys
from pathlib import Path

import json
from pprint import pprint
import queue


import logging



#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                    datefmt='%m-%d %H:%M',
#                    handlers = [logging.FileHandler(os.path.dirname(os.path.abspath(__file__)) + '/log.txt', 'w', 'utf-8'),])

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(level = logging.DEBUG)

logger = logging.getLogger(__name__)

logger.debug('fisrt log')

def GetQ(q_filename = 'titlelist.txt',max_page = -1):
    lp,tl = getPageTitles()
    
    urls = ["https://forum.gamer.com.tw/B.php?bsn=60076&subbsn=0&page=" + str(page) for page in range(1,int(lp['page']))]

    if max_page > 0:
        urls = [urls[i] for i in range(0,min(max_page,len(urls)))]

    que = queue.Queue()
    for u in urls:
        que.put(u)

    #threads = [threading.Thread(target=dequeue, name='Thd' + str(i), args=(que,destFolder,i)) for i in range(0,100)]

    titles = []
    for u in urls:
        lp,tl = getPageTitles(u)
        titles.extend(tl)

    exportFile(titles,filename = q_filename)
    print(titles)

#再取得Answers list
def destPath(destFolder,srcData = {}):
    #print(srcData['id'])
    #print('cdir',os.path.dirname(os.path.abspath(__file__)))
    #print('dir',os.path.dirname(os.path.abspath(__file__))+ '/QA/')
    path = destFolder + str(srcData['id']) + '.json'
    #print('destPath',path)
    return path


def AsyncGetA(searchIfNonExist = False,q_filename = 'titlelist.txt',destFolder = ''):
    
    with open(q_filename) as data_file:    
        data = json.load(data_file)

    #pprint([data[i] for i in range(0,3)])

    que = queue.Queue()

    if searchIfNonExist:
        srcData = [d for d in data 
        if Path(destPath(destFolder,d)).exists() == False]
    else:
        srcData = data

    logger.info('還有' + str(len(srcData)) + '筆資料要處理')

    #srcData = [srcData[i] for i in range(0,3)]
    for d in srcData:
        que.put(d)

    logger.info('Queue Size:' + str(que.qsize()))
    threads = [threading.Thread(target=dequeue, name='Thd' + str(i), args=(que,destFolder,i)) for i in range(0,100)]
    logger.info('Thread Size:' + str(len(threads)))
    for th in threads:
        th.start()

def dequeue(*args):
    #print(args)
    queue = args[0]
    destFolder = args[1]

    while queue.qsize() > 0:  
        d = queue.get()
        print('[dequeue]SrcData:',d)

        print('[dequeue]Link:',d['link'])
        path = destPath(destFolder,d)
        print('[dequeue]DestPath:',path)
        cmds = getCommendList(d['link'])
        print(cmds)
        
        qa = {'question':d['title'],'answers':cmds,'reference':d['link']}
            
        os.makedirs(os.path.dirname(path), exist_ok=True)
        exportFile(qa,filename = path)

if __name__ == '__main__':

    q_filename = os.path.dirname(os.path.abspath(__file__)) + '/titlelist.txt'
    logger.info('title來源:' + q_filename)
    #GetQ()

    a_folder = os.path.dirname(os.path.abspath(__file__))+ '/QA/'
    logger.info('目標資料夾:' + a_folder)    
    
    #getA(searchIfNonExist = True,q_filename = q_filename)
    AsyncGetA(searchIfNonExist = True,q_filename = q_filename,destFolder = a_folder)
    #print(os.path.dirname(os.path.abspath(__file__)))
