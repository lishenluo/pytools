#coding=utf8
import os
#import tkFileDialog
import re
pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
pattern = re.compile(r'(深圳金三甲)')
    
def readFilename(file_dir):
    for root, dirs, files in os.walk(file_dir): 
        return files,dirs,root
 
def findstring(pathfile,edcode):
    fp = open(pathfile, "r",encoding=edcode)#注意这里的打开文件编码方式
    strr = fp.read()
    #print strr.find("DoubleVec")
    #print(strr)
    txt = pattern.findall(strr)
    if txt != []:#(strr.find("121.43.72.15") != -1):
        print (txt)
        return True
    return False
    
def startfind(files,dirs,root):
    for ii in files:
        if ii=="connect.cfg":
            pass
        else:
            #continue
            pass
        #print(ii)
        try:
            if(findstring(root+"\\"+ii,'utf-8')):
                print (root,ii)
        except Exception as err:
            try:
                    
                if(findstring(root+"\\"+ii,'gbk')):
                    print (root,ii)
            except Exception as er:
                continue
            
            
                
    for jj in dirs:
        fi,di,ro = readFilename(root+"\\"+jj)
        startfind(fi,di,ro)
    
if __name__ == '__main__':
    default_dir = u"F:\SEN WORK"  # 设置默认打开目录
    file_path = default_dir#th.expanduser(default_dir)))
    files,dirs,root = readFilename(file_path)
    print(root)
    startfind(files,dirs,root)
