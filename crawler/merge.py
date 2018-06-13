import sys

printed = set()

for fi in sys.argv[1:]:
	fil = open(fi,"r")
	for lin in fil:
		name = lin.strip()
		if name not in printed:
			print(name)
			printed.add(name)
	fil.close()

