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
from bioservices import *
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

from Bio import SwissProt

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--vcf", type=str, dest="vcf", help="Input variant file (vcf)", required=True)
    parser.add_argument("--output", type=str, dest="out", help="Output file (tabular)", required=True)
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

    outputfile = open(args.out, "w")
    # Output header
    outputfile.write("chr\tpos\tid\tref\talt\tgene\tfeature\tfeature_type\tconsequence\tswissprotid\tuniprotid\tpdbid\tprotein_position\tamino_acid\n")

    vcf_row = {}

    #Interface to the UniProt service
    u = UniProt(verbose=False)

    vcf_reader = vcf.Reader(open(args.vcf, 'r'))
    ENSP_PDB_UNIPROT_mapping_DataFram = pd.DataFrame(columns=['ENSP','UniProtID','PDB'])
    #creating a util function to store mapping of Uniprot and PDB_ID
    for record in vcf_reader:
        # VEP fields
        curr_ENSP = ''
        if "CSQ" in record.INFO:
            csq = record.INFO['CSQ']
            # BELOW: THERE ARE A COUPLE OF OPTIONS TO PROCEED
            # For going through annotations for all transcript
            for current_csq_element in csq:
                current_csq = current_csq_element.split('|')
                curr_ENSP = str(current_csq[26])
                if curr_ENSP != "":
                    # to get Protein ID given ENSP ID
                    current_protein_list = u.search(curr_ENSP,frmt="list")
                    for curr_protein in current_protein_list.split("\n"):
                        if curr_protein != "":
                            # to get PDB ID given protein id
                            mapping_Dictionary = u.mapping(fr="ID", to="PDB_ID", query=str(curr_protein))
                            if bool(mapping_Dictionary) == True :
                                if curr_ENSP not in ENSP_PDB_UNIPROT_mapping_DataFram.index:
                                    ENSP_PDB_UNIPROT_mapping_DataFram.loc[curr_ENSP] = pd.Series({'ENSP':curr_ENSP, 'UniProtID':mapping_Dictionary.keys(), 'PDB':mapping_Dictionary.values()})
    print(ENSP_PDB_UNIPROT_mapping_DataFram)
    # writing in a csv file
    for record in vcf_reader:
        current_chr = record.CHROM
        current_id = record.ID
        current_pos = record.POS
        current_ref = record.REF
        current_alt = ','.join(str(v) for v in record.ALT)

        # VEP fields
        current_gene, current_feature = '',''
        current_feature_type, current_consequence = '',''
        current_swissport,current_ENSP, current_protein, current_pdbid , current_protein_position, current_amino_acid = '','','','','',''
        if "CSQ" in record.INFO:
            csq = record.INFO['CSQ']

            # BELOW: THERE ARE A COUPLE OF OPTIONS TO PROCEED
            # For going through annotations for all transcript
            for current_csq_element in csq:
                current_csq = current_csq_element.split('|')
                current_consequence = current_csq[1]
                current_gene = current_csq[4]
                current_feature_type = current_csq[5]
                current_feature = current_csq[6]
                current_protein_position = current_csq[14]
                current_amino_acid = current_csq[15]
                current_ENSP = current_csq[27]
                current_swissport = current_csq[28]

                #if current_swissport_in_my_list(current_swissport, swissprot_pdb_)
                if current_ENSP in ENSP_PDB_UNIPROT_mapping_DataFram.index:
                    current_protein = ENSP_PDB_UNIPROT_mapping_DataFram.loc[current_ENSP]['UniProtID']
                    for item in ENSP_PDB_UNIPROT_mapping_DataFram.loc[current_ENSP]['PDB']:
                        current_pdbid = item
                        break;
                    out_str = [ current_chr, str(current_pos), str(current_id), current_ref, current_alt,
                                current_gene, current_feature, current_feature_type, current_consequence,current_swissport,current_ENSP, current_protein, current_pdbid , current_protein_position, current_amino_acid]
                else:
                    current_protein = ""
                    current_pdbid = ""
                    out_str = [ current_chr, str(current_pos), str(current_id), current_ref, current_alt,
                            current_gene, current_feature, current_feature_type, current_consequence,current_swissport,current_ENSP, current_protein, current_pdbid , current_protein_position, current_amino_acid]

                out_str = [x or 'None' for x in out_str]

                outputfile.write("\t".join(out_str))
                outputfile.write("\n")

        else:
            current_gene, current_feature = '',''
            current_feature_type, current_consequence = '',''
            current_swissport,current_ENSP, current_protein, current_pdbid , current_protein_position, current_amino_acid = '','','','','',''

            out_str = [ current_chr, str(current_pos), str(current_id), current_ref, current_alt,
                        current_gene, current_feature, current_feature_type, current_consequence,current_swissport,current_ENSP, current_protein, current_pdbid , current_protein_position, current_amino_acid]
            out_str = [x or 'None' for x in out_str]
            outputfile.write("\t".join(out_str))
            outputfile.write("\n")

    outputfile.close()

    logging.info('Start.')
    logging.info('Command line: {}'.format(' '.join(sys.argv)))

    # logging.info()

if __name__ == '__main__':
    main()
