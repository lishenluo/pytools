import requests        #导入requests包
import json
import csv
import dtutils as dtl

def getStocks(page,noStock):  
    headerValue = {'Accept-Encoding':'gzip,deflate,br',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'__jsluid_h=86e9aeae3ec77476d3603d36cfeb8099; __jsluid_s=d4e2b23967ae848f7efc1bea4a404034; __jsl_clearance=1590046242.044|0|Sg3eu0dPKGmNsQOshhVJPKSnMsc%3D; JSESSIONID=9xM2LV-wL4ZFxcrAi6ozls2pRD_h39VUx6LHYhCE3Q2gdS4NkVcc!2034289863',
    'Host':'www.csc108.com',
    'Referer':'https://www.csc108.com/kyrz/xxggIndex.jspx',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    
    print('nowpage:'+str(page))
    url = 'https://www.csc108.com/kyrz/kcdbzjList.json?curPage='+str(page)+'&stkCode=&market=&enable='
    try:
        strhtml = requests.request("GET",url,headers=headerValue)
        #print(strhtml.text)

        context = json.loads(strhtml.text)
        currentPage=context['currentPage']
        filename='stocksCanPledge'
        if noStock:
            filename='stocksCanPledgeNotStock'
        f = open(filename+dtl.nowdate()+'.csv','a+',encoding='utf-8',newline='')
        csv_writer = csv.writer(f)
        if context['list']==[]:
            print('end')
            return
        for li in context['list']:

            lis=[]
            mtk = 'SH' if li['market']=='1' else 'SZ'
            if li['stkCode'][0:1] in ['6'] and mtk=='SH':
                continue
            if li['stkCode'][0:1] in ['0','3'] and mtk=='SZ':
                continue
            lis.append(li['stkCode'])
            lis.append(li['stkName'])
            lis.append(float(li['pledgerate']))
            csv_writer.writerow(lis)
        f.close()
    except ee:
        print(ee)
        return
    newpage=int(currentPage)+1
    getStocks(newpage,noStock)
    
    
if __name__=="__main__":
    page=1
    noStock=True
    getStocks(page,noStock)
    