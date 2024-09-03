#!/usr/bin/env python
import os
import argparse
import time
from utils import isFastq, makeOutputDir
from biotools import runFastqc, runFastp, runBBduk, runKraken2


def getArgs():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('-f', '--forward', required=True, metavar='<FILE>', help='Input sequence fastq file.')
    required.add_argument('-r', '--reverse', required=True, metavar='<FILE>', help='Input sequence fastq file.')
    optional = parser.add_argument_group('Optional arguments')
    optional.add_argument('-t', '--threads', type=int, metavar='int', default= 2, help='number of parallel CPU workers to use for multithreads  [2]')
    optional.add_argument('-o', '--output', default= 'RESULT_PRE', help='Dirname output')
    args = parser.parse_args()

    return args

def main():
    args = getArgs()
    path = os.getcwd()
    forward = args.forward
    reverse = args.reverse
    threads = args.threads

    result = os.path.join( path, args.output )
    
    if isFastq( forward ) and isFastq( reverse ):
        #RUN fastqc
        output1 = makeOutputDir( result, 'fastqc')
        print('RUN FASTQC')
        if runFastqc( forward, reverse, output1 ):
            print(f'Fastqc finished: {output1}')
        
        #RUN fastp
        time.sleep(3)
        output2 = makeOutputDir( result, 'fastp')
        print('RUN FASTP')
        if runFastp( forward, reverse, threads, output2):
            print(f'Fastp finished: {output2}')
        
        #RUN Kraken2
        time.sleep(3)
        output3 = makeOutputDir( result, 'kraken2')
        print('RUN KRAKEN2')
        if runKraken2( forward, reverse, threads, output3):
            print(f'Kraken2 finished: {output3}')      

    else:
        print("FASTQ INVALIDOS")


if __name__ == '__main__':
    main()
