#! /usr/bin/python

import sys
import os
import argparse
from Bio import SeqIO

'''
cut_gbk.py

by Isabel

Extract a segment from a GenBank file using coordinates or locus_tags.
'''
	

def coo_by_loc_tag(gbk, loc_tag):
	#find the coordinates of the gene with a given locus_tag
	for contig in gbk.keys():
		for feature in gbk[contig].features:
			if feature.type=="gene" and feature.qualifiers["locus_tag"][0]==loc_tag:
				return [int(feature.location.start), int(feature.location.end),contig]


def main(argv):

	
	parser=argparse.ArgumentParser(description="by Isabel\n\nExtract a segment from a GenBank file using coordinates or locus_tags.", formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-i', '--inputfile', required=True, help="a GenBank file")
	parser.add_argument('-s','--start', required=True, help="start coordinate or locus_tag")
	parser.add_argument('-e','--end', required=True, help="end coordinate or locus_tag")
	parser.add_argument('-c','--contig', required=False, help="identifier of contig to be cut (needed when coordinates are given and there is more than one GenBank record in the input file)")
	
	args=parser.parse_args()
	
	#input file
	gbk_in=SeqIO.to_dict(SeqIO.parse(args.inputfile,"genbank"))
	
	#output file
	gbk_out=open(args.inputfile.replace(".gbk","")+"_cut.gbk","w")
	
	#find cut coordinates when locus_tags are given
	if "_" in args.start and "_" in args.end:
		coo_start=coo_by_loc_tag(gbk_in, args.start)
		coo_end=coo_by_loc_tag(gbk_in, args.end)
		
		coo_start_pos=coo_start[0]
		coo_end_pos=coo_end[1]
		
		#test if start and end locus_tags are on the same contig
		if coo_start[2]!=coo_end[2]:
			sys.exit("Error: Start and end locus_tags are not on the same GenBank record.")
		else:
			contig=coo_start[2]
	
	#store given coordinates
	elif args.start.isdigit() and args.end.isdigit():
		coo_start_pos=args.start
		coo_end_pos=args.end
		
		if len(gbk_in.keys())>1 and args.contig==None:
			sys.exit("Error: Contig identifier needed.\nUse the '-c' parameter to state the identifier of the GenBank record to be cut.")
		elif len(gbk_in.keys())==1:
			contig=gbk_in.keys()[0]
	
	#error	
	else:
		sys.exit("Error: Start and end are neither valid integers nor valid locus_tags.")
	
	
	print("\nCutting contig "+contig+" from "+str(coo_start_pos)+" to "+str(coo_end_pos)+"\n")
	
	gbk_out.write(gbk_in[contig][coo_start_pos:coo_end_pos].format("genbank"))
	gbk_out.close()

if __name__ == "__main__":
   main(sys.argv)
