#!/usr/bin/env python
#
# Programmed by Keehyoung Joo at KIAS
# newton@kias.re.kr

import os, sys, string
import numpy as np
import array
from math import log

stdout=sys.stdout
stderr=sys.stderr

mapping=[0,4,3,6,13,7,8,9,11,10,12,2,14,5,1,15,16,19,17,18]
aaNum = {'A': 0,'C': 1,'D': 2,'E': 3,'F': 4,
         'G': 5,'H': 6,'I': 7,'K': 8,'L': 9,
         'M':10,'N':11,'P':12,'Q':13,'R':14,
         'S':15,'T':16,'V':17,'W':18,'Y':19,'X':0}
blos_aa= [0,14,11,2,1,13,3,5,6,7,9,8,10,4,12,15,16,18,19,17]

def read_qij(file):
    file = open(file)
    qij = np.zeros((20,20), dtype=np.float64)
    i=0
    for line in file.readlines():
        val = map(float, string.split(line))
        for j in range(len(val)):
            qij[blos_aa[i],blos_aa[j]] = val[j]
            qij[blos_aa[j],blos_aa[i]] = val[j]
        i+=1
    for i in range(20):
        sum = 0.0
        for j in range(20):
            sum += qij[i,j]
        for j in range(20):
            qij[i,j] = qij[i,j]/sum
    return qij

def read_chk(file,qij):
    file = open(chkfile,mode='rb')
    n = array.array('i')
    n.read(file, 1)
    naa=n[0]
    str = array.array('c')
    str.read(file,naa)
    seq = str.tostring()
    out =np.zeros((naa,20), dtype=np.float64)
    col =np.zeros((naa), dtype=np.int)
    quality = np.zeros((naa), dtype=np.float64)

    for i in range(naa):
        v = array.array('d')
        v.read(file,20)
        data=np.array(v, dtype=np.float64)
        if sum(data)==0:
            col[i] = 0
            for j in range(20):
                out[i,j] = qij[aaNum[seq[i]],j]
        else:
            col[i] = 1
            for j in range(20):
                out[i,j] = data[mapping[j]]
        for k in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]:
            quality[i] = quality[i] - out[i,k]*log(out[i,k])
    file.close()
    return naa, seq, out, col, quality
    
if __name__ == '__main__':
    if len(sys.argv)<3:
        print USAGE
        sys.exit()

    name   = sys.argv[1]    # 1tonA
    chkfile= name+'.chk'
# Read Data and Transformation
    b62file = sys.argv[2]
    qij = read_qij(b62file)
#print qij

    naa, seq, out, col, quality = read_chk(chkfile,qij)
    ck2file = open(name+'.ck2','w')
    print >> ck2file, naa
    print >> ck2file, seq
    for i in range(naa):
        for j in range(20):
            print >> ck2file, '%6.4f' % out[i,j],
        print >> ck2file
    ck2file.close()

