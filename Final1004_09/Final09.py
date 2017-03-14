
# coding: utf-8

# In[1]:


# modifidate:10/04,
def dirAndfileNameCheck():
    import os
    if not os.path.exists('process'):
        os.makedirs('process')
    with open('./process/nameCheck.txt','w') as nc:
        nc.write('檢查當下目錄'+os.getcwd()+'\n')
        print '檢查當下目錄',os.getcwd()
        nc.write('============'+'\n')
        print '============'
        files = []
        for k in os.listdir('.'):
            if os.path.isfile(k):
                files.append(k)
        countf = 0
        countnof = 0
        nc.write('正確格式'+'\n')
        print '正確格式' 
        for f in files:
            if'日報表' in f:
                countf += 1
                print f  #解開註解可以顯示檔案名稱
        nc.write('正確格式有'+str(countf)+'個'+'\n')
        print '正確格式有', countf,'個'
        nc.write('============'+'\n')
        print '============'
        nc.write('不正確格式'+'\n')
        print '不正確格式'        
        for f in files:  
            if('日報表' not in f)&( 'xls' in f):
                countnof += 1
                print f
        nc.write('不正確格式有'+str(countnof)+'個'+'\n')
        print '不正確格式有', countnof,'個'  
        


# In[2]:

dirAndfileNameCheck()


# In[3]:

# ---------設定字的格式
def set_style(name,height,bold=False):
    import xlwt
    style = xlwt.XFStyle() # 初始化样式
    font = xlwt.Font() # 为样式创建字体                    
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6
    style.font = font  # style.borders = borders
    return style
# ---------


# In[11]:

#讀取北市Excel資料只抓出我所設定之內湖區的街道資料
def julToSepNeihu():
    import os
    try:
        if not os.path.exists('NeiHu'):
            os.makedirs('NeiHu')
    except:
        print 'can not make NeiHu directory'
    files = []
    for f in os.listdir('.'):
            if os.path.isfile(f):
                    files.append(f)
    for f in files:
        if '日報表' in f:
            import xlrd,xlwt
            wbk = xlwt.Workbook()
            # 
            data = xlrd.open_workbook(f)
            sheet = wbk.add_sheet('sheet1',cell_overwrite_ok=True)
            table = data.sheet_by_name(u'日報表詳表')  #以名字去找表1003改
            j=0
            for i in range(775,781):
                rows = table.row_values(i)
                j+=1
                for ele in range(0,len(rows)):
                    sheet.write(j-1,ele,rows[ele],set_style('Times News Roman',200,True))
            try:
                for k in range(1252,1303):
                        rows = table.row_values(k)
                        if rows[2] == u'健康路-南京東路':
                            continue
                        else:
                            j+=1
                            for ele in range(0,len(rows)):
                                sheet.write(j-1,ele,rows[ele],set_style('Times News Roman',200,True))
            except:
                print f,'range小於1306'

            # print len(rows)
            # for ele in rows:
            #     print ele
            # sheet.write(0,1,table)
            wbk.save('NeiHu/'+f)


# In[12]:

julToSepNeihu()


# In[13]:

import os
files = []
for f in os.listdir('./NeiHu'):      
    files.append(f)
for f in files:
    print f


# In[14]:

#讀取內湖資料只抓出設定之內湖區各時段分開的街道資料，將三個時段資料存成三個資料夾（上/下/全日）。

def writePeriod09():
    import os
    if not os.path.exists('NeiHu/上午時段'):
        os.makedirs('NeiHu/上午時段')
    if not os.path.exists('NeiHu/下午時段'):
        os.makedirs('NeiHu/下午時段')
    if not os.path.exists('NeiHu/全日時段'):
        os.makedirs('NeiHu/全日時段')
    
#      上午時段
    files = []
    for f in os.listdir('./NeiHu'):      
        files.append(f)
    for f in files:
        if '日報表' in f:
            import xlrd,xlwt
            wbk = xlwt.Workbook()
            data = xlrd.open_workbook('NeiHu/'+f)
            sheet = wbk.add_sheet('sheet1',cell_overwrite_ok=True)
            table = data.sheets()[0]
            j=0
            for i in range(0,57,+3):#只取上午時段
                rows = table.row_values(i)
                j+=1
                for ele in range(0,len(rows)):
                    sheet.write(j-1,ele,rows[ele],set_style('Times News Romans',200,True))
            sheet.write(j,5,"=SUM(F1:F19)")
            # print len(rows)
            # for ele in rows:
            #     print ele
            # sheet.write(0,1,table)
            wbk.save('NeiHu/上午時段/'+'上午'+f)
#     下午時段        
    files = []
    for f in os.listdir('./NeiHu'):
            
        files.append(f)
    for f in files:
        if '日報表' in f:
            import xlrd,xlwt
            wbk = xlwt.Workbook()
            data = xlrd.open_workbook('NeiHu/'+f)
            sheet = wbk.add_sheet('sheet1',cell_overwrite_ok=True)
            table = data.sheets()[0]
            j=0
            for i in range(1,57,+3):#只取下午時段
                rows = table.row_values(i)
                j+=1
                for ele in range(0,len(rows)):
                    sheet.write(j-1,ele,rows[ele],set_style('Times News Romans',200,True))
            sheet.write(j,5,"=SUM(F1:F19)")
            # print len(rows)
            # for ele in rows:
            #     print ele
            # sheet.write(0,1,table)
            wbk.save('NeiHu/下午時段/'+'下午'+f)
#      全日時段        
    files = []
    for f in os.listdir('./NeiHu'):
            
        files.append(f)
    for f in files:
        if '日報表' in f:
            import xlrd,xlwt
            wbk = xlwt.Workbook()
            data = xlrd.open_workbook('NeiHu/'+f)
            sheet = wbk.add_sheet('sheet1',cell_overwrite_ok=True)
            table = data.sheets()[0]
            j=0
            for i in range(2,57,+3):#只取全日時段

                rows = table.row_values(i)
                j+=1
                for ele in range(0,len(rows)):
                    sheet.write(j-1,ele,rows[ele],set_style('Times News Romans',200,True))
            sheet.write(j,5,"=SUM(F1:F19)")
            # print len(rows)
            # for ele in rows:
            #     print ele
            # sheet.write(0,1,table)
            wbk.save('NeiHu/全日時段/'+'全日'+f)


# In[15]:

writePeriod09()


# In[9]:

#  把抓出來的內湖區的資料，取檔案日期跟當日所有路段的當量做總和，在寫成一個csv檔

def periodVolume09():
    # -*- coding: utf-8 -*-
    import os,re
    import csv
#     上午
    try:
        newcsv = open('NeiHu/上午時段/上午.csv','w')
        files = []
        for f in os.listdir('./NeiHu/上午時段'):
            files.append(f)
        #  在表頭加上分類    
        newcsv.write('date'+','+'eq'+','+'day'+'\n')
        for f in files:
            if '日報表' in f:
                import xlrd
                
                data = xlrd.open_workbook('NeiHu/上午時段/'+f)
                table = data.sheets()[0]
                cols = table.col_values(5)
#                 7to9的星期是row(0)[12],但是4to6&7在row(0)[9]的地方 
                cellDay = table.row(0)[12].value
                sumall = 0
                for i in range(0,len(cols)-1):
                #print cols[i]
                    sumall += float(cols[i])
                match = re.findall('[0-9]+.[0-9]+.[0-9]+',f)
    #             print str(match[0]) , str(sumall) # 解開註解可以印出來看 
                newcsv.write(str(match[0])+','+str(sumall)+','+str(cellDay)+'\n')
        newcsv.close()
        
    except:
        print 'no 上午時段 directory'
    try:

    #     下午
        newcsv = open('NeiHu/下午時段/下午.csv','w')
        files = []
        for f in os.listdir('./NeiHu/下午時段'):
            files.append(f)
            #  在表頭加上分類    
        newcsv.write('date'+','+'eq'+','+'day'+'\n')
        for f in files:
            if '日報表' in f:
                import xlrd
               
                data = xlrd.open_workbook('NeiHu/下午時段/'+f)
                table = data.sheets()[0]
                cols = table.col_values(5)
                #  7to9的星期是row(0)[12],但是4to6&7在row(0)[9]的地方 
                cellDay = table.row(0)[12].value
                sumall = 0
                for i in range(0,len(cols)-1):
                #print cols[i]
                    sumall += float(cols[i])
                match = re.findall('[0-9]+.[0-9]+.[0-9]+',f)
    #             print str(match[0]) , str(sumall) # 解開註解可以印出來看 
                newcsv.write(str(match[0])+','+str(sumall)+','+str(cellDay)+'\n')
        newcsv.close()
    except:
        print 'no 下午時段 directory'
    try:

    #     全日

        newcsv = open('NeiHu/全日時段/全日.csv','w')
        files = []
        for f in os.listdir('./NeiHu/全日時段'):
            files.append(f)
            #  在表頭加上分類    
        newcsv.write('date'+','+'eq'+','+'day'+'\n')
        for f in files:
            if '日報表' in f:
                import xlrd
              
                data = xlrd.open_workbook('NeiHu/全日時段/'+f)
                table = data.sheets()[0]
                cols = table.col_values(5)
                # 7to9的星期是row(0)[12],但是4to6&7在row(0)[9]的地方 
              
                cellDay = table.row(0)[12].value
                sumall = 0
                for i in range(0,len(cols)-1):
                #print cols[i]
                    sumall += float(cols[i])
                match = re.findall('[0-9]+.[0-9]+.[0-9]+',f)
    #             print str(match[0]) , str(sumall) # 解開註解可以印出來看 
#     加上了星期幾str(cellDay)
                newcsv.write(str(match[0])+','+str(sumall)+','+str(cellDay)+'\n')

        newcsv.close()
        
    except:
        print 'no 全日時段 directory'


# In[10]:

periodVolume09()


# In[24]:

def morningAndNoon():

    import os
    import csv
    if not os.path.exists('NeiHu/上下午'):
        os.makedirs('NeiHu/上下午')

    morning = open('NeiHu/上午時段/上午.csv','rU')
    noon = open('NeiHu/下午時段/下午.csv','rU')
    twoPeriod = open('NeiHu/上下午/上下午.csv','w')

    # 上午
    mrlist = []
    mr = csv.reader(morning,delimiter=' ')
    for mrow in mr:
        mrlist.append(mrow)


    # 下午
    nrlist = []
    nr = csv.reader(noon,delimiter=' ')
    for nrow in nr:
        nrlist.append(nrow)

    # print len(nrlist)


    for i in range(0,len(mrlist)):
    #     print nrlist[i][0]
        twoPeriod.write(mrlist[i][0]+','+'am')
        twoPeriod.write('\n')

        twoPeriod.write(nrlist[i][0]+','+'pm')
        twoPeriod.write('\n')



    morning.close()
    noon.close()
    twoPeriod.close()


# In[25]:

morningAndNoon()


# In[ ]:



