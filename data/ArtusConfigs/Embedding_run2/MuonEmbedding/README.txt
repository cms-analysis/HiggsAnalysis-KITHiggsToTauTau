#### Performing Muon Embedding for validation.

#### Different tasks for this will be described. Before specific steps in 1) and 2), please perform

HiggsToTauTauAnalysis.py -i artus_input_list_embedded.txt @HiggsAnalysis/KITHiggsToTauTau/data/ArtusWrapperConfigs/MuEmbedded.cfg --nick "embedded"

HiggsToTauTauAnalysis.py -i artus_input_list_selected.txt @HiggsAnalysis/KITHiggsToTauTau/data/ArtusWrapperConfigs/MuEmbedded.cfg --nick "selected"

#### for lists with corresponding kappa datasets. "selected" is derived from the reference MINIAOD dataset, "embedded" from embedded MINIAOD. Now, various validation checks are performed.

#### 1) Input comparison before selection steps, for instance check of first PV position, number of particles etc. Corresponding pipeline config: InputCheck.json

### After the "selected" and "embedded" root files are produced, perform for vertex check:

eventmatching.py selected.root embedded.root -t "input_check/ntuple" -f vertex_check.root

root -l HiggsAnalysis/KITHiggsToTauTau/scripts/EmbeddingVertexCorrection.C

#### 2) Comparison between selected and embedded Z->mumu datasets. Selection ist chosen similar to the one used for embedding. Corresponding pipeline config: ZMuMuSelectionForEmbedding.json


