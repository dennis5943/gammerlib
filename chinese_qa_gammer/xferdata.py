"""
1.整理原始檔案，去除不要的問答
2.將所有Question分詞好，並輸出Question索引
3.將完整的QA問答資料按照Question索引上的指定位置放好
"""
from os import listdir
from os.path import isfile, join
import os
import sys
import re
import pandas as pd
import json
import logging
import jieba

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.debug('start')

def cleanData(qa_folder = 'QA/'):
    logger.info('整理原始資料，去除沒用的問答')
    qafiles = [qa_folder + f for f in listdir(qa_folder) if isfile(join(qa_folder, f)) and os.path.splitext(f)[1] == '.json']

    #qafiles = ['QA/3891399.json']
    filesdata = []
    for file in qafiles:

        try:
            with open(file) as data_file:   
                data = json.load(data_file)
                #print(data)
                data_file.close()

            if '首篇已刪' in data['question']:
                continue

            if len(data['answers']) == 0:
                continue

            filesdata.append(data)
        except:
            logger.error(file + "Unexpected error:" + sys.exc_info()[0])   

    for d in filesdata:
        d['question'] = re.sub('^(\s*【[^】]*】)','',d['question'])
    
    logger.info('整理原始資料結束，總共還有%d筆資料' % len(filesdata))
    return filesdata
    

#--------開始輸出Questions Index檔案------
def outputIndexFile(src_data ,max_file_size = 1000,dest_folder = 'answers',index_file_name = 'question_index.txt'):
    logger.info('開始輸出Questions Index檔案')
    max_file_size = 1000
    i = 0
    filesIdx = []
    
    jieba.set_dictionary('dict.txt.big')

    for d in src_data:
        #輸出question分詞陣列、folder name、file name
        q = {'file':"%s/%05d.txt" % (dest_folder,int(i / max_file_size)),
             'id':i,
             'question':[word for word in jieba.cut(d["question"],cut_all=True) if word != ""]}
        filesIdx.append(q)
        i = i + 1
    
    if os.path.dirname(index_file_name) != '':
        os.makedirs(os.path.dirname(index_file_name), exist_ok=True)
    with open(index_file_name,'w') as res_file:
        json.dump(filesIdx, fp = res_file,ensure_ascii=False)

#輸出各別檔案
def ouptputQAFiels(src_data,max_file_size = 1000,dest_folder = 'answers'):
    logger.info('輸出各別檔案')
    i = 0
    datalist = []
    for d in src_data:
        #輸出question分詞陣列、folder name、file name
        q = {'file':"%s/%05d.txt" % (dest_folder,int(i / max_file_size)),
             'id':i,
             'question':[word for word in jieba.cut(d["question"],cut_all=True) if word != ""]}

        d['id'] = q['id']
        d.pop('reference')
        #del some_dict['reference']
        os.makedirs(os.path.dirname(q['file']), exist_ok=True)

        datalist.append(d)
        i = i + 1

        if i%max_file_size == 0 or i == len(src_data):
            logger.debug('開始寫檔:%s data size:%d' %(q['file'],len(datalist)))
            with open(q['file'],'w') as res_file:
                json.dump(datalist, fp = res_file,ensure_ascii=False)
            datalist = []

if __name__ == '__main__':
    max_file_size = 1000

    src_data = cleanData(qa_folder = 'QA/')

    #輸出Questions Index檔案
    outputIndexFile(src_data,dest_folder = 'answers',index_file_name = 'answers_index.txt')

    #輸出各別檔案
    ouptputQAFiels(src_data,dest_folder = 'answers')

    availkeys = ('question','answers')
    pd.DataFrame(src_data,columns = availkeys)