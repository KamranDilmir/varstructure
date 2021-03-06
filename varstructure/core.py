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
import sqlite3

from Bio import SwissProt
from flask import Flask, render_template

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
    
app = Flask(__name__)

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
    outputfile.write("chr\tpos\tid\tref\talt\tgene\tfeature\tfeature_type\tconsequence\tswissprotid\tcurrent_ENSP\tuniprotid\tpdbid\tprotein_position\tamino_acid\n")

    vcf_row = {}

    #Interface to the UniProt service
    u = UniProt(verbose=False)
    vcf_reader = vcf.Reader(open(args.vcf, 'r'))
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
        current_swissprot,current_ENSP, current_protein, current_pdbid , current_protein_position, current_amino_acid = '','','','','',''
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
                current_ENSP = current_csq[26]
                current_swissprot = current_csq[27]
                # only cosider missense mutation
                con = sqlite3.connect("PDB_Chain_Uniprot.db")
                cur = con.cursor()
                #print(current_swissprot)

                if current_swissprot != "":
                    cur.execute("SELECT PDB,SP_PRIMARY FROM PDB_Chain_Uniprot WHERE Swissprot_Id =?",(str(current_swissprot),))
                    rows = cur.fetchall()
                    #print(rows)
                    for row in rows:
                        #print(row)
                        current_pdbid = row[0]
                        #print(row[0])
                        current_protein = row[1]
                        #print(row[1])
                        #print(current_pdbid)
                        #print(current_protein)
                        break;
                            #out_str = [ current_chr, str(current_pos), str(current_id), current_ref, current_alt,current_gene, current_feature, current_feature_type, current_consequence,current_swissport,current_ENSP, current_protein, str(current_pdbid) , current_protein_position, current_amino_acid]
                else:
                    current_protein = ""
                    current_pdbid = ""

                out_str = [ current_chr, str(current_pos), str(current_id), current_ref, current_alt,current_gene, current_feature, current_feature_type, current_consequence,current_swissprot,current_ENSP, current_protein, current_pdbid , current_protein_position, current_amino_acid]
                out_str = [x or 'None' for x in out_str]
                outputfile.write("\t".join(out_str))
                outputfile.write("\n")
                con.commit()
                con.close()
        else:
            current_gene, current_feature = '',''
            current_feature_type, current_consequence = '',''
            current_swissprot,current_ENSP, current_protein, current_pdbid , current_protein_position, current_amino_acid = '','','','','',''

            out_str = [ current_chr, str(current_pos), str(current_id), current_ref, current_alt,
                        current_gene, current_feature, current_feature_type, current_consequence,current_swissprot,current_ENSP, current_protein, current_pdbid , current_protein_position, current_amino_acid]
            out_str = [x or 'None' for x in out_str]
            outputfile.write("\t".join(out_str))
            outputfile.write("\n")

    outputfile.close()
    logging.info('Start.')
    logging.info('Command line: {}'.format(' '.join(sys.argv)))


@app.route("/")
def flskmain():
    return render_template('index0.html')

    # logging.info()

if __name__ == '__main__':
    main()
    app.run()
