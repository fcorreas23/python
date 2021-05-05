#! /usr/bin/env python3

import os, argparse, subprocess, logging
from pathlib import Path
from Bio import SeqIO

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--blast', required=True, help='Program blast')
    parser.add_argument('-q', '--query', required=True, metavar='<FILE>',  help='Input file name')
    parser.add_argument('-db', '--database', required=True, metavar='PATH', help='BLAST database name')
    parser.add_argument('-e', '--evalue', metavar='E-value', default=1e-20, help='Expectation value (E) threshold for saving hits')
    parser.add_argument('-max_target_seqs', '--mts', metavar='Integer, >=1', default=1, help='Maximum number of aligned sequences to keep')
    parser.add_argument('-t', '--threads', default=8, help='Number of threads (CPUs) to use in the BLAST search')
    args = parser.parse_args()
    return args



def blast( input ):

    filename = os.path.basename( input.query )
    dbname = os.path.basename( input.database )
    basename = filename.split('.')
    output = f'{basename[0]}_vs_{dbname}.tsv'

    blast_cmd = f"{input.blast} -db {input.database} -query {input.query} -evalue {input.evalue} " \
        f"-max_target_seqs {input.mts} -num_threads {input.threads} " \
        "-outfmt '6 qseqid sseqid stitle pident length mismatch gapopen qstart qend sstart send evalue bitscore' " \
        f"-out {output}"
    p = subprocess.Popen(blast_cmd, shell=True)
    logging.info(f"Running {input.blast} on {filename}")
    logging.info(f"cmd: {blast_cmd}")
    p.wait()

    return output

def check_fasta( fastaFile ):
    data = []
    for seq_record in SeqIO.parse( fastaFile, 'fasta'):
        data.append(seq_record.id)
    return data

def filter_blast( outBlastFile ):
    with open(str(outBlastFile), 'r') as f:
        blastn_file = f.readlines()

    logging.info(f"Se blastearon {len(blastn_file)} secuencias")


def main():
    args = getArgs()
    filename = os.path.basename( args.query )
    
    logging.basicConfig(
        format='%(asctime)-15s %(message)-8s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    
    sequences = check_fasta( args.query )
    
    logging.info(f'Numero de secuencias a blastear: { len(sequences) }')   
    
    
    
    blast_result = blast( args )
    filter_blast( blast_result )
    

if __name__ == '__main__':
    main()