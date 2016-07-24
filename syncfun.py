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
import re

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

def func_exist( buf, key ):
	# check if func exists.
	if len(buf):
		for line in buf:
			if key in line:
				return True
	return False

def sync_func_declare(buffer, key, path):

	if os.path.isfile(path):
		file = open(path, "r")
		lines = file.readlines()
		file.close()

		# pass 1
    # check if func exists.
		found=func_exist(buffer, key)

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

def replace_class_name( key, ori, buf ):
	#search function in file
	for line in buf:
		# :: in string
		# ; NOT in string
		# white space is first position
		# this is the first line of function.
		if ( ("::" in line) and (";" not in line) and (0 != line.index(' ')) ):
			# get white space position
			widx = line.index(' ')
			widx+=1
			# get "::" position
			double_colon_idx = line.index('::')
			# get sub string
			new_class_name=line[widx:double_colon_idx]

			widx=ori.index(' ')
			widx+=1
			double_colon_idx = ori.index('::')
			old_class_name=ori[widx:double_colon_idx]
	
			new_func = re.sub(old_class_name ,new_class_name, ori)
			return new_func

def sync_func_define(buf, key, path):

	if os.path.isfile(path):
		file = open(path, 'r')
		lines = file.readlines()

		#Pass 1 
		#Check if function is in file
		found=func_exist(lines, key)

		#Pass 2
		#Create tmp file and record.
		tmpfile=open("tmp.cpp", "w+")

		# record class name, replace class name to buffer
		buf[0] = replace_class_name(key, buf[0], lines)

		# if function already exist, replace to origin file
		# else put this function to the end of file.

		if found:
			func_is_fund=False
			func_scope_start=False
			func_scope_end=False

			print "Func exists"
			for line in lines:
				skip = False

				if (key in line) and (not func_is_fund):
					func_is_fund=True
					func_scope_start=True
					skip = True
					for buf_line in buf:
						tmpfile.write(buf_line)

				if func_scope_start and (not func_scope_end ):
					skip = True
					if ("}" in line) and (0 == line.index("}")):
						func_scope_end = True
					
				if not skip:
					tmpfile.write(line)
		else:
			# record class name, replace class name to buffer
			# put this function to the end of file.
			for line in lines:
				tmpfile.write(line)
			tmpfile.write("\n")
			for line in buf:
				tmpfile.write(line)
		tmpfile.close()
		os.rename("tmp.cpp", path)

# main

#open source file and copy source function by searchkey
buf = ""
searchKey = ""

# sync .h files
sourcePath = ""
targetPath = ""
#sync .cpp files


buf = cache_souce_function(searchKey, sourcePath)

if is_define:
	sync_func_declare( buf, searchKey, targetPath)
else:
	sync_func_define (buf, searchKey, targetPath)

