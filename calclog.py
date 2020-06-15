#coding:utf-8
import re
from dtutils import *
import numpy as np
fi1eName = "./hqdata.2020-06-15.log"
str1="ServerLog:searchdata"
str2="ServerLog:codelist"

pattern1 = re.compile(r'60969\] \[([\s\w\S\W\d]+)\]')

def calc():
    fi = open(fi1eName,'r')
    text = fi.readlines()
    start=[]
    end=[]
    for tx in text:
        if tx.replace(" ","").find(str1) != -1:
            pa = pattern1.findall(tx)
            dtg = datetime2millitimetag(pa[0],type="%Y-%m-%d %H:%M:%S.%f")
            start.append(dtg)
        if tx.replace(" ","").find(str2) != -1:
            pa = pattern1.findall(tx)
            dtg = datetime2millitimetag(pa[0],type="%Y-%m-%d %H:%M:%S.%f")
            end.append(dtg)
    st = np.array(start)
    ed = np.array(end)
    diff = ed-st
    print(np.sum(diff)/1000)
    
        
if __name__=='__main__':
    calc()
