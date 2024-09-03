#! /usr/bin/env python3
import os
import pandas as pd
import seaborn as sns
import subprocess as sp
import argparse
import re



def getArgs():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('--primers', required=True, metavar='<FILE>', help='Lista de primers formato IPCRESS')
    required.add_argument('--fasta', required=True, metavar='<FILE>', help='Secuencias formato fasta')
    optional = parser.add_argument_group('Optional arguments')
    #optional.add_argument('-o', '--output', default= 'MLOCI')
    optional.add_argument('--min', type=int, metavar='int', default= 3, help='minimo de amplicones')
    optional.add_argument('--max', type=int, metavar='int', default= 10, help='maximo de amplicones')
    args = parser.parse_args()
    return args

def runIPCRESS( primers, fasta):
    file_output = './IPCRESS/IPCRESS_RESULT.txt'
    
    if os.path.exists(file_output): #Si ya existe la PCR
        print(f'IPCRESS: EL ARCHIVO YA EXISTE')
        return file_output
    cmd = ["ipcress", str(primers), str(fasta)]

    with open(file_output, 'w') as f:
        run = sp.run(cmd, stdout=f)      
    if run.returncode == 0:
        return file_output
    else:
        return False

def parseIPCRESS( file ):
    ipcress_header=['sequence_id', 'primer_id','product_length','primer_5','pos_5', 'mismatch_5', 'primer_3', 'pos_3', 'mismatch_3', 'description']
    result = []
    test = [line for line in open(file) if re.match(r'^ipcress:',line)]
    aux = [x.split() for x in test]
    for item in aux:
        result.append([item[1].split(":")[0], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10]])
    
    ePCR_hits=pd.DataFrame( result, columns=ipcress_header)
    ePCR = ePCR_hits.drop(ePCR_hits[(ePCR_hits['description'] == 'single_A') |(ePCR_hits['description'] == 'single_B')].index)
    ePCR.to_csv('IPCRESS/IPCRESS_RESULT_RESUMEN.tsv', sep="\t", index=False)
    #countPrimers = dict(ePCR['primer_id'].value_counts())
    return ePCR

def filterByNumAmpli( dfPCR, min, max ):
    primers = dict(dfPCR['primer_id'].value_counts())




    return True

def main():
    args = getArgs()
    df_primers = pd.read_csv(args.primers, delimiter="\t")
    print(f"Numero de partidores: {len(df_primers)}")
    
    try:
        ipcress_result = runIPCRESS(  args.primers, args.fasta)
    except TypeError:
        print("An exception occurred") 

    dfPCR= parseIPCRESS( ipcress_result)
    #filterByNumAmpli(dfPCR, args.min, args.max)





if __name__ == '__main__':
    main()