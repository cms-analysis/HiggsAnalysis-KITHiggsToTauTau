#!/usr/bin/env python
import gfal2


class gfal_filelist():
	def __init__(self, gridpath, out_file_name='test.txt' ,file_prefix='dcap://dcache-cms-dcap.desy.de/', create_by_init=True):
		self.gridpath = gridpath
		self.out_file_name = out_file_name
		self.file_prefix = file_prefix
		self.files = []
		if create_by_init:
			self.list_files()
			self.write_file()

	def list_files(self, akt_grid_path = None):
		#Also posibble to add subfolder herer
		ctxt = gfal2.creat_context()
		if not akt_grid_path:
			akt_grid_path = self.gridpath
		try:
			listdir = ctxt.listdir(akt_grid_path)
		except:
			print "could not excute \ngfal-ls ",akt_grid_path,"\nShoure that this folder exists"
			return
		for f in listdir:
			if f.endswith('.root'):
				self.files.append(akt_grid_path.rstrip('/')+'/' + f)

	def write_file(self):
		if not self.files:
			print "List files is empty there no file for this gridpath could be crated \n",gridpath
			return 
		with open(self.out_file_name, 'w') as outfile:
			for akt_file in self.files:
				akt_file_output = akt_file.split('=')[-1]
				if self.file_prefix:
					akt_file_output = self.file_prefix+akt_file_output
				outfile.write(akt_file_output+'\n')
			

for akt_f in ['Embedding2016B','Embedding2016C','Embedding2016D','Embedding2016E','Embedding2016F','Embedding2016G']:
	gridpath = 'srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/swayand/Kappa_skimm_v5/TauEmbedding_'+akt_f+'_PromptRecov2_13TeV_MINIAOD' 
#	gfal_filelist(gridpath=gridpath, out_file_name=akt_f+"_files_MuTau.txt", file_prefix='root://dcache-cms-xrootd.desy.de:1094/')
	gfal_filelist(gridpath=gridpath, out_file_name=akt_f+"_files_MuTau.txt")



