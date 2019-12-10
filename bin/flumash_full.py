import sys
import csv
import re
import argparse
import subprocess as sp
import multiprocessing as mp

#Argument Parser
parser = argparse.ArgumentParser(description="Use mash to determine influenza subtype")
parser.add_argument("-i", "--containment", type=float, help="Minimum containment to report (Default = 0.95)", default=0.95)
parser.add_argument("-m", "--multiplicity", type=int, help="Minimum median multiplicity (coverage depth) to report (Default = 10)", default=10)
parser.add_argument("-p", "--threads", help="Maximum number of processors to use (Default = 1)", type = int, default=1)
parser.add_argument("--HA_sketch", help="Path to custom hemagglutinin sketch")
parser.add_argument("--NA_sketch", help="Path to custom neuraminidase sketch")
parser.add_argument("Fastqs", help="Input fastq files to process", nargs='+')
args = parser.parse_args()

#Identify reads that should be paired and create input read list

inlist = []
prefs = []
infiles=sorted(args.Fastqs)

while infiles:
	s1=infiles.pop(0)
	s2=None
	mtch=re.search(r'_S[0-9][0-9]*_L001_R1_001.f["ast"]*q', s1)
	if mtch:
		s2=s1.replace("_R1_", "_R2_")
		pref=re.split(r'_S[0-9][0-9]*_L001_R1_001.f["ast"]*q', s1)[0]
	else:
		mtch=re.search(r'_1.f["ast"]*q', s1)
		if mtch:
			s2=s1.replace("_1.f", "_2.f")
			pref=re.split(r'_1.f["ast"]*q',s1)[0]
		else:
			pref=i.split(".")[0]
	if infiles and s2 == infiles[0]:
		inlist.append([s1, infiles.pop(0)])
	else:
		inlist.append([s1])
	pref=pref.split("/")[-1]
	prefs.append(pref)

if len(prefs) != len(inlist):
	sys.exit("Something went wrong when parsing input files")

#Determining the number of jobs and threads per job
ncpus = min(args.threads, mp.cpu_count()) 
totjobs = len(inlist) #The total number of input sequences, which is also the total number of jobs to run



#Call mash
for i in range(0, len(prefs)):
	prefix=prefs[i]
	outf_H = prefix + "_mash_HA.tsv"
	outf_N = prefix + "_mash_NA.tsv"
	errf_H = prefix + "_mash_HA.err"
	errf_N = prefix + "_mash_NA.err"

	if len(inlist[i]) in [1,2]:
		H_cmd = ["mash", "screen",  "-i", str(args.containment), "-p", str(ncpus), args.HA_sketch] + inlist[i]
		sp.call(H_cmd, stdout=open(outf_H, 'w'), stderr=open(errf_H,'w'))
		N_cmd = ["mash", "screen",  "-i", str(args.containment), "-p", str(ncpus), args.NA_sketch] + inlist[i]
		sp.call(N_cmd, stdout=open(outf_N, 'w'), stderr=open(errf_N, 'w'))
	else:
		sys.exit("Something wrong with inlist length")
