import re
import time
import sys
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.stdout = default_stdout
sys.stderr = default_stderr
sys.setdefaultencoding('utf-8')
import requests
import json
from bs4 import BeautifulSoup



headers= {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
         'Cookie':'_gat=1; _ga=GA1.3.783444797.1482466352'}
with open('/Users/Jackie/Desktop/tt1227.csv','w') as fw:
    for ele in range(5,195800,5):
        try:
            print ele
            time.sleep(0.05)
            res = requests.get('http://hospital.kingnet.com.tw/free/consulting.html?start={}'.format(ele), headers = headers)
            res.encoding='big5'
            soup = BeautifulSoup(res.text, 'html.parser')

            depart = []
            idlist = []

            for dep in soup.select('td.health01 a'):
                if '科' in dep.text:
                    depart.append(dep.text)


            for idd in soup.select('a'):
                if (idd.get('name') == None) or (idd.get('name') == 'moreservice') or ('doctor' in idd.get('name')):
                    pass
                else:
                    idlist.append(idd.get('name'))

            i=0
            for p in soup.select('p'):
                for tt in p.select('font.medicine03'): #症狀：
                    if '不要怕' in tt.text:
                        pass
                        break
                    else:
        #                 print tt.text
                        fw.write(tt.text.strip())
                        break

                for ii in p.select('font.health03'):# Dr.who
        #             print idlist[i]
        #             print depart[i]
        #             print ii.text
                    fw.write(','+depart[i]+','+idlist[i])
                    fw.write(','+ii.text.strip()+'\n')
                    i+=1
                    break

                for ee in p.select('span.content'): # 問題
                    if ee.text == '醫師':
                        pass
                    else:
        #                 print ee.text
                        fw.write(''.join(ee.text.replace(',','#').split()))
                    break
                for dd in p.select('font.doctor05'): # 醫生回答
        #             print dd.text,'r'
                    fw.write(','+''.join(dd.text.replace(',','#').split())+',')
                    break
        except:
            print ele+'error'
            with open('craw.txt','w') as here3:
                here3.write(u'craw exception'+u'\n')
                here3.write(str(sys.stderr)+u'\n')
                here3.write(str(sys.exc_info()[0])+u'\n')
                here3.write(str(sys.exc_info()[1])+u'\n')
                here3.write(str(sys.exc_info()[2])+u'\n')
            continue


