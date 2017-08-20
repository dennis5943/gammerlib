import logging
from chinese_qa_gammer import gammer
import os

max_file_size = 1000

src_data = gammer.cleanData(qa_folder = 'QA/')

#輸出Questions Index檔案
outputIndexFile(src_data,dest_folder = 'answers',index_file_name = 'answers_index.txt')

#輸出各別檔案
ouptputQAFiels(src_data,dest_folder = 'answers')

availkeys = ('question','answers')
pd.DataFrame(src_data,columns = availkeys)