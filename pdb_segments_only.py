
# coding: utf-8

# In[60]:

#this script is to compare the MSA of the cockroach protein D0E0C2 to the PDB structure file used in VMD. This will be used for calculating relative entropy between the cockroach MSA


# In[61]:

import pandas as pd 

msa = open('../Marina_USB/seqs/specific_insects_removed_extras.mfa').read()
msa = msa.split('>')
msa = msa[2]

msa = msa.replace('-', '')
msa = msa[85:]
msa = msa.replace('\n', '')
seq = list(msa)


# In[62]:

from Bio.PDB import *
parser = PDBParser()
structure = parser.get_structure('NAvPaS', '../docking/cluster_domain1.pdb')

aa = []
for model in structure:
    for chain in model:
        for residue in chain.get_residues():
            aa.append(residue.get_resname())


# In[63]:

d = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M', 'HSD': 'H', 'ASX': 'N'}
pdb = []
for line in aa:
    try:
        pdb.append(d[line])
    except KeyError:
        pass  #should just be BGL and BMA- which is just sugar. Don't need 
        #print line <-- this is how you can check to be sure you only have sugars, just comment out when running



# In[64]:

match = 0
indexes = []
testing = []
for n, line in enumerate(pdb):
    try: 
        if line == seq[match]:
            indexes.append(n)     #loop through the pdb file (which is longer than seq), so you should be skipping lines ONLY in PDB!!!
            #therefore only append the line number (n) to indexes when there is a match, and when you match then move forward one in the seq file (MSA file)
            testing.append(line)
            match = match + 1
    except IndexError:
        pass
#testing and seq should be =!!



# In[65]:

import numpy as np
indexes = np.asarray(indexes)    #make into array for finding diff
indexes = indexes + 140 #indexing for this pdb file start at 140
a= np.asarray(np.where(np.diff(indexes)!= 1)) #where are the differences are equal to 1, these are consecutive matches in the MSA => are sequences of the segment
sect_r = indexes[a] #+ 140  
sect_r = np.append(sect_r, 1528) #last number of pdb file
sect_l = indexes[a + 1] #+ 140 
sect_l = np.insert(sect_l, 0, 141)  #this is the first number of the pdb file that we want

#sect_l will be where the indexing starts for the extract function
#sect_r will be where the indexing stops
# ^^ these are the two numbers surrounding to diff != 1 in indexes. So if in indexes it reads 18, 19, 26- 
# np.diff will say 1, 7, and a will take only 7. We want 19 and 26, so in sect_l goes 19 and in sect_r goes 26! 
length = np.shape(sect_l)[0]
names = []
for i in xrange(length):
    names.append('split_' + str(i) + '.pdb')
    
for i in xrange(length):
    extract(structure, 'A', sect_l[i], sect_r[i], names[i])
    #print sect_l[i], sect_r[i], names[i]

# think of indexing, it is + 140 on pdb file


#extract(structure, 'A', 141, 159, 'testing.pdb') #this is how it should look for example. This INCLUDES last index


# In[ ]:


    


# In[76]:

match = 0
### LOOK HERE!!!!
for n, line in enumerate(pdb):
    try: 
        if line == seq[match]:
            print n + 332, line, match+4, '< seq in MSA'
            match = match + 1
    except IndexError:
        pass


# In[70]:

for m in structure:
    for c in m:
        for r in c:
            print r


# In[83]:

missing = open('../Marina_USB/seqs/pdbfiles/find_missing_aa.txt').read().splitlines()
m = []
for line in missing:
    line = line.split()
    m.append(d[line[3]])


# In[87]:

len(testing)


# In[ ]:



