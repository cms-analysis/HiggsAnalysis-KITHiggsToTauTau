#!/usr/bin/env python
import argparse
import copy
import os
import sys
import logging

def format_number(expr):
	f = float(expr)
	if f == 0.0:
		return "0.000"
	elif 0.1<=abs(f)<100:
		return "{0:.04g}".format(f)
	else:
		n = "{0:.03e}".format(f)
		base = n.split("e")[0]
		exponent = n.split("e")[1]
		return base+"\cdot 10^{"+exponent+"}"

def format_purity(expr):
	return "{0:.01f}\\,\\%".format(float(expr)*100.0)
	
def print_BDT_weight_file(args, input_file, output_file):
	In = open(input_file,"r")
	Out = open(output_file,"w")
	
	Out.write("\\documentclass{article}\n")
	Out.write("\\usepackage{tikz}\n")
	Out.write("\\usetikzlibrary{positioning}\n")
	Out.write("\\begin{document}\n")
	
	variables = []
	tree_active = False
	indentation = 2
	for line in In:
		entries = line.split()
		
		if not tree_active:
			if entries[0]=="<Variable":
				variables.append(entries[3].split("\"")[1])
		
			if entries[0]=="<BinaryTree":
				if int(entries[3].split("\"")[1]) in args.tree_indices:
					#initiate tree graph
					tree_active = True
					Out.write("%Tree No. %i\n")
					Out.write("\\resizebox{\\textwidth}{!}{\n")
					Out.write("\\begin{tikzpicture}[level distance=25mm]\n")
					Out.write("  \\tikzstyle{every node}=[fill=blue!60,rectangle,draw,rounded corners,inner sep=5pt]\n")
					Out.write("  \\tikzstyle{level 1}=[sibling distance=120mm, set style={{every node}+=[fill=blue!45]}]\n")
					Out.write("  \\tikzstyle{level 2}=[sibling distance=60mm, set style={{every node}+=[fill=blue!30]}]\n")
					Out.write("  \\tikzstyle{level 3}=[sibling distance=30mm, set style={{every node}+=[fill=blue!15]}]\n")
		else:
			if entries[0]=="<Node":
				var_index = int(entries[4].split("\"")[1])
				for i in range(indentation): Out.write(" ")
				purity = entries[9].split("\"")[1]
				if args.C:
					x = float(purity)
					if x > 0.5:
						col = ", fill=green!%f"%((x-0.5)*60.0)
					else:
						col = ", fill=red!%f"%((0.5-x)*60.0)
				else:
					col = ""
				if var_index >= 0:
					cut_value = entries[5].split("\"")[1]
					if indentation == 2:
						Out.write("\\node [name=base,align=center%s]{%s: \\\\ $<%s<$}\n"%(col, variables[var_index].replace("_","\\_"), format_number(cut_value)))
					else:
						Out.write("child {node [align=center%s]{S/(S+B): $%s$ \\\\ %s: \\\\ $<%s<$}\n"%(col, format_purity(purity), variables[var_index].replace("_","\\_"), format_number(cut_value)))
					indentation += 2
				else:
					Out.write("child {node [align=center%s]{S/(S+B): \\\\ $%s$}}\n"%(col, format_purity(purity)))
			if entries[0]=="</Node>":
				indentation -= 2
				for i in range(indentation): Out.write(" ")
				if indentation == 2:
					Out.write(";\n")
				else:
					Out.write("}\n")
			
			if entries[0]=="</BinaryTree>":
				if args.C:
					Out.write("  \\node [below = 85mm of base,align=center,left color=red!60,right color=green!60,middle color=white, rounded corners=0cm, draw=none]{$0\\,\\%$ \\hspace{80mm} S/(S+B) \\hspace{80mm} $100\\,\\%$};\n")
				tree_active = False
				Out.write("\\end{tikzpicture}\n")
				Out.write("}\n")
	Out.write("\\end{document}\n")
	In.close()
	Out.close()

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Train BDTs using TMVA interface.")
	parser.add_argument("-i", "--input-files", nargs="+", required=True,
						help="Input file.")
	parser.add_argument("-o", "--output-files", nargs="+", required=False,
						help="Output file. [Default: inputfilename without .weights.xml plus .tex]")
	parser.add_argument("--output-folder", required=False,
						help="Output folder. [Default: same as input]")
	parser.add_argument("-n", "--tree-indices", nargs="+", type=int, required=False,
						default=[0],
						help="index of tree to be printed. [Default: %(default)s]")
	parser.add_argument("-C", "--C", default = False, action="store_true",
						help="node color shows S/(S+B) [Default: %(default)s]")
	args = parser.parse_args()
	for i, filename in enumerate(args.input_files):
		if args.output_files == None:
			output_file = filename.replace(".weights.xml", ".tex")
		else:
			output_file = args.output_files[i]
		if not args.output_folder == None:
			output_file = os.path.join(args.output_folder, os.path.basename(output_file))
		print_BDT_weight_file(args, filename, output_file)

