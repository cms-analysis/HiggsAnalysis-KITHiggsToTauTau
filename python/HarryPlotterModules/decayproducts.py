#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import Artus.HarryPlotter.harrycore as harrycore
import Artus.HarryPlotter.plot1d as plot1d
import Artus.HarryPlotter.tools.utils as utils
import Artus.HarryPlotter.tools.labels as labels
import Artus.HarryPlotter.tools.mplconvert as mplconvert

particledict = {
	  25: r'Higgs',
	  22: r'$\gamma$',
      -20213: r'$a_1(1260)^-$',
       20213: r'$a_1(1260)^+$',
	-323: r'$K^*(892)^-$',
	 323: r'$K^*(892)^+$',
	-321: r'$K^-$',
	 321: r'$K^+$',
	-213: r'$\rho (770)^-$',
	 213: r'$\rho (770)^+$',
	-211: r'$\pi ^-$',
	 211: r'$\pi ^+$',
	 -24: r'$W^-$',
	  24: r'$W^+$',
	  15: r'$\tau ^-$',
	 -15: r'$\tau ^+$',
          13: r'$\mu ^-$',
         -13: r'$\mu ^+$',
	  11: r'$e^-$',
	 -11: r'$e^+$',
	  12: r'$\nu_e$',
	 -12: r'$\bar{\nu_e}$',
	  14: r'$\nu_{\mu}$',
	 -14: r'$\bar{\nu_{\mu}}$',
	  16: r'$\nu_{\tau}$',
	 -16: r'$\bar{\nu_{\tau}}$',	

	}

def decayproducts(plotdict):
	""" Write here what this function does
	"""
	plotdict['xlims'] = [-20300.5, 20299.5]
	plotdict['nbins'] = 40600
	

	plot1d.get_root_histos(plotdict)
	plot1d.get_mpl_histos(plotdict)
	# remove empty bins
	# map  plotdict["mplhistos"]  x entries (=pdgIDs) to particle names
	# regroup

	pdgids=[-20213,20213,-323,323,-321,321,-213,213,-211,211,-24,24,11,-11,13,-13]
	for i in range(len(plotdict["mplhistos"])):
		for xc,y in zip(plotdict["mplhistos"][i].xc,plotdict["mplhistos"][i].y):
			if (y!=0) and not (xc in pdgids) and (xc!=0):
				print "PdgId %5.0f is not contained in the list 'pdgids'"%xc 
				sys.exit(1)   
		
	binlabelslist = [particledict.get(p) for p in pdgids]


	for i in range(len(plotdict["mplhistos"])):
		new_y=[0]*len(pdgids)
		new_yerr=[0]*len(pdgids)
		for j in range(len(pdgids)):
			for xc,y,yerr in zip(plotdict["mplhistos"][i].xc,plotdict["mplhistos"][i].y,plotdict["mplhistos"][i].yerr):
				if pdgids[j]==xc:
					new_y[j]=y
					new_yerr[j]=yerr
		numblist =  range(len(pdgids))
		for k in numblist:
			numblist[k]-=0.5
		plotdict["mplhistos"][i].x =  numblist
		plotdict["mplhistos"][i].xc = range(len(pdgids))
		plotdict["mplhistos"][i].y = new_y
		plotdict["mplhistos"][i].yerr = new_yerr

	plot1d.plot1d_mpl(plotdict) #plottet mplhistos

	# set x axis ticks, ticklabels
	plotdict['axes'].set_ylim(top= 1.2 * max(d.ymax() for d in plotdict['mplhistos']), bottom = 0)
	labels.add_labels(plotdict)
	plotdict["axes"].set_xticks(range(len(pdgids)))
	plotdict["axes"].set_xticklabels(binlabelslist, rotation=90)
	utils.save(plotdict)

