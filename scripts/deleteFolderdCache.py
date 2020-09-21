#! /usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
import os
import sys

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
		if answer not in ['yes', 'YES', 'no', 'NO']:
			print 'please enter yes or no.'
			continue
		if answer == 'yes' or answer == 'YES':
			return True
		if answer == 'no' or answer == 'NO':
			return False


def main():

	parser = optparse.OptionParser(usage="usage: %prog [options]",
	                               description="Script to delete a skim folder using dCache commands.")

	# folder
	parser.add_option("-f", "--folder", help="skim folder to be deleted, in the form: /pnfs/desy.de/cms/tier2/store/user/user_name/folder", default = None)
	#force
	parser.add_option("--force", action="store_true", help="forces deletion without asking for confirmation, use with care!", default = False)

	(options, args) = parser.parse_args()
	
	if options.folder == None:
		print 'no folder given...exiting.'
		sys.exit(1)

	print 'trying to delete skim folder: {}\n'.format(options.folder)

	subfolderDirs = []
	for root, subdirs, files in os.walk(options.folder):
		for subdir in subdirs:
			subfolderDirs.append(os.path.join(root, subdir))
	
	# move backwards, from the most internal directory
	for subdir in subfolderDirs[::-1]:
		print '\tfound subfolder {}'.format(subdir)
		delete = True if options.force else confirm('\tdelete folder {} ?'.format(options.folder + '/' + subdir), False)

		if delete:
			for file in os.listdir(subdir):
				# command = 'lcg-del -b -l -T srmv2 "srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN={0}/{1}"'.format(subdir, file)
				command = 'srmls "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN={0}/{1}"'.format(subdir, file)
				os.system(command)

			print '\tcontent of subfolder {} deleted.'.format(subdir)
			print '\tsubfolder now empty...deleting.'
			# command = 'srmrmdir "srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN={0}"'.format(subdir)
			command = 'srmls "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN={0}"'.format(subdir)
			os.system(command)

		else:
			print '\tnothing done.'


	subfolderDirs = os.listdir(options.folder)
	if len(subfolderDirs) == 0:
		print '\n\nfolder {} is empty...delete it?'.format(options.folder)
		delete = confirm('', False)

		if delete:
			# command = 'srmrmdir "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN={0}"'.format(options.folder)
			command = 'srmls "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN={0}"'.format(options.folder)
			os.system(command)

		else:
			print '\tnothing done.'

	print 'exiting.'


if __name__ == "__main__":
	main()
