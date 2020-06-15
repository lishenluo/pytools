#求所有自然数中的素数
import math
from collections import Iterator,Iterable
def calc():
    i=0
    while True:
        if [ii for ii in range(2,int(math.sqrt(i))) if i%ii == 0] ==[]:
            yield i
        i+=1
    return 0

def show():
    while True:
        info=yield
        print(info)

if __name__=='__main__':
##    gen = calc()
##    for ii in gen:
##        print(ii)
    aa=show()
    print(isinstance(aa,Iterator))
    print(isinstance(aa,Iterable))
    next(aa)
    for ii in ['I','LOVE','YOU']:
        aa.send(ii)
