
import sys
import csv
import re
import argparse

#Argument Parser
parser = argparse.ArgumentParser(description="Report H or N type from mash output")
parser.add_argument("-s", "--segment", help="Segment to parse (H or N)", choices = ["H", "N"])
parser.add_argument("-c", "--containment", type=float, help="Minimum containment to report (Default = 0.95)", default=0.95)
parser.add_argument("-m", "--multiplicity", type=int, help="Minimum median multiplicity (coverage depth) to report (Default = 10)", default=10)
parser.add_argument("report_files", help="Mash output files to parse", nargs='+')
args = parser.parse_args()
	
	
csvw = csv.writer(sys.stdout, csv.excel_tab, lineterminator='\n')
csvw.writerow(["File", "Primary Type", "Best Hit", "Containment", "Multiplicity", "Minor Types", "Best Hits", "Containments", "Multiplicities"])

for file in args.report_files:
	type_dict = {}
	stem = file.split(sep=".")[0]
	csvr=csv.reader(open(file, 'r'), delimiter = "\t")
	for line in csvr:
		cont = float(line[0].strip())
		mult = int(line[2].strip())
		#taxon = line[5].strip()
		if cont >= args.containment and mult >= args.multiplicity:
			M = None
			t = None
			acc = line[4].split(sep = "_")[0]
			if args.segment == "H":
				M = re.search("[,_]H[1-9][0-9]?", line[4])
				if M:
					t = M.group(0)[1:len(M.group(0))]
				else:
					t = "unknown"
			elif args.segment == "N":
				M = re.search("N[1-9][0-9]?[,_]", line[4])
				if M:
					t = M.group(0)[0:len(M.group(0))-1]
				else:
					t = "unknown"
			else:
				print("Uh oh")
			if t in type_dict.keys():
				if cont > type_dict[t][1]:
					type_dict[t] = [acc, cont, mult]
			else:
				type_dict[t] = [acc, cont, mult]
	
	sorted_types = sorted(type_dict.items(), key=lambda x: x[1][2], reverse=True)
	if len(sorted_types) == 1:
		csvw.writerow([stem, sorted_types[0][0], sorted_types[0][1][0], sorted_types[0][1][1], sorted_types[0][1][2],"None", "NA", "NA", "NA"])
	elif len(sorted_types) == 0:
		csvw.writerow([stem, "None", "NA", "NA", "NA", "None", "NA", "NA", "NA"])
	else:
		m_types = ""
		m_accs = ""
		m_cons = ""
		m_mults = ""
		for i in range(1, len(sorted_types)):
			m_types += str(sorted_types[i][0]) + ";"
			m_accs += str(sorted_types[i][1][0]) + ";"
			m_cons += str(sorted_types[i][1][1]) + ";"
			m_mults += str(sorted_types[i][1][2]) + ";"
		csvw.writerow([stem, sorted_types[0][0], sorted_types[0][1][0], sorted_types[0][1][1], sorted_types[0][1][2], m_types, m_accs, m_cons, m_mults])

	
