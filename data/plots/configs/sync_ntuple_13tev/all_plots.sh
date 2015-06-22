for f in plots/*.json
do
 echo "Processing $f"
 harry.py -j $f $1  -i miniaod.root cern.root --folders tt/ntuple tree --labels "KIT miniAOD" "CERN miniAOD" --export-json /dev/null
done

