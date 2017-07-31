
from biopandas.pdb import PandasPdb
import pandas as pd 
ppdb = PandasPdb()
ppdb.read_pdb('EeNav_conect.pdb')
sugar_atoms = ppdb.df['HETATM'][(ppdb.df['HETATM']['residue_name'] == 'BMA')| 
                  (ppdb.df['HETATM']['residue_name'] == 'NAG')]

sugar_atoms = sugar_atoms.loc[:, 'atom_number'].tolist()
sugar_atoms = map(str, sugar_atoms)


entry = ppdb.df['OTHERS'][ppdb.df['OTHERS']['record_name']=='CONECT'].loc[:,'entry'].str.split(expand = True)
a = entry.isin(sugar_atoms)
a = a[0]|a[1]|a[2]|a[3]   #put all cols together, and if any col == True, then the whole column is True for a

ppdb.df['OTHERS'][ppdb.df['OTHERS']['record_name'] == 'CONECT'] = ppdb.df['OTHERS'][ppdb.df['OTHERS']['record_name'] == 'CONECT'][a]   
#basically the way the indexing in the biopandas works is a bit odd, so you have to be very specific what you are replacing. [a] is either true or false
# so what comes out of this is either Nan or a value. So we drop the nans below
ppdb.df['OTHERS'] = ppdb.df['OTHERS'].dropna()

### entry= find in OTHERS where record_name is CONECT, (will return True and False so this is why you need the first ppdb.df["OTHERS"] to get indexing)
### and then locate 'entry' in there because that is all we need. And split this on the whitespace. I did a bit of editing in sublime text to split each 
### since if the entry was len(5) it was smushed together like CONECT100411212435235 instead of CONECT 10041 12124 45235


ppdb.to_pdb(path='./EeNav_conect_sugar_only.pdb', 
            records=None, 
            gz=False, 
            append_newline=True)







#ppdb.df['OTHERS']['entry'].str.extract('(.{1,5})' * 2, expand = True)


#ppdb.df['OTHERS'][ppdb.df['OTHERS']['record_name'] == 'CONECT']


#ppdb.df['OTHERS']['new'] = new


#entry = ppdb.df['OTHERS'] #.loc[:,'entry'].str.split(expand = True)
