#!/usr/bin/python3

import os
import os.path as path
import sys


# If file is there, and a backup does not already exist, copy it to file.backup
def backup_file(backup_path):
	if path.exists(backup_path) and not path.islink(backup_path) and not path.exists(backup_path+".backup"):
		print("File \"{0}\" exists: making backup".format(path.basename(backup_path)))
		os.rename(backup_path, backup_path+".backup")


def make_link(src, dst):
	print("Making link from {0} to {1}".format(src, dst))
	if path.exists(dst):
		os.remove(dst)
	os.symlink(path.join(os.getcwd(), src), dst)


# Given a file containing link info, create links
def create_all_links(list_file):
	with open(list_file, 'r') as conf_file:
		for line in conf_file:
			try:
				src, dst, action = map(lambda s: s.strip(), line.split(' '))
			except ValueError:
				# Not enough values in line
				continue
			src = path.expanduser(src)
			dst = path.expanduser(dst)
			print("\nsrc, dst, action =", src, dst, action)
			
			if action == "link_backup":
				backup_file(dst)
				make_link(src, dst)




if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Provide path to file list")
		sys.exit(1)
	create_all_links(sys.argv[1])


