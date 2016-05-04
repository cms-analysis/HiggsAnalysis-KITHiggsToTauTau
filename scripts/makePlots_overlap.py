#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import glob
import ROOT
import matplotlib.pyplot as plt

def plot_overlap(vbf, ggh, file_path="Testfile"):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	c1_left=[]
	c1_width=[]
	c1_bottom=[]
	c1_height=[]
	c2_left=[]
	c2_width=[]
	c2_bottom=[]
	c2_height=[]
	c3_width=[]
	ax.set_xlim(-1, max(3+sum(ggh),3+sum(vbf)))
	right_border = max(2+sum(ggh),2+sum(vbf))
	for i,tups in enumerate([vbf, ggh]):
		c1_left.append(1)
		c1_width.append(tups[0]+tups[2])
		c1_bottom.append(2*i+0.5)
		c1_height.append(1)
		c2_left.append(1+tups[0])
		c2_width.append(tups[1]+tups[2])
		c3_width.append(tups[2])
		ax.annotate("%1.2f"%tups[0], xy=(0, 2*i+1),)
		ax.annotate("%1.2f"%tups[1], xy=(1.5+sum(tups), 2*i+1),)
		ax.annotate("%1.2f"%tups[2], xy=(1+tups[0]+0.5*tups[2], 2*i+1))

	ax.barh(left=c1_left, width=c1_width, bottom=c1_bottom, height=c1_height, edgecolor = "blue", facecolor="none", label="classic")
	ax.barh(left=c2_left,width=c2_width, bottom=c1_bottom, height=c1_height, edgecolor = "red", facecolor="none", label="vbf tagger")
	ax.barh(left=c2_left,width=c3_width, bottom=c1_bottom, height=c1_height, edgecolor = "none", facecolor="green", hatch="/", alpha=0.15, label="overlap", zorder=1)
	ax.set_yticks([1,3])
	ax.set_yticklabels(["VBF", "ggH"], size='x-large', va='center', ha='right', rotation_mode='anchor')


	ax.set_ylim(0, 4)
	ax.set_ylabel("")
	ax.set_xlabel("")
	ax.legend(loc="best")
	plt.tight_layout()
	plt.savefig("%s.png"%file_path)
	log.info("create plot %s.png"%file_path)
	plt.savefig("%s.pdf"%file_path)
	log.info("create plot %s.pdf"%file_path)
	plt.savefig("%s.eps"%file_path)
	log.info("create plot %s.eps"%file_path)


if __name__ == "__main__":
	plot_overlap((1.5,2.5,5), (2.5, 0.5,3))