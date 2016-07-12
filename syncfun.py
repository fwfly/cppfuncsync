# Targe is to search function name in file.
# keyword is default.
# read file and compare every string in file.
# return "Found it in line <num>" if found this string
# retrun "Error There is no function <Keyword>"
# To do :
#  find put pos in target file.
#  func define need to modify class name.
#  Handle duplicate function.

import os.path
import os

is_define = False

def cache_souce_function( key, path ):
	buffer = []
	file = open(path, 'rw')
	lines = file.readlines();
	file.close()

	found = False
	end_func = False
	for line in lines :
		if (not found) and (key in line) :
			found = True
			buffer.append(line)
			if ";" not in line :
				is_define = True
			else:
				break
		elif found and is_define and not end_func:
			# get function body
			if ('}' in line) and (0 == line.index('}')):
				end_func = True
			buffer.append(line)
    
	return buffer

def sync_func_declare(buffer, key, path):

	if os.path.isfile(path):
		file = open(path, "r")
		lines = file.readlines()
		file.close()
		found=False

		# pass 1
    # check if func exists.
		if len(lines):
			for line in lines:
				if key in line:
					found = True
					break

		# pass 2 
    # create tmp file
		# recode line to tmp file
		tmpfile = open("tmpfile.h", "w+")
		if found :
			for line in lines:
				if key in line:
					tmpfile.write(buffer[0])
				else:
					tmpfile.write(line)
		else :
			# find public scope
			# put func to end of public scope
			# skip win32 define
			in_public_scope = False
			end_public_scope = False
			func_in_file = False
			for line in lines:
				if not func_in_file:
					if "public:" in line:
						in_public_scope = True
						print "public scope"
					if in_public_scope:
						#start to search end of scope
						if "private:" in line:
							end_public_scope = True
						elif ("};" in line) and (0 == line.index('}')) :
							end_public_scope = True
						if end_public_scope:
							tmpfile.write(buffer[0])
							func_in_file = True
				tmpfile.write(line)
		tmpfile.close()
		os.rename("tmpfile.h", path)
	else:
		print "File can't be found : %s " % path

def sync_func_declare(buffer, key, path)
	if os.path.isfile(path):
		file = open(path, "r")
		lines = file.readlines()
		file.close()
		found=False

		# pass 1
    # check if func exists.
		if len(lines):
			for line in lines:
				if key in line:
					found = True
					break

		if found:
			print "%s is in file"

		
# main

#open source file and copy source function by searchkey
buffer = ""
searchKey = ""

# sync .h files
sourcePath = ""
targetPath = ""

#sync .cpp files


buffer = cache_souce_function(searchKey, sourcePath)

if is_define:
	sync_func_declare( buffer, searchKey, targetPath)
else:
	sync_func_declare( buffer, searchKey, targetPath)
 


