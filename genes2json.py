import sys
import csv
import os.path
import json
from collections import OrderedDict
from Bio import SeqIO


def main():
	try:
		sys.argv[1]
		sys.argv[2]
	except Exception as e:
		print("ERROR: Faltal Parametros")
		sys.exit(0)

	header   = ["locus", "assembly", "sequence", "desc", "product", "length"]
	basename = os.path.basename(sys.argv[1]).split('.')

	genes = fasta2list(sys.argv[1])

	jsonFile = fasta2json( genes, basename, sys.argv[2])
	
	print(f'{jsonFile} ha sido generado')
	

def fasta2list( fastaFile ):
	data = []
	for seq_record in SeqIO.parse( fastaFile, 'fasta'):
		locus    = seq_record.id
		desc     = seq_record.description.split(seq_record.id)
		sequence = str(seq_record.seq)
		product  = "mRNA"
		length   = len(seq_record)

		data.append([locus, desc[1], sequence, product, length])

	return data


def fasta2json( genes, basename, uid):

	assembly = { "$oid" : uid }
	filename = f'{basename[0]}.json'
	data = []
	for gen in genes:
		fastaDic = dict(assembly=assembly, locus=gen[0], description=gen[1] , sequence=gen[2], product=gen[3], lenght=gen[4])
		data.append(fastaDic)

	with open( filename, 'w') as jsonfile:
		json.dump(data, jsonfile, indent=2)

	return filename





if __name__ == '__main__':
	main()