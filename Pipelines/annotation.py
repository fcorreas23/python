#! /usr/bin/env python3
import os
import argparse
from utils import isFastq, makeOutputDir
from biotools import runProkka, runBakta, runDfast

def getArgs():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('-g', '--genome', required=True, metavar='<FILE>', help='Input sequence fastq file.')
    required.add_argument('-p', '--prefix', required=True, help='Filename and locus tag tag prefix')

    optional = parser.add_argument_group('Optional arguments')
    optional.add_argument('--genus', default= "Genus", help="Genus name (default 'Genus')")
    optional.add_argument('--species', default= "species", help="Species name (default 'species')")
    optional.add_argument('--strain', default= "strain", help="Strain name (default 'strain')")
    optional.add_argument('-t', '--threads', type=int, metavar='int', default= 2, help='Number of CPUs to use [0=all] (default: 2)')
    optional.add_argument('-o', '--output', default= 'RESULT_ANNOT', help='Output folder (default RESULT_ANNOT )')
    optional.add_argument('--increment', default=5, type=int, metavar='int', help='Locus tag counter increment (default: 5)')
    args = parser.parse_args()

    return args

def main():
    args = getArgs()
    path = os.getcwd()

    result = os.path.join( path, args.output )
    out_prokka = makeOutputDir( result, 'prokka')
    out_bakta = makeOutputDir( result, 'bakta')
    out_dfast = makeOutputDir( result, 'dfast')

    """ if runProkka( args, out_prokka):
        print(f'Prokka finished: {out_prokka}') """
    
    """ if runBakta( args, out_bakta):
        print(f'Prokka finished: {out_bakta}') """

    if runDfast( args, out_dfast):
        print(f'Dfast finished: {out_dfast}')
        
if __name__ == '__main__':
    main()