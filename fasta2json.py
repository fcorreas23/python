#! /usr/bin/env python3

import os.path, sys, json, argparse
from collections import OrderedDict
from Bio import SeqIO

def getArgs(): 
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', required=True, metavar='<FILE>', help='Input sequence fasta file.')
	args = parser.parse_args()
	return args

def fastaTojson( fastaFile, basename):
    	
	filename = f'{basename}.json'
	header   = ["locus", "sequence", "description", "length"]
	data = []
	
	for seq_record in SeqIO.parse(fastaFile, 'fasta'):
		locus = seq_record.id
		sequence = str(seq_record.seq)
		desc = seq_record.description.split(seq_record.id)
		length = len(seq_record)
		data.append(OrderedDict(zip(header, [locus, sequence, desc[1], length])))
	
	with open( filename, 'w') as jsonfile:
		json.dump(data, jsonfile, indent=2)

	return filename

def main():
	args = getArgs()

	filename = os.path.basename( args.input)
	basename = filename.split('.')
	jsonFile = fastaTojson( args.input, basename[0])

	print(f'{jsonFile} ha sido generado')
	




if __name__ == '__main__':
	main()