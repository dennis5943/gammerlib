import logging
from chinese_qa_gammer import xferdata
import os
import pandas as pd

max_file_size = 1000

qa_folder = os.path.dirname(os.path.abspath(__file__))  + '/QA/'
print('qa_folder' , qa_folder)

dest_folder = os.path.dirname(os.path.abspath(__file__))  + '/output/'
print('dest_folder' , dest_folder)

src_data = xferdata.cleanData(qa_folder = qa_folder)

#輸出Questions Index檔案
xferdata.outputIndexFile(src_data,dest_folder = dest_folder)

#輸出各別檔案
xferdata.ouptputQAFiles(src_data,dest_folder = dest_folder)

availkeys = ('question','output')
pd.DataFrame(src_data,columns = availkeys)