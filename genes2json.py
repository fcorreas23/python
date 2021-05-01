import os.path, sys, csv, json, argparse
from collections import OrderedDict
from Bio import SeqIO



def getArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', required=True, metavar='<FILE>', help='Input sequence fasta file.')
	parser.add_argument('-u', '--uid', required=True, metavar='uid', help='Mongodb uid assembly')
	args = parser.parse_args()
	return args


def toJson( fastaFile, basename, uid):
	assembly = { "$oid" : uid }
	filename = f'{basename}.json'
	genes = []
	header = ["assembly", "locus", "description", "sequence", "product", "length"]
	for seq_record in SeqIO.parse( fastaFile, 'fasta'):
		locus    = seq_record.id
		description = seq_record.description.split(seq_record.id)
		sequence = str(seq_record.seq)
		product  = "mRNA"
		length   = len(seq_record)
		genes.append(OrderedDict(zip(header, [ uid, locus, description[1], sequence, product, length])))
	
	with open( filename, 'w') as jsonfile:
		json.dump(genes, jsonfile, indent=2)

	return filename
			
	

def main():
	args = getArgs()
	filename = os.path.basename( args.input )
	basename = filename.split('.')
	jsonFile = toJson( args.input, basename[0], args.uid)

	print(f'{jsonFile} ha sido generado')
	

if __name__ == '__main__':
	main()