import subprocess
import xlsxwriter
import sys
import os
import re

if (len(sys.argv) < 2):
	print "Usage: python read_vpr_power.py [directories]"
	sys.exit()

errors = 0
dirs = []
args = sys.argv[1:]

for a in args:
	if a[-1:] != '/':
		a = a + '/'

	if not os.path.isdir(a):
		errors += 1
		print "Error: '" + a + "' is not a directory."
	else:
		dirs.append(a)

if errors > 0:
	sys.exit()

circuits = []

for d in dirs:
	if not os.path.isfile((d + "vpr.out")):
		errors += 1
		print "Error: '" + d + "vpr.out' does not exist."

	if ".v/" in d:
		circuits = d.split(".v/")
		circuits = circuits[0].split("xml/")
		if not os.path.isfile((d + circuits[1] + ".power")):
			errors += 1
			print "Error: '" + d + circuits[1] + ".power' does not exist."
	elif ".blif/" in d:
		circuits = d.split(".blif/")
		circuits = circuits[0].split("xml/")
		if not os.path.isfile((d + circuits[1] + ".power")):
			errors += 1
			print "Error: '" + d + circuits[1] + ".power' does not exist."
	elif "." in d:
		circuits = d.split(".")
		if not os.path.isfile((d + circuits[0] + ".power")):
			errors += 1
			print "Error: '" + d + circuits[0] + ".power' does not exist."
	else:
		circuits = d.split("/")
		if not os.path.isfile((d + circuits[0] + ".power")):
			errors += 1
			print "Error: '" + d + circuits[0] + ".power' does not exist."

if errors > 0:
	sys.exit()

workbook = xlsxwriter.Workbook("vpr_power.xlsx")
worksheet = workbook.add_worksheet()

format = workbook.add_format()
format.set_font_size(10)

row = 0
col = 0

for d in dirs:
	vpr = os.path.realpath(d + "vpr.out")

	print vpr

	if ".v/" in d:
		circuits = d.split(".v/")
		circuits = circuits[0].split("xml/")
		power = os.path.realpath(d + circuits[1] + ".power")
	elif ".blif/" in d:
		circuits = d.split(".blif/")
		circuits = circuits[0].split("xml/")
		power = os.path.realpath(d + circuits[1] + ".power")
	elif "." in d:
		circuits = d.split(".")
		power = os.path.realpath(d + circuits[0] + ".power")
	else:
		circuits = d.split("/")
		power = os.path.realpath(d + circuits[0] + ".power")

	print power

	vprfile = open(vpr)
	vprlines = vprfile.readlines()

	i = 0
	j = 0

	worksheet.set_column(col, col, 30)
	worksheet.set_column(col + 1, col + 1, 20)
	worksheet.write(0, col + 1, circuits[0], format)

	for l in vprlines:
		if re.search("average net length", l):
			worksheet.write(1, col, "average net length", format)
			worksheet.write(1, col + 1, l.split()[6], format)
			print "average net length" + " -> " + l.split()[6]
		if re.search("critical path delay", l):
			worksheet.write(2, col, "critical path delay (" + l.split()[6] + ")", format)
			worksheet.write(2, col + 1, l.split()[5], format)
			print "critical path delay" + " -> " + l.split()[5] + " -> " + l.split()[6]
		if re.search("channel width factor", l):
			if l.split()[8][:-1] == 'o':
				worksheet.write(5, col, "routed channel width", format)
				worksheet.write(5, col + 1, l.split()[9][:-1], format)
				print "routed channel width" + " -> " + l.split()[9][:-1]
			else:
				worksheet.write(5, col, "minimum routable channel width", format)
				worksheet.write(5, col + 1, l.split()[8][:-1], format)
				print "minimum routable channel width" + " -> " + l.split()[8][:-1]

	vprfile.close()

	powerfile = open(power)
	powerlines = powerfile.readlines()

	for l in powerlines:
		if re.search("Routing", l):
			worksheet.write(3, col, "routing power (W)", format)
			worksheet.write(3, col + 1, l.split()[1], format)
			print "Routing Power" + " -> " + l.split()[1] + " -> " + "W"
		if re.search("PB Types", l):
			worksheet.write(4, col, "pb types (W)", format)
			worksheet.write(4, col + 1, l.split()[2], format)
			print "PB Types Power" + " -> " + l.split()[2] + " -> " + "W"

	col += 2

	powerfile.close()

workbook.close()

sys.exit()
