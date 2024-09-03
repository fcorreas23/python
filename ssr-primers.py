#! /usr/bin/env python3
import os
import pandas as pd
import subprocess as sp
import seaborn as sns
import argparse

SSRMMD = '/opt/biotools/SSRMMD-master/SSRMMD.pl'
PRIMER3 = '/opt/biotools/SSRMMD-master/connectorToPrimer3/connectorToPrimer3.pl'
THREADS = 6


def getArgs():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('--fasta', required=True, metavar='<FILE>', help='Secuencias formato fasta')
    optional = parser.add_argument_group('Optional arguments')
    optional.add_argument('--mo', type=str, default= '2=7,3=4,4=4,5=4,6=4', help='motif=num de repiticiones')
    optional.add_argument('--as', type=str, default= '100-300', help='Rango del amplicon')
    optional.add_argument('--gc', type=str, default= '45,60', help='GC primers')
    optional.add_argument('--tm', type=str, default= '57,60,63', help='TM primers')




    args = parser.parse_args()
    return args

def makeOutDir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def runSSRMMD( fasta, outdir, mo ):
    cmd = ['perl', SSRMMD, '-f1', fasta, '-p', '0', '-o', outdir, '-t', str(THREADS), '-mo', mo, '-ss', '1']
    print(cmd)
    run = sp.run(cmd)
    if run.returncode == 0:
        return True
    else:
        return False


def main():
    args = getArgs()
    outdir = os.path.join(os.getcwd(), 'SSR-PRIMERS')
    makeOutDir(outdir)

    runSSRMMD(args.fasta, outdir, args.mo)





if __name__ == '__main__':
    main()
