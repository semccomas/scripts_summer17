***
**readme file for scripts summer 2017**
***

* [finding_insects_ipython.py](https://github.com/semccomas/scripts_summer17/blob/master/finding_insects_ipython.py) searches the [speclist](http://www.uniprot.org/docs/speclist) at uniprot for
the insect taxonomy using [the insecta taxonomy group](http://www.uniprot.org/taxonomy/?query=ancestor%3a50557) also from uniprot. This then finds the insects in the MSA file using the 'common
name' from the uniprot speclist and saves the output in the same format as the MSA file ('>blahblah \n alignment info)

*[extract_dendroscope.py](https://github.com/semccomas/scripts_summer17/blob/master/extract_dendroscope_match_fasta.py) takes the output of the dendroscope channel selection and find the matching fasta, giving sodium channels and the ones closest pyhlogenetically in it 

*pdb matching file is a total mess but have at it. Was supposed to parse the PDB file to cut only segments out that match from the MSA but the numbering was off and I could not figure out how to get BioPython to extract files after a certain number


*dx.py calculates the electrostatic potential for 3 different applied electric fields (exists in Marina_USB/electric_field) for each voltage sensor domain based on where the domain is in the .gro file

*docking.sh will do docking for a given ligand, receptor, and grid. The directory and ligand and receptor must be specified, but beyond that the ligand/ receptor will be converted from .pdb to .pdbqt and autodock vina will be run, the ligands will be converted back to pdb for reading in VMD. Its just to load the receptor and ligands into vmd to see the docking status. 

*do.sh and shannon.entropy.Sarah.py calculate entropy for the MSA's. the .py script makes an entropy.dat file, one line for each column in the MSA. This tells how conserved the elements of the sequence is. Do.sh then takes this to the pdb file and gives each residue in there (=> the MSA AND THE PDB FILE MUST MATCH EXACTLY!!!!) the corresponding entropy. This can then be visualized in the VMD with 'Beta' coloring option. Red means more conserved and blue means less conserved

*sugars_only.py is from 31 July. This takes only the sugars of the pdb file and keeps only those CONECT lines
