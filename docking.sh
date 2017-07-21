#NOTES:
# the prepare_ligand4.py is not exactly the same and I can't figure out why
# prepare_receptor4.py is the same!! 

directory=/Users/sarahmccomas/Desktop/Summer17/docking/old_ligands/fenvalerate_larger_docking
receptor=cluster_domain1
ligand=fenvalerate

echo 'making ligand file' $ligand 'at' $directory
pythonsh /Library/MGLTools/1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -l $directory/$ligand.pdb -o $directory/$ligand.pdbqt

echo 'making receptor file' $receptor 'at' $directory
pythonsh /Library/MGLTools/1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -r $directory/$receptor.pdb -o $directory/$receptor.pdbqt

echo 'docking...'
~/Desktop/Summer17/docking/autodock_vina_1_1_2_mac/bin/vina --receptor $directory/$receptor.pdbqt --ligand $directory/$ligand.pdbqt --center_x 1.611 --center_y 0.361 --center_z -11.333 --size_x 30 --size_y 16 --size_z 18 --log $directory/$ligand.$receptor.log --out $directory/$ligand.out.pdbqt --num_modes 50 --energy_range 5

#~/Desktop/Summer17/docking/autodock_vina_1_1_2_mac/bin/vina
#~/Desktop/Summer17/docking/autodock_vina_1_1_2_mac/bin/vina_split

#vina


## change the pdbqt output to pdb file
#qt=*.pdbqt 
#for i in $qt;
#do
#	basei=${i%.*}  #strip off file extension
	#echo $basei
#	grep -E '^ATOM' $i > $basei.pdb 
#	echo $i '-->' $basei.pdb
#done


#pythonsh /Library/MGLTools/1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/pdbqt_to_pdb.py -f fenvalerate.pdbqt -o TEST