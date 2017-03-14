import os
import csv
csvlist=[]
for root,dirs,files in os.walk('A'):
    for ele in files:
        if '.csv' in ele:
            csvlist.append(root+'/'+ele)
            
with open('resultAppend.csv','a') as wf:            
    for ele in csvlist:
        for i in open(ele,'r'):
            wf.write(i)
    