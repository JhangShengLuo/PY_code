 #!/Users/Jackie/anaconda/bin/python
 #coding: utf-8

import sys
import io
import os
import csv
import re
import datetime




try:
  import rpy2.rinterface 
  
except :
  with open('/Users/Jackie/Desktop/1101try/here3.txt','w') as here3:
    here3.write(str(sys.stderr)+u'\n')
    here3.write(str(sys.exc_info()[0])+u'\n')
    here3.write(str(sys.exc_info()[1])+u'\n')
    here3.write(str(sys.exc_info()[2])+u'\n')


