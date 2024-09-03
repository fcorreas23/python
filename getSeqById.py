#! /usr/bin/env python3

import argparse
from Bio import SeqIO

def getArgs():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('-f', '--fasta', required=True, help='fasta format sequences')
    required.add_argument('-i', '--id', required=True, help='sequence identifier')
    args = parser.parse_args()
    return args

def search( fasta, id ):
    for record in SeqIO.parse( fasta, "fasta" ):
        if record.id == id:
            print(f' RESULT: {id}.fasta')
            SeqIO.write( record, f'{id}.fasta', "fasta")
            return True
    return False

def main():
    args = getArgs()
    found = search( args.fasta, args.id )
    if not found :
        print(f'{args.id} not found')

    

if __name__ == '__main__':
    main()