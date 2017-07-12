## this file will compare the output from the dendoscope where we got only the sodium or calcium channels to the fasta file. We will find the matching labels and make a new fasta file with only sodium or only calcium channels

#sodium = open('../Marina_USB/seqs/trees/sodium_only.nexml').read().splitlines()
sodium = open('../Marina_USB/seqs/trees/calcium_only_total.nexml').read().splitlines()
fasta = open('../Marina_USB/seqs/nogaps_iter2.final.fa').read()

label = [] 
for line in sodium:
	line = line.split()
	try:
		if 'label' in line[2] and len(line[2]) > 15:
			l = line[2].split('|')
			label.append(l[1])
	except IndexError:
		pass
'''
fasta_label = [] 
fasta_splitline = fasta.split('\n')
for line in fasta_splitline:
	if '>' in line:
		if 'PSEUDO' in line:
			line = line.split('_')
			fasta_label.append(line[0][1:])
		else:
			line = line.split('|')
			fasta_label.append(line[1]) 

'''


f_splitentry = fasta.split('>')   # I do this because the alignments often took longer than one line, so this keeps the alignment in one piece with the text entry 
o = open('../Marina_USB/seqs/calcium_fasta_only.fa', 'w')

m = 0
for line in label:
	for c, l in enumerate(f_splitentry):
		if line in l:
			o.write('>' + l)
 
o.close()


'''
#to check and see if there are any missing files, c should = len after
c= 0
for line in label:
	if line in fasta:
		c = c+ 1
		print line, c, len(label)

'''

