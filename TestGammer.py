import logging
from chinese_qa_gammer import gammer
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


q_filename = os.path.dirname(os.path.abspath(__file__)) + '/titlelist.txt'
logger.info('title來源:' + q_filename)


url="https://forum.gamer.com.tw/B.php?bsn=60561&subbsn=0"

gammer.GetQ(q_filename = q_filename,max_page = 2,url = url)

a_folder = os.path.dirname(os.path.abspath(__file__))+ '/QA/'
logger.info('目標資料夾:' + a_folder)    
    
#getA(searchIfNonExist = True,q_filename = q_filename)
gammer.AsyncGetA(searchIfNonExist = True,q_filename = q_filename,destFolder = a_folder)
