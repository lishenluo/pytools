#coding:utf8
import time

TYPE='insertorder'
#TYPE='queryorder'
#TYPE='queryaccount'
#TYPE="queryposition"
#TYPE="login"
#TYPE="cancelorder"
#TYPE = "tradecost"
MID_NAMES=[1]
#MID_NAME=''

def diffMillSeconds(strTimeStart,strTimeEnd):
    strTimeStart = strTimeStart.replace("[","")
    strTimeStart = strTimeStart.replace("]","")
    sts = strTimeStart.split(",")

    sts = time.mktime(time.strptime(sts[0], "%Y-%m-%d %H:%M:%S"))*1000+float(sts[1])

    strTimeEnd = strTimeEnd.replace("[","")
    strTimeEnd = strTimeEnd.replace("]","")
    ste = strTimeEnd.split(",")

    ste = time.mktime(time.strptime(ste[0], "%Y-%m-%d %H:%M:%S"))*1000+float(ste[1])

    return ste - sts


def doCalcStat(mid_name):
    import re
    date = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    pattern = re.compile(r'requestid:(\d+)')
    pattern1 = re.compile(r'iOrderNo=(\d+)')
    pattern2 = re.compile(r'size:(\d+)')
    pattern3 = re.compile(r'requestId=(\d+)')
    pattern4 = re.compile(r'"iOrderNo":(\d+)')
    pattern5 = re.compile(r'entrustid:(\d+)')
    testQueryOrder = dict()
    queryOrderRst = dict()
    total=0
    file = "testjkfront."+date + mid_name+".log"
    if TYPE=="tradecost":
        file = "sofront.log.2020-03-10-国海模拟"#+date
    with open(file,'r', encoding='GBK') as fi:
        if TYPE=="tradecost": #日志查询下单情况
            for tx in fi.readlines():
                if tx.find("entryFunc, funcNo") != -1:
                    txt = pattern4.findall(tx.replace(" ",""))
                    if txt !=[] and txt[0] !="0":
                        for tt in txt:
                            testQueryOrder[tt] = tx[0:29]
                if tx.find("EntrustPushHandle, handle entrust confirm push") != -1:
                    txt = pattern5.findall(tx.replace(" ",""))
                    if txt !=[]:
                        if txt[0] not in queryOrderRst:
                            queryOrderRst[txt[0]] = tx[0:29]
        if TYPE=="insertorder": #下单速度
            for tx in fi.readlines():
                if tx.find("testOrderInsert") != -1:
                    txt = pattern.findall(tx.replace(" ",""))
                    testQueryOrder[txt[0]] = tx[0:29]
                if tx.find("orderConfirm") != -1:
                    txt = pattern1.findall(tx.replace(" ",""))
                    queryOrderRst[txt[0]] = tx[0:29]
        if TYPE=="cancelorder": #撤单速度
            for tx in fi.readlines():
                if tx.find("testOrderCancel") != -1:
                    txt = pattern.findall(tx.replace(" ",""))
                    testQueryOrder[txt[0]] = tx[0:29]
                if tx.find("cancelOrderConfirm") != -1:
                    txt = pattern1.findall(tx.replace(" ",""))
                    queryOrderRst[txt[0]] = tx[0:29]
        if TYPE=="login": #登录速度
            for tx in fi.readlines():
                if tx.find("testLogin") != -1:
                    txt = pattern.findall(tx.replace(" ",""))
                    testQueryOrder[txt[0]] = tx[0:29]
                if tx.find("accoLoginRst") != -1 and tx.find("Jkfront Response") != -1:
                    txt = pattern.findall(tx.replace(" ",""))
                    queryOrderRst[txt[0]] = tx[0:29]
        elif TYPE=="queryaccount": #查询资金
            for tx in fi.readlines():
                if tx.find("testQueryAcco") != -1:
                    txt = pattern.findall(tx.replace(" ",""))
                    testQueryOrder[txt[0]] = tx[0:29]
                if tx.find("queryAccoRst") != -1 and tx.find("QueryAccoRsp") != -1:
                    txt = pattern3.findall(tx.replace(" ",""))
                    queryOrderRst[txt[0]] = tx[0:29]
                    if int(total)<=0:
                        total = pattern2.findall(tx.replace(" ",""))[0]
        elif TYPE=="queryorder": #查询速度
            for tx in fi.readlines():
                if tx.find("testQueryOrder") != -1:
                    txt = pattern.findall(tx.replace(" ",""))
                    testQueryOrder[txt[0]] = tx[0:29]
                if tx.find("queryOrderRst") != -1 and tx.find("Jkfront Response") != -1 :
                    txt = pattern.findall(tx.replace(" ",""))
                    queryOrderRst[txt[0]] = tx[0:29]
                    if int(total)<=0:
                        total = pattern2.findall(tx.replace(" ",""))[0]
        elif TYPE=="queryposition": #查询持仓
            for tx in fi.readlines():
                if tx.find("testQueryPosition") != -1:
                    txt = pattern.findall(tx.replace(" ",""))
                    testQueryOrder[txt[0]] = tx[0:29]
                if tx.find("queryStockRst") != -1 and tx.find("Jkfront Response") != -1:
                    txt = pattern.findall(tx.replace(" ",""))
                    queryOrderRst[txt[0]] = tx[0:29]
                    if int(total)<=0:
                        total = pattern2.findall(tx.replace(" ",""))[0]
                
    time_list = []
    bigtime_tag=[]
    for reqid,stime in testQueryOrder.items():
        if reqid in queryOrderRst:
            time_list.append(diffMillSeconds(stime,queryOrderRst[reqid]))
            bigtime_tag.append(queryOrderRst[reqid])

    #print(time_list)

    import numpy as np
    print("文件:",file)

    #知识点enumerate 把序列如list，tuple，str 加上index，默认从0开始


        
    #额外统计二
    if False:
        import heapq
        print("最大的10个时间:",heapq.nlargest(10,time_list))
        print("最小的10个时间:",heapq.nsmallest(10,time_list))

    #额外统计
    if False:
        bigtime = heapq.nlargest(10,time_list)
        big_value_index = [k for k,v in enumerate(time_list) if v>=bigtime[-1]]#满足某个条件的元素和下标
        for ii in big_value_index:
            print(bigtime_tag[ii])
        mid_value_index = [k for k,v in enumerate(time_list) if v<1000 and v>=500]
        len_big = len(big_value_index)
        len_mid = len(mid_value_index)
        print("大于1s的次数:",len_big,",对应第几次满足:",big_value_index)
        print("大于500ms小于1s的次数:",len_mid,",对应第几次满足:",mid_value_index)
        print("占比(%s+%s)/%s=%s"%(len_big,len_mid,len(time_list),(len_big+len_mid)/len(time_list)))

        '''print("\n去除上面两部分的统计情况:")
        sum_index=[]
        sum_index.extend(big_value_index)
        sum_index.extend(mid_value_index)     
        time_list = [v for k,v in enumerate(time_list) if k not in sum_index]'''
        
    print("平均(ms):",np.mean(time_list))
    print("标准差(ms):",np.sqrt(np.var(time_list)))
    print("最大(ms):",np.max(time_list))
    print("最小(ms):",np.min(time_list))  
    
    if TYPE=="insertorder" or TYPE=="login":
        print("下单次数:",len(time_list)) if TYPE=="insertorder" else print("登录次数:",len(time_list))
    elif TYPE=="queryorder" or TYPE=="queryposition" or TYPE=="queryaccount":
        print("查询次数:",len(time_list))
        s = "总委托数:" if TYPE=="queryorder" else "持仓数据条数:" if TYPE=="queryposition" else "资金数据条数:"
        print("%s%s"%(s,total))
    elif TYPE=="tradecost":
        print("统计次数:",len(time_list))



if __name__=="__main__":
    for ii in MID_NAMES:
        doCalcStat("-"+str(ii))
