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
		sys.argv[3]
	except Exception as e:
		print("ERROR: Faltan Parametros")
		sys.exit(0)

	res = []
	assembly = sys.argv[3]
	basename = os.path.basename(sys.argv[1]).split('.')
	proteinas = fasta2list( sys.argv[1] )
	anotaciones = emmaperResult( sys.argv[2] )


	print(f'Numero de proteinas: {len(proteinas)}')
	print(f'Numero de proteinas anotadas: {len(anotaciones)}')
	for proteina in proteinas:
		#res = protein2json(proteina, anotaciones, assembly)
		res.append( protein2json(proteina, anotaciones, assembly) )

	with open(f'{basename[0]}.json', 'w') as jsonfile:
		json.dump(res, jsonfile, indent=4)

	print(f'{basename[0]}.json ha sido generado')	

def protein2json(seqid, anotaciones, assembly):
	data = []
	for anotacion in anotaciones:
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


def emmaperResult( eggnog ):
	data = []
	with open( eggnog ) as tsvfile:
		rows = csv.reader(tsvfile, delimiter='\t')
		for row in rows:
			if row[0].strip()[0] == '#':
				continue
			data.append(row)
			#if row[0] == seqid:
	
	return data			


def fasta2list( fastaFile ):
	data = []
	for seq_record in SeqIO.parse( fastaFile, 'fasta'):
		locus    = seq_record.id
		desc     = seq_record.description.split(seq_record.id)
		sequence = str(seq_record.seq)
		length   = len(seq_record)

		data.append([locus, desc[1], sequence, length])

	return data








if __name__ == '__main__':
	main()
