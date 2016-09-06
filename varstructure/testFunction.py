# -*- coding: utf-8 -*-
from string import whitespace
from argparse import ArgumentParser
from string import whitespace
import logging
import os
import string
import sys
import vcf
#Bioservices Library
from bioservices import UniProt
from bioservices import PDB
#BioPython Library
from Bio.PDB import *
#added to work with sequence
from Bio import SeqIO
from Bio.Seq import Seq
#added for data structures
from collections import defaultdict
from collections import OrderedDict
import itertools
import pandas as pd

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--vcf", type=str, dest="vcf", help="Input variant file (vcf)", required=True)
    parser.add_argument("--log", type=str, help="Logs progress in specified file, defaults to stdout.")
    parser.add_argument("-v", "--verbosity", action="count", default=0)

    args = parser.parse_args()


    if args.verbosity >= 2:
        print "{} to the power {} equals {}".format(args.v, args.o, answer)
    elif args.verbosity >= 1:
        print "{}^{} == {}".format(args.x, args.y, answer)

    return args

def get_hmm():
    """Get a thought."""
    return 'hmmm...'

def hmm():
    """Contemplation..."""
    print get_hmm()

def main():
    """ Main function."""
    args = parse_args()
    if args.log:
        logfile = args.log
        logging.basicConfig(filename=logfile, level=logging.DEBUG, \
            filemode='w', format='%(asctime)s %(message)s', \
            datefmt='%Y-%m-%d %H:%M:%S')
    else:
        logfile = sys.stdout


    vcf_row = {}

    #Interface to the UniProt service
    u = UniProt(verbose=False)

    vcf_reader = vcf.Reader(open(args.vcf, 'r'))
    #df= pd.DataFrame()
    columns = ['Uniprot_ID','PDB_ID']
    df = pd.DataFrame()
    #creating a util function to store mapping of Uniprot and PDB_ID
    for record in vcf_reader:
        print record
        # VEP fields
        current_swissport = ''
        if "CSQ" in record.INFO:
            csq = record.INFO['CSQ']
            # BELOW: THERE ARE A COUPLE OF OPTIONS TO PROCEED
            # For going through annotations for all transcript
            for current_csq_element in csq:
                current_csq = current_csq_element.split('|')
                current_swissport = current_csq[27]

                mapping_Dictionary={}
                # to get PDB ID given uniport id
                if current_swissport != "":
                    mapping_Dictionary= u.mapping("ID", "PDB_ID", current_swissport)
                    print mapping_Dictionary.values()

                if bool(mapping_Dictionary) == True:
                    new_record = pd.DataFrame(mapping_Dictionary.items(),mapping_Dictionary.values())
                    df = pd.concat([df,new_record])
                    #df = df.set_value(, )
                    print df

                #parser = PDBParser()
                #structure = parser.get_structure('PHA-L', '1FAT.pdb')

                #parser = MMCIFParser()
                #structure = parser.get_structure('PHA-L', '1FAT.cif')
                #mmcif_dict = MMCIF2Dict('1FAT.cif')

                #resolution = structure.header['resolution']
                #keywords = structure.header['keywords']



    logging.info('Start.')
    logging.info('Command line: {}'.format(' '.join(sys.argv)))

    # logging.info()

if __name__ == '__main__':
    main()
