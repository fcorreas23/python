import sys
import csv
import os.path
import json
from collections import OrderedDict
from Bio import SeqIO


def main():
	try:
		sys.argv[1]
	except Exception as e:
		print("ERROR: Faltal Parametros")
		sys.exit(0)

	header   = ["locus", "sequence", "description", "length"]
	basename = os.path.basename(sys.argv[1]).split('.')
	jsonFile = fastaTojson( sys.argv[1], basename, header)

	print(f'{jsonFile} ha sido generado')
	

def fastaTojson( fastaFile, basename, header):
	
	filename = f'{basename[0]}.json'
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


if __name__ == '__main__':
	main()