import numpy as np
import sys
import os
import re

if (len(sys.argv) < 4):
	print "Usage: python vtr_fs_sweep.py arch_file range increment"
	sys.exit()

arch_file = sys.argv[1]
sweep_range = sys.argv[2]
increment = sys.argv[3]

print "Architecture file: " + arch_file
print "Parameter: fs"
print "Sweep range: " + sweep_range
print "Increment: " + increment

if not os.path.isfile(arch_file):
	print "Error: '" + arch_file + "' does not exist."
	sys.exit()

sweep_range_list = sweep_range.split("-")

if (len(sweep_range_list) != 2):
	print "Error: Invalid sweep range."
	sys.exit()

if (increment.isdigit() == False):
	print "Error: Invalid increment specified."
	sys.exit()

start = sweep_range_list[0]
end = sweep_range_list[1]

arch = open(os.path.realpath(arch_file))

# Grab the default value of fs, then start generating new arch_files

lines = arch.readlines()
fs = 0

for l in lines:
	if re.search("fs=", l):
		fs = l.split('"')[3]

# Sanity check, check default arch_file name with default arch_file parameter

range_list = []
increment_check = float(increment)

if re.search("fs" + fs, arch_file):
	if (increment_check < 1):
		range_list = np.arange(float(start), float(end) + float(increment), float(increment))
	else:
		range_list = np.arange(int(start), int(end) + 1, int(increment))
else:
	print "Error: Invalid default arch_file name, for specified parameter."
	sys.exit()

# Loop through range_list

for i in range_list:
	if (i != int(fs)):
		new_arch_file = arch_file.replace(fs, str(i))

		print new_arch_file

		new_arch = open(new_arch_file, "w")

		arch.seek(0)

		lines = arch.readlines()

		for l in lines:
			if re.search("fs=", l):
				new_arch.write(l.replace(fs, str(i)).rstrip() + "\n")
			else:
				new_arch.write(l.rstrip() + "\n")

		new_arch.close()

arch.close()

sys.exit()
