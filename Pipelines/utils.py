 #!/usr/bin/env python
 
import os

def isFastq( file ):
    ext = ['.fq', '.fastq', '.fq.gz', '.fastq.gz']
    return file.endswith( tuple(ext) )

def isFasta( file ):
    ext = ['.fa', 'fna','.fasta', '.fa.gz', '.fasta.gz']
    return file.endswith( tuple(ext) )

def fileName( file ):
    filename = os.path.basename( file )
    basename = filename.split('.')
    return basename[0]

def makeOutputDir( path, dirname ):
    outputdir = os.path.join( path, dirname)
    if not os.path.exists( outputdir ):
        os.makedirs( outputdir )
    return outputdir
