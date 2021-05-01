#! /usr/bin/env python3

import os.path, sys, csv, json, argparse
from collections import OrderedDict
from Bio import SeqIO

def getArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', required=True, metavar='<FILE>', help='Input sequence fasta file.')
	parser.add_argument('-e', '--emmaper', required=True, metavar='<FILE>', help='Input protein emmaper file.')
	parser.add_argument('-u', '--uid', required=True, metavar='uid', help='Mongodb uid assemblt')
	args = parser.parse_args()
	return args


def fasta2list( fastaFile ):
	data = []
	for seq_record in SeqIO.parse( fastaFile, 'fasta'):
		locus    = seq_record.id
		desc     = seq_record.description.split(seq_record.id)
		sequence = str(seq_record.seq)
		length   = len(seq_record)

		data.append([locus, desc[1], sequence, length])

	return data

def emmaperResult( emmaper ):
	data = []
	with open( emmaper ) as tsvfile:
		rows = csv.reader(tsvfile, delimiter='\t')
		for row in rows:
			if row[0].strip()[0] == '#':
				continue
			data.append(row)
	return data

def protein2json(seqid, annotations, assembly):
	data = []
	for anotacion in annotations:
		if anotacion[0] == seqid[0]:
			return dict(
					assembly = { "$oid" : assembly },
					locus = seqid[0], 
					description = anotacion[21], 
					sequence = seqid[2], 
					length = seqid[3], 
					alias = anotacion[5], 
					gene_ontology = anotacion[6],
					enzyme_code = anotacion[7],
					kegg_ko = anotacion[8],
					kegg_pathway = anotacion[9],
					kegg_module = anotacion[10],
					cog_funcional = anotacion[20]
			)
			
	return dict(
			assembly = { "$oid" : assembly },
			locus = seqid[0], 
			description = seqid[1],
			sequence = seqid[2],
			length = seqid[3],
			alias = '',
			gene_ontology = '',
			enzyme_code = '',
			kegg_ko = '',
			kegg_pathway = '',
			kegg_module = '',
			cog_funcional = ''
	)

def main():

	args = getArgs()
	res = []
	filename = os.path.basename( args.input )
	basename = filename.split('.')
	proteins = fasta2list( args.input )
	annotations = emmaperResult( args.emmaper)
	
	print(f'Numero de proteinas: {len(proteins)}')
	print(f'Numero de proteinas anotadas: {len(annotations)}')
	print('Generando json.......')

	for protein in proteins:
		res.append( protein2json(protein, annotations, args.uid) )

	with open(f'{basename[0]}.json', 'w') as jsonfile:
		json.dump(res, jsonfile, indent=4)

	print(f'{basename[0]}.json ha sido generado')	


if __name__ == '__main__':
	main()
