# This file is a inteface.
# When user execute this file. It will read a configure file to sync function.
# configure formate is below:
# SOURCE=<file name>     
# KEY=<function pattern> # the function you want to sync
# TARGET=<file name...>  # You can get multiple target here, splite by white space.

import sys
import os.path
import syncfun

CFG_SYMBOL_KEY="KEY"
CFG_SYMBOL_SOURCE="SOURCE"
CFG_SYMBOL_TARGET="TARGET"


#input : file path
#output : list of tasks
def create_tasks_by_a_file(cfg_file):
	#read lines
	tmp_file = open(cfg_file, 'r')
	lines = tmp_file.readlines()
	tmp_file.close()

	tasks=[]
	#task : dict
	#{
	#  key : string
	#  source : string
  #  targets : list
	#}

	#Parse cfg file
	key=""
	source=""
	targets=[]
	task = {
		'key':"",
		'source':"",
		'targets':[]
	}
	for line in lines:
		#Parser

		# remove new line tag '\n'
		line=line[:-1]

		if (CFG_SYMBOL_SOURCE in line) and (0 == line.index(CFG_SYMBOL_SOURCE)):
			symbol_equal_idx = line.index('=') + 1
			source = line[symbol_equal_idx : ]
			task['source'] = source
			task['targets'] = []
		elif (CFG_SYMBOL_KEY in line) and (0 == line.index(CFG_SYMBOL_KEY)):
			symbol_equal_idx = line.index('=') + 1
			key = line[symbol_equal_idx : ]	
			task['key'] = key
		elif (CFG_SYMBOL_TARGET in line) and (0 == line.index(CFG_SYMBOL_TARGET)):

			symbol_equal_idx = line.index('=') + 1
			task['targets'].append(line[symbol_equal_idx : ])

	tasks.append(task)
	return tasks

# read config files.
# build each task and push into queue.
# return taks queue.
def build_task_queue():
	args = sys.argv
	argc = len(args)
	if 1 == argc:
		print "Error : There is no any input file."
		exit()
	else:
		task_queue = []
		args.pop(0) # remove cmd
		for arg in args:
			if os.path.isfile(arg):
				# Read lines and parse configure.
				tasks = create_tasks_by_a_file(arg)

				# Add tasks to task_queue
				task_queue.extend(tasks)
			else:
				print "Error : No such file %s"% arg

	return task_queue

# execute task in queue
def process_tasks(queue):
	for task in queue:
		for target in task['targets']:
			syncfun.process_sync_func( task['source'], task['key'], target  )


tasks_queue = build_task_queue()
process_tasks(tasks_queue)

