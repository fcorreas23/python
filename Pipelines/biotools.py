#! /usr/bin/env python3

import subprocess as sp
import os



def fileName( file ):
    filename = os.path.basename( file)
    basename = filename.split('.')
    return basename[0]



""" Pre-ensamble """

def runFastqc( fq1, fq2, output ):
    cmd = ['fastqc', '-t', '2', '-o', output, fq1, fq2]
    run = sp.run(cmd)
    if run.returncode == 0:
        return True

def runFastp( fq1, fq2, threads, output ):
    fq1_name = fileName( fq1 )
    fq2_name = fileName( fq2 )
    fq1_out = f'{output}/{fq1_name}_fastp.fq.gz'
    fq2_out = f'{output}/{fq2_name}_fastp.fq.gz'
    cmd = [
        "fastp",
        "detect_adapter_for_pe",
        "--cut_right",
        "--length_required",
        "30",
        "--thread",
        str(threads),
        "--html",
        f'{output}/report.html',
        "--json",
        f'{output}/report.json',
        "--compression",
        "4",
        "-i",
        fq1,
        "-o",
        fq1_out,
        "-I",
        fq2,
        "-O",
        fq2_out
    ]
    run = sp.run(cmd)
    if run.returncode == 0:
        return True

def runBBduk( fq1, fq2, output ):
    fq1_name = fileName(fq1)
    fq2_name = fileName(fq2)
    fq1_out = f'{output}/{fq1_name}_bbduk.fq.gz'
    fq2_out = f'{output}/{fq2_name}_bbduk.fq.gz'
    bbduk = '/opt/biotools/bbmap/bbduk.sh'
    adapters = '/opt/biotools/bbmap/resources/adapters.fa'
    cmd = [
        bbduk,
        f'in1={fq1}',
        f'out1={fq1_out}',
        f'in2={fq2}',
        f'out2={fq2_out}',
        f'ref={adapters}',
        "minavgquality=20",
        "qtrim=rl",
        "minlength=30"
    ]
    run = sp.run(cmd)
    if run.returncode == 0:
        return True

def runKraken2( fq1, fq2, threads, output):
    kraken = '/opt/biotools/kraken2-2.1.2/kraken2'
    database = '/media/labinia/Respaldos/DATABASES/kraken/minikraken2_v2_8GB_201904'
    cmd = [
        kraken,
        "-db",
        database,
        "--threads",
        str(threads),
        "--paired",
        "--output",
        f'{output}/Kraken2_RESULT.txt',
        "--report",
        f'{output}/kraken2_REPORT.txt',
        fq1,
        fq2
    ]
    run = sp.run(cmd)
    if run.returncode == 0:
        return True


""" Post ensample """

def runProkka( args, output ):
    prokka = "/opt/biotools/prokka-1.14.5/bin/prokka"
    cmd = [
        prokka,
        '--outdir',
        output,
        '--prefix',
        args.prefix,
        '--locustag',
        args.prefix,
        '--cpus',
        str(args.threads),
        '--force',
        args.genome
    ]
    run = sp.run(cmd)
    if run.returncode == 0:
        return True
    else:
        return False

def runBakta( args, output ):
    bakta = "/opt/biotools/bakta-1.4.0/bin/bakta"
    database = "/media/labinia/Respaldos/DATABASES/bakta"
    cmd= [
        bakta,
        '--output',
        output,
        '--db',
        database,
        '--prefix',
        args.prefix,
        '--locus-tag',
        args.prefix,
        '--keep-contig-headers',
        '--threads',
        str(args.threads),
        args.genome
    ]
    run = sp.run(cmd)
    if run.returncode == 0:
        return True
    else:
        return False

def runDfast( args, output ):
    dfast = "/opt/biotools/dfast/dfast"
    database = '/media/labinia/Respaldos/DATABASES/dfast'
    cmd = [
        dfast,
        "-g",
        args.genome,
        "-o",
        output,
        '--locus_tag_prefix',
        args.prefix,
        '--step',
        str(args.increment),
        '--cpu',
        str(args.threads),
        '--dbroot',
        database,
        '--force'
    ]
    run = sp.run(cmd)
    if run.returncode == 0:
        return True
    else:
        return False





""" OTRAS """
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


