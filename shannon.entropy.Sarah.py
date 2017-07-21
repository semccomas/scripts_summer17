import sys
import math
import numpy as np

lines = [data.rstrip('\n') for data in open(sys.argv[1])]

Nseq=0
seq=''

for l in lines:
    search='>'
    if search in l:
        Nseq=Nseq+1
    else:
        seq=seq+l

nsymb=len(seq)/Nseq

aalist='ARNDCQEGHILKMFPSTWYV-X'

j=0

while j<nsymb:
    en=0
    column=seq[j:len(seq)-1:nsymb]
    gap=float(column.count('-'))/float(Nseq)
    if gap>=0.5:
        print 1
    else:
        for aa in aalist:
            stat=float(column.count(aa))/float(Nseq)+0.000001
            en=en-(stat*math.log(stat))/(math.log(21))
        #print en
        print '{0:.10f}'.format(en)
    j=j+1


#'{0:.10f}'.format(a)