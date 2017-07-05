### there will be 3 input files to this script. 1st is the alignment file. 2nd is the uniprot database for insects, 3rd is the uniprot identifiers 
#typical fasta file = >Metazoa|a|sp|C9D7C2|CAC1A_APIME/4-186 Voltage-dependent calcium channel type A subunit alpha-1 OS=Apis mellifera GN=CAC PE=2 SV=1
#this is for honeybee btw
#the thing they have in common is the taxon code 

import pandas as pd 

fasta = open('../Marina_USB/seqs/test.txt').read()   #find out how to do absolute path cause this bugs me
#uniprot = open('../Marina_USB/speclist.txt').read()   #this is the whole uniprot
uniprot = open('speclist.txt').read().splitlines()
insects = pd.read_csv('../Marina_USB/insects_uniprot.tab', sep = '\t')


print uniprot
