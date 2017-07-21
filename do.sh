ef='entropy.dat'
in4='../Marina_USB/seqs/pdbfiles/segments_from_MSA_and_cluster.pdb'
out='../Marina_USB/seqs/pdbfiles/segments_from_MSA_and_cluster_entropy.pdb'
rm er

awk '{print substr($0,23,4)}' $in4 > tt

i=0

a=""

while read line ; do
    if [ "$line" = "$a" ] ; then
        b=`head -n $i $ef | tail -n 1`
        echo $b >> er
    else
        i=$(($i+1))
        b=`head -n $i $ef | tail -n 1`
        echo $b >> er
        a=$line
    fi

done < tt

awk '{print substr($0,1,54)}' $in4 > tt2

paste tt2 er | awk '{printf "%s  %s%7.3f\n", substr($0,1,54), "1.00",  substr($0,55,8)*10}' > $out

rm tt tt2 er
