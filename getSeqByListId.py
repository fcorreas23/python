#! /usr/bin/env python

import argparse
from Bio import SeqIO


def getArgs():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('-f','--fasta', required=True, help='secuencias formato fasta')
    required.add_argument('-i','--list', required=True,  help='Lista de primers id forward reverse')
    optional = parser.add_argument_group('Optional arguments')
    optional.add_argument('-o', '--output', default= 'RESULT_PTRA', help='Dirname output')
    args = parser.parse_args()
    return args

def listid( ids ):
    lines = []
    with open( ids, "r") as file:
        for line in file:
            lines.append(line.strip())
    return lines

def getGenes( fasta, listids ):
    sequences = []
    for gen in listids:
        for seq_record in SeqIO.parse( fasta, "fasta"):
            if gen == seq_record.id:
                sequences.append(seq_record)

    SeqIO.write( sequences, 'Genes.fasta', "fasta")
def main():
    args = getArgs()
    getGenes( args.fasta, listid(args.list))

if __name__ == '__main__':
    main()