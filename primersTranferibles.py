#! /usr/bin/env python3
import os
import re
import argparse
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
from utils import isFasta, fileName, makeOutputDir




def getArgs():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    required.add_argument('--primers', required=True, metavar='<FILE>', help='Lista de primers id forward reverse')
    required.add_argument('--fasta', required=True, metavar='<FILE>', nargs='*', help='secuencias formato fasta')
    optional = parser.add_argument_group('Optional arguments')
    optional.add_argument('-o', '--output', default= 'RESULT_PTRA', help='Dirname output')
    optional.add_argument('--min', type=int, metavar='int', default= 3, help='minimo de amplicones')
    optional.add_argument('--max', type=int, metavar='int', default= 100, help='maximo de amplicones')
    args = parser.parse_args()
    return args
    
def runIPCRESS( primers, fasta, output ):
    name = fileName( fasta )
    file_output = f'{output}/{name}_PCR_IPCRESS_RESULT.txt'
    
    if os.path.exists(file_output): #Si ya existe la PCR
        return file_output
    cmd = ["ipcress", str(primers), str(fasta)]

    with open(file_output, 'w') as f:
        run = sp.run(cmd, stdout=f)      
    if run.returncode == 0:
        return file_output
    else:
        return False

def parseIPCRESS( file, output ):
    ipcress_header=['sequence_id', 'primer_id','product_length','primer_5','pos_5', 'mismatch_5', 'primer_3', 'pos_3', 'mismatch_3', 'description']
    result = []
    outfile = f'{output}/PCR_IPCRESS_RESULT_TABLE.tsv'
    test = [line for line in open(file) if re.match(r'^ipcress:',line)]
    aux = [x.split() for x in test]
    for item in aux:
        result.append([item[1].split(":")[0], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10]])
    
    ePCR_hits=pd.DataFrame(result, columns=ipcress_header)
    ePCR = ePCR_hits.drop(ePCR_hits[(ePCR_hits['description'] == 'single_A') |(ePCR_hits['description'] == 'single_B')].index)
    ePCR.to_csv(outfile, sep="\t", index=False)

    primers = dict(ePCR_hits['primer_id'].value_counts())

    with open(f'{output}/PRIMERS_NUM-AMPLICONES.tsv', 'w') as f: 
        f.write('PRIMERS_ID\tN°AMPLICONES\n')
        for key, value in primers.items(): 
            f.write('%s\t%s\n' % (key, value))
    
    return ePCR, primers

def dfPrimers( primers ):
    header = ['PRIMER_ID', 'FORWARD', 'REVERSE', 'MIN', 'MAX']
    df_primers = pd.read_csv(primers, sep=" ", names=header)
    df_primers['PRIMER_ID']=df_primers['PRIMER_ID'].values.astype(str)
    return df_primers

def plotAmplificaciones ( primers, output ):
    plot_name = f'{output}/pcr_insilico_plot.png'
    one = { key:value for (key, value) in primers.items() if value == 1 }
    two = { key:value for (key, value) in primers.items() if value == 2 }
    range1 = { key:value for (key, value) in primers.items()  if value >= 3 and value <= 9 }
    range2 = { key:value for (key, value) in primers.items()  if value >= 10 and value <= 30 }
    range3 = { key:value for (key, value) in primers.items()  if value > 30 and value <= 50 }
    range4 = { key:value for (key, value) in primers.items()  if value > 50 }

    plot = {'1': len(one), '2': len(two), '3-9': len(range1), '10-30': len(range2), '31-50': len(range3), '> 50': len(range4) }

    plot_x = list( plot.keys() )
    plot_y = list( plot.values() )
    plt.title('PCR in-silico')
    plt.xlabel('Cantidad de amplicones')
    plt.ylabel('Numero de Primers')
    plt.bar( range( len(plot) ), plot_y, tick_label=plot_x)
    plt.savefig(plot_name)
    plt.close()
    return plot_name

def filterByAmplicon( primers, min, max ):
    filtro_amplificacion = { key:value for (key, value) in primers.items()  if value >= min and value <= max }
    primers_selecionados = list( set(filtro_amplificacion.keys()) )
    return primers_selecionados

def filterDataFrames( dataframe, primers ):
    strains = []
    sizes = []
    num_amplicones = []
    for primer in primers:
        strains.append(unique(list( dataframe['sequence_id'].loc[ dataframe['primer_id'] == primer ] )))
        sizes.append(unique(list(dataframe['product_length'].loc[dataframe['primer_id'] == primer])))
        num_amplicones.append(len(list( dataframe['sequence_id'].loc[ dataframe['primer_id'] == primer ] )))    
    data_frame = pd.DataFrame({'PRIMER_ID': primers,
                            'NUM_AMP_': num_amplicones,
                            'STRAIN': strains,
                            'SIZE_AMPL': sizes})
    return data_frame

def unique(lista):
    unique_list = ( list( set(lista)))
    #unique_list.sort()
    return unique_list

def main():
    args = getArgs()
    lista_primers = args.primers
    secuencias_fasta = args.fasta
    min_amp = args.min
    max_amp = args.max
    resultados = os.path.join(os.getcwd(), args.output )    
    df_primers = dfPrimers( lista_primers )
    primers_selected = []
    nombre_fastas = []
    df_InSilicoPCRs =[]

    print(f'\nN° DE PRIMERS: {len( df_primers )}')
    print(f'GENOMA MODELO: {os.path.basename(secuencias_fasta[-1])}')

    for fasta in secuencias_fasta:
        if isFasta( fasta ):
            print(f'\nCorriendo PCR in-Silico en {os.path.basename(fasta)}')
            nombre = fileName( fasta )
            nombre_fastas.append( nombre )
            output = makeOutputDir( resultados, nombre)
            pcr_insilico = runIPCRESS( lista_primers, fasta, output )
            df_ePCR, primers = parseIPCRESS( pcr_insilico, output )
            primers_selected.append(set(primers.keys()))
            df_InSilicoPCRs.append(df_ePCR)
            plot_out = plotAmplificaciones( primers, output )
            print(f'De { len( df_primers ) } primers testeados, amplificaron { len(primers)} ')
            print(f'Resultado PCR inslico: { pcr_insilico }')
            print(f'Plot: { plot_out }')
            
        else:
            print(f'El archivo {fasta} no es valido')
    
    print("\n-----PRIMERS TRANSFERIBLES------")
    sleep(3)
    primers_transferibles = list(set.intersection( *primers_selected )) #Intersección de la lista de primers que amplifican
    print(f'Numero de primers transferibles: {len(primers_transferibles)}')
    df_primers_transferibles = df_primers[df_primers['PRIMER_ID'].isin(primers_transferibles)]
    df_primers_transferibles[['PRIMER_ID', 'FORWARD', 'REVERSE']].to_csv(f'{resultados}/PRIMERS_TRANSFERIBLES.tsv', sep="\t", index=False)
    print(f'Primes transferibles: {resultados}/PRIMERS_TRANSFERIBLES.tsv')
    #Obtener diccionario de primers transferibles
    amplicones_primers_transferibles = dict( (key, primers[key]) for key in primers_transferibles)
    #Graficar la distribucion de n° de amplicones usando la referencia asignada
    print(f'Distribucion n° amplicones: {plotAmplificaciones( amplicones_primers_transferibles, resultados )}')
    #Obtener el compartimiento de los primers filtrado por numero de amplicones
    fastaName_dfPCR = dict( zip(nombre_fastas, df_InSilicoPCRs))
    filter_by_amplicon = filterByAmplicon(amplicones_primers_transferibles, min_amp, max_amp)
    
    for (key, value ) in fastaName_dfPCR.items():
        print(f'Buscando en: {key}')
        sheet = filterDataFrames( value, filter_by_amplicon)
        sheet.to_csv(f'{resultados}/{key}_{min_amp}-{max_amp}.tsv', index=False, sep="\t")
    
    #sheet = []
    """ x=1
    for s in sheet:
        with pd.ExcelWriter(f'{resultados}/filename.xlsx') as writer:
            s.to_excel(writer, sheet_name=f'Fruits_{x}', index=False)
        x = x+1 """  

if __name__ == '__main__':
    main()
