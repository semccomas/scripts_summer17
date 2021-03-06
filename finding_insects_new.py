
# coding: utf-8

# In[81]:

### there will be 3 input files to this script. 1st is the alignment file. 2nd is the uniprot database for insects, 3rd is the uniprot identifiers 
#typical fasta file = >Metazoa|a|sp|C9D7C2|CAC1A_APIME/4-186 Voltage-dependent calcium channel type A subunit alpha-1 OS=Apis mellifera GN=CAC PE=2 SV=1
#this is for honeybee btw
#the thing they have in common is the taxon code 
#also for uniprot I removed the rightmost column in excel because i didn't want to figure how to do that otherwise it wasa mess
#insects i removed the uniprot headers before parsing here so that it was easy for pandas to read

import pandas as pd 
import numpy as np 
import sys 

#print 'choose fasta file'

fasta = open('../Marina_USB/seqs/nogaps_iter2.final.fa').read()
#fasta = open('../Marina_USB/seqs/sodium_fasta_only.fa').read()
#fasta = open('../Marina_USB/seqs/calcium_fasta_only.fa').read()
uniprot = open('../Marina_USB/speclist.txt').read().splitlines()
insects = pd.read_csv('../Marina_USB/arthropoda_uniprot.tab', sep = '\t')
insects = insects.drop(['Mnemonic','Synonym', 'Reviewed', 'Rank', 'Lineage', 'Common name','Parent', 'Other Names', 'Virus hosts'], axis = 1)



#parsing the uniprot file which was kind of a mess. It was a text file with somewhat column-like structure but a ton of missing values
#was tab deliminated so that is why split by tab
## parsing the uniprot speclist. It is kind of a funky dataset so the first for loop is filtering out the things I dont need and making the data
#easier to parse in a DF. 
uniprot_speclist = []
for line in uniprot:
    line = line.split()
    if len(line) >= 4 and len(line[1]) == 1:
        line = ' '.join(line)   #basically trying to keep the word in N=<species> together. will get split after again now that we have filtered
        line = line.split(': ')
        uniprot_speclist.append(line)

        
uniprot_speclist = pd.DataFrame(uniprot_speclist)
u_s_split = uniprot_speclist.iloc[:,0].str.split().tolist()   #split so that the code and taxon will be separate
u_s_split = pd.DataFrame(u_s_split)
u_s_split = u_s_split[[0,1,2]]   #there were some byproducts


uniprot_clean = pd.concat([u_s_split, uniprot_speclist], axis = 1) #join the two together again and remove the extra column
uniprot_clean.columns = ['Code', 'x', 'Taxon', 'Delete','Scientific name']   #renaming for clarity
uniprot_clean = uniprot_clean.drop(['x', 'Delete'], axis = 1) #dropping some for clarity
uniprot_clean['Taxon'] = uniprot_clean['Taxon'].map(lambda x: x.rstrip(':'))  #remove the : that was at the end of all vals
uniprot_clean['Taxon'] = uniprot_clean['Taxon'].map(lambda x: x.rstrip(':00:00'))  #remove the :00:00 that was at the end of some vals
uniprot_clean['Taxon'] = uniprot_clean.loc[:,'Taxon'].apply(pd.to_numeric, errors='ignore') #tried with astype but it didnt accept errors.
#this leaves some vals as strings but thats okay because they will get nixed anyways
uniprot_clean['Scientific name'] = uniprot_clean['Scientific name'].map(lambda x: str(x)[2:])  #remove the N= that was at the start of all vals


#getting only the insects from uniprot id's. An issue I see now is that speclist (ie uniprot_clean) does not have all Taxa
taxon = insects.loc[:,'Taxon'].tolist()
#uniprot_insects = uniprot_clean[uniprot_clean['Taxon'].isin(taxon)]   #i tested this with list comprehension so they are def the same length

uniprot_insects = pd.merge(insects, uniprot_clean, on = ['Scientific name'])

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

uniprot_insects


# time to parse fasta file. There are some 'none's at the bottom but I drop them for now, since they wont be in the uniprot list I dont think
species = []
f_splitline = fasta.split('\n')
for line in f_splitline:
    if '>' in line:
        if 'PSEUDO/' in line:
            line = line.split('_')
            species.append(line[1])
        else:
            if '>sp' in line:
                line= line.replace('_','|')
                line = line.split('|')
                species.append(line[2])
            if '>tr' in line:
                line= line.replace('_','|')
                line= line.replace('/','|')
                line= line.replace(' ','|')
                line = line.split('|')
                species.append(line[3]) 


insect_species_in_fasta = []
for line in uniprot_insects["Code"]:
    if line in species:
        insect_species_in_fasta.append(line)


f_splitentry = fasta.split('>')   # I do this because the alignments often took longer than one line, so this keeps the alignment in one piece with the text entry 
o = open('../Marina_USB/seqs/arthropoda_in_fasta_file.txt', 'w')
for insect in insect_species_in_fasta:
    for c, line in enumerate(f_splitentry):
        if insect in line:
            o.write('>' + f_splitentry[c])# + '\n' + f_splitline[c+1] + '\n')
            
o.close()

