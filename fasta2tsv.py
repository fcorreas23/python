#! /usr/bin/env python3

import os.path, sys, csv, argparse
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', required=True, metavar='<FILE>', help='Input sequence fasta file.')
	args = parser.parse_args()
	return args


def fasta2tsv( fastaFile, basename ):
	filename = f'{basename}.tsv'
	data = []
	header   = ["locus", "description", "sequence", "length"]
	data.append( header)
	for seq_record in SeqIO.parse( fastaFile, 'fasta'):
		locus    = seq_record.id
		desc     = seq_record.description.split(seq_record.id)
		sequence = str(seq_record.seq)
		length   = len(seq_record)

		data.append([locus, desc[1], sequence, length])

	with open( filename, mode='w') as file:
		writer = csv.writer(file, delimiter='\t')
		writer.writerows(data)

	return filename


def main():

	args = getArgs()
	filename = os.path.basename( args.input )
	basename = filename.split('.')
	tsvFile  = fasta2tsv( args.input, basename[0])

	print(f'{tsvFile} ha sido generado')	


if __name__ == '__main__':
	main()