
# coding: utf-8

# In[1]:



#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        import shutil,os,time
        ct=time.strftime('%Y%m%d',time.localtime())
        if not os.path.exists('/Users/Jackie/Desktop/1025hist/'+ct):
            os.makedirs('/Users/Jackie/Desktop/1025hist/'+ct)
        for root,dirs,files in os.walk('/Users/Jackie/Desktop/1024testdir/'):
            for ele in files:
                if '.csv' in ele:
                    print ele
                    shutil.move('/Users/Jackie/Desktop/1024testdir/'+ele,'/Users/Jackie/Desktop/1025hist/'+ct+'/')
        
        
#         for root,dirs,files in os.walk('/Users/Jackie/Desktop/1024testdir/'):
# #             print files
#             for ele in files:
#                 print ele
#         print "Got it!"


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/Users/Jackie/Desktop/1024testdir/', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    print observer.join()


# In[107]:

# import shutil,os,time


# ct=time.strftime('%Y%m%d',time.localtime())

# if not os.path.exists('/Users/Jackie/Desktop/1025hist/'+ct):
#     os.makedirs('/Users/Jackie/Desktop/1025hist/'+ct)


# for root,dirs,files in os.walk('/Users/Jackie/Desktop/1024testdir/'):
#     for ele in files:
#         if '.csv' in ele:
#             print ele
#             shutil.move('/Users/Jackie/Desktop/1024testdir/'+ele,'/Users/Jackie/Desktop/1025hist/'+ct+'/')
            

            



# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



