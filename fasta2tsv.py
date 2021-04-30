import sys
import csv
import os.path
from Bio import SeqIO


def main():
	try:
		sys.argv[1]
	except Exception as e:
		print("ERROR: Faltal Parametros")
		sys.exit(0)

	header   = ["locus", "description", "sequence", "length"]
	basename = os.path.basename(sys.argv[1]).split('.')

	genes = fasta2list(sys.argv[1])

	tsvFile  = fasta2tsv( genes, basename, header)
	
 

	print(f'{tsvFile} ha sido generado')	

def fasta2list( fastaFile ):
	data = []
	for seq_record in SeqIO.parse( fastaFile, 'fasta'):
		locus    = seq_record.id
		desc     = seq_record.description.split(seq_record.id)
		sequence = str(seq_record.seq)
		length   = len(seq_record)

		data.append([locus, desc[1], sequence, length])

	return data


def fasta2tsv( genes, basename, header):

	filename = f'{basename[0]}.tsv'
	genes.insert(0, header)

	with open( filename, mode='w') as file:
		writer = csv.writer(file, delimiter='\t')
		writer.writerows(genes)

	return filename





if __name__ == '__main__':
	main()