#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.Utility.tools as tools

import optparse
import os
import sys
import subprocess
import re

srmpath = 'srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN='


def confirm(prompt=None, default=False):
	"""Prompts for yes or no response from the user. Returns True for yes and
	False for no.
	'resp' should be set to the default value assumed by the caller when
	user simply types ENTER.
	"""

	if prompt == None:
		prompt = 'Delete folder?'

	if default:
		prompt = '%s [%s]|%s: ' % (prompt, 'YES', 'no')
	else:
		prompt = '%s %s|[%s]: ' % (prompt, 'yes', 'NO')

	while True:
		answer = raw_input(prompt)
		if not answer:
			return default
		if answer not in ['yes', 'YES', 'y', 'Y', 'no', 'NO', 'n', 'N']:
			print 'please enter yes or no.'
			continue
		if answer.lower() == 'yes' or answer.lower() == 'y':
			return True
		if answer.lower() == 'no' or answer.lower() == 'n':
			return False

def dirWalkAndDelete(currentPath, options):
	currentPath = currentPath if not currentPath.endswith('/') else currentPath[:-1]
	bashCommand = 'srmls -count=9999 ' + srmpath + '{}'.format(currentPath)
	print bashCommand
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	# srmlsrc = process.returncode
	# log.debug(output)
	subfolderDirsAndFiles = output.split()
	lenListsubfolderDirsAndFiles = len(subfolderDirsAndFiles)
	offset = 9999

	while lenListsubfolderDirsAndFiles%20000 == 0 and lenListsubfolderDirsAndFiles > 0:
		bashCommand = 'srmls -count=9999 -offset={} '.format(offset) + srmpath + '{}'.format(currentPath)
		print bashCommand
		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()
		# srmlsrc = process.returncode
		# log.debug(output)
		subfolderDirsAndFilesExtended = output.split()
		subfolderDirsAndFiles.extend(subfolderDirsAndFilesExtended)
		lenListsubfolderDirsAndFiles = len(subfolderDirsAndFiles)
		if lenListsubfolderDirsAndFiles%20000 != 0:
			break
		else:
			offset += 9999

	subfolderDirsAndFilesSorted = sorted([x if not x.endswith('//') else x[:-1] for x in subfolderDirsAndFiles if not unicode(x, "utf-8").isnumeric()], key = lambda ele: -ele.count("/"))
	# sort files to the top of the list to prevent failure of non-empty folder deletion
	for index, dirOrFile in enumerate(subfolderDirsAndFilesSorted):
		# regex to find paths with file extensions 1 to 4 characters long
		if re.search('\.[a-zA-Z0-9]{1,4}$', dirOrFile):
			filesToDelete.append(dirOrFile)
			# subfolderDirsAndFilesSorted.insert(0, subfolderDirsAndFilesSorted.pop(index))
		elif dirOrFile.endswith('/') and dirOrFile not in foldersToDelete:
			foldersToDelete.append(dirOrFile)

	if len(filesToDelete) > 0:
		args = [[file, options] for file in filesToDelete]
		n_cores = min(len(args), options.n_cores)
		if options.force or options.dry_run:
			returnvalues = tools.parallelize(deleteFolderOrFile, args, n_cores, description='deleting Files')
			for index, value in enumerate(returnvalues[::-1]):
				if value[0] == 0 or value[0] == 2: # NOTE: deleted files have value 0, failed deletions 1 and skipped files 2
					del filesToDelete[len(returnvalues) - index - 1]
		else:
			for arg in args:
				index = deleteFolderOrFile(arg)
				del filesToDelete[index]

	# deleteFoldersAndFiles(subfolderDirsAndFilesSorted, options)

	subfolderDirsSorted = sorted([x for x in subfolderDirsAndFilesSorted if x.endswith('/')], key = lambda ele: -ele.count("/"))
	if len(subfolderDirsSorted) > 0:
		subfolderDirsSorted.pop()
		for folder in subfolderDirsSorted:
			dirWalkAndDelete(folder, options)

def deleteFolderOrFile(args):
	dirOrFile = args[0]
	options = args[1]
	# srmrm return code
	srmrmrc = 1
	# srmrmdir return code
	srmrmdirrc = 1
	filestypesToDelete = ()
	if not options.delete_rootfiles_only and not options.delete_logfiles_only:
		filestypesToDelete = ('.root', '.log', '.tar.gz')
	elif options.delete_rootfiles_only:
		filestypesToDelete = ('.root')
	elif options.delete_logfiles_only:
		filestypesToDelete = ('.log', '.tar.gz')
	if dirOrFile.startswith('/'):
		delete = False if options.dry_run else (True if options.force else confirm('\tdelete folder or file {} ?'.format(options.folder + dirOrFile), False))
		if dirOrFile.endswith(filestypesToDelete):
			if delete:
				deleteCommand = 'srmrm ' + srmpath + '{}'.format(dirOrFile)
				print deleteCommand
				deleteProcess = subprocess.Popen(deleteCommand.split(), stdout=subprocess.PIPE)
				deleteOutput, deleteError = deleteProcess.communicate()
				srmrmrc = deleteProcess.returncode
				if deleteProcess.returncode:
					print 'failed to delete {}'.format(dirOrFile)
				else:
					print 'deleted {}'.format(dirOrFile)
			else:
				print 'not deleting {}'.format(dirOrFile)
		elif dirOrFile.endswith('/'):
			lsCommand = 'srmls -count=9999 ' + srmpath + '{}'.format(dirOrFile)
			print lsCommand
			lsProcess = subprocess.Popen(lsCommand.split(), stdout=subprocess.PIPE)
			lsOutput, lsError = lsProcess.communicate()
			srmlsrc = lsProcess.returncode
			if len(lsOutput.split()) == 2: # NOTE: len == 2 means the folder has no subfolders or files and can be deleted. output[0] is the size if the folder and output[1] is the path of the folder
				if delete:
					deleteCommand = 'srmrmdir ' + srmpath + '{}'.format(dirOrFile)
					print deleteCommand
					deleteProcess = subprocess.Popen(deleteCommand.split(), stdout=subprocess.PIPE)
					deleteOutput, deleteError = deleteProcess.communicate()
					srmrmdirrc = deleteProcess.returncode
					if deleteProcess.returncode:
						print 'failed to delete {}. Folder probably not empty'.format(dirOrFile)
					else:
						print 'deleted {}'.format(dirOrFile)
						foldersToDelete.remove(dirOrFile)
				else:
					print 'not deleting {}'.format(dirOrFile)
		else:
			print 'File type not caught. Skipping {}'.format(dirOrFile)
			srmrmc = 2
	return srmrmrc, srmrmdirrc

def deleteFoldersAndFiles(subfolderDirsAndFilesSorted, options, tries=0):
	# srmrm return code sum
	srmrmrc = 0
	# srmrmdir return code sum
	srmrmdirrc = 0
	for dirOrFile in subfolderDirsAndFilesSorted:
		output = deleteFolderOrFile([dirOrFile, options])
		srmrmrc += output[0]
		srmrmdirrc += output[1]
	if srmrmrc == 0 and srmrmdirrc == 0:
		print 'Deleted everything successfully.'
	else:
		print 'Failed to delete {0} folders and {1} files.'.format(srmrmdirrc, srmrmrc)
		# tryAgain = True if options.force else confirm('\tTry again?', False)
		# if tryAgain:
		# 	if options.force and tries >= options.recursion_depth:
		# 		return
		# 	tries += 1
		# 	deleteFoldersAndFiles(subfolderDirsAndFilesSorted, options, tries)

def main():

	parser = optparse.OptionParser(usage="usage: %prog [options]",
	                               description="Script to delete a skim folder using dCache commands.")

	# folder
	parser.add_option("-f", "--folder", help="skim folder to be deleted, in the form: /pnfs/desy.de/cms/tier2/store/user/user_name/folder", default = None)
	# force
	parser.add_option("--force", action="store_true", help="forces deletion without asking for confirmation, use with care!", default = False)
	# dry run, just doing ls and not deleting anything
	parser.add_option("--dry-run", action="store_true", help="do a dry-run and not actually delete anything. Just does 'ls' on all files to be deleted outside of a dry-run", default = False)
	# set srmls -recursion-depth option
	parser.add_option("--recursion-depth", type = int, default = 1, help="set the recursion depth for subfolders. [Default: %(default)s]")
	# number of cores for files deletion parallelization
	parser.add_option("-n", "--n-cores", type = int, default = 4, help="set the number of cores for file deletion parallelization. [Default: %(default)s]")

	group = optparse.OptionGroup(parser, "File ending options")
	# delete log files
	group.add_option("--delete-logfiles-only", action="store_true", help="only delete log files and tarballs", default = False)
	# delete root riles
	group.add_option("--delete-rootfiles-only", action="store_true", help="only delete root files", default = False)
	parser.add_option_group(group)

	(options, args) = parser.parse_args()

	if options.delete_logfiles_only and options.delete_rootfiles_only:
		parser.error("options --delete-logfiles-only and --delete-rootfiles-only are mutually exclusive.")

	if options.folder == None:
		parser.error('no folder given...exiting.')

	print 'trying to delete skim folder: {}\n'.format(options.folder)

	# just do recursion_depth 10 for now. should be more than enough to get everything
	# # NOTE: this will not work when output of srmls is larger than 10k. Have to adapt to way it is done in folderSizedCache.py
	recursion_depth = options.recursion_depth
	bashCommand = 'srmls -recursion_depth={1} "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN={0}"'.format(options.folder, recursion_depth)

	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	srmlsrc = process.returncode
	if srmlsrc:
		print 'Folder does not exist.'
		sys.exit(1)
	# log.debug(output)
	subfolderDirsAndFiles = output.split()

	global filesToDelete
	filesToDelete = []
	global foldersToDelete
	foldersToDelete = []

	# attempts = 0
	dirWalkAndDelete(options.folder, options)

	if not (options.delete_logfiles_only or options.delete_rootfiles_only):
		if len(filesToDelete) == 0 and len(foldersToDelete) > 0:
			foldersToDeleteCopy = sorted([x for x in foldersToDelete], key = lambda ele: -ele.count("/"))

			for folder in foldersToDeleteCopy:
				print 'deleting', folder
				deleteFolderOrFile([folder, options])

		if len(filesToDelete) == 0 and len(foldersToDelete) == 1:
			deleteFolderOrFile([options.folder + '/', options])
	print 'exiting.'

if __name__ == "__main__":
	main()
