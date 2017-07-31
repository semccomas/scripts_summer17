#NOTES:
# the prepare_ligand4.py is not exactly the same and I can't figure out why
# prepare_receptor4.py is the same!! 

##################################################
# here are the only thing you have to change 
#
directory=/Users/sarahmccomas/Desktop/Summer17/docking/open_state_docking     #do not add the '/' here!! 
receptor=open_state_aligned_to_closed  #!!! Give these without file extensions for easier naming
ligand=R,R_fenvalerate #!!! Give these without file extensions for easier naming
#
###############################################


output=$ligand.$receptor.out

echo ''
echo 'making ligand file' $ligand 'at' $directory
pythonsh /Library/MGLTools/1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -l $directory/$ligand.pdb -o $directory/$ligand.pdbqt

echo ''
echo 'making receptor file' $receptor 'at' $directory
pythonsh /Library/MGLTools/1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -r $directory/$receptor.pdb -o $directory/$receptor.pdbqt

echo ''
echo 'docking...'
~/Desktop/Summer17/docking/autodock_vina_1_1_2_mac/bin/vina --receptor $directory/$receptor.pdbqt --ligand $directory/$ligand.pdbqt --center_x 126.301 --center_y 146.276 --center_z 131.541 --size_x 28 --size_y 12 --size_z 24 --log $directory/$output.log --out $directory/$output.pdbqt --num_modes 50 --energy_range 5

echo ''
echo 'split docking results'
~/Desktop/Summer17/docking/autodock_vina_1_1_2_mac/bin/vina_split --input $directory/$output.pdbqt --ligand $directory/$output.model

echo ''
for i in $directory/$output.model*.pdbqt;
do 
j=${i%.pdbqt}
echo $i '>> pdb'
pythonsh /Library/MGLTools/1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/pdbqt_to_pdb.py -f $i -o $j.pdb

done


#for P33500 model 45, 27 July --center_x -2.194 --center_y 12.528 --center_z 0.306 --size_x 28 --size_y 12 --size_z 24