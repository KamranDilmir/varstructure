# -*- coding: utf-8 -*-
import csv, sqlite3
import logging
from argparse import ArgumentParser
import sys
#Bioservices Library
from bioservices import UniProt
from bioservices import PDB
from bioservices import *
#BioPython Library
from Bio.PDB import *


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--log", type=str, help="Logs progress in specified file, defaults to stdout.")
    parser.add_argument("-v", "--verbosity", action="count", default=0)

    args = parser.parse_args()


    if args.verbosity >= 2:
        print "{} to the power {} equals {}".format(args.v, args.o, answer)
    elif args.verbosity >= 1:
        print "{}^{} == {}".format(args.x, args.y, answer)

    return args


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

    #Interface to the UniProt service
    u = UniProt(verbose=False)

    con = sqlite3.connect("PDB_Chain_Uniprot.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE PDB_Chain_Uniprot (PDB, CHAIN, SP_PRIMARY, RES_BEG, RES_END, PDB_BEG, PDB_END, SP_BEG, SP_END, Swissprot_Id);") # use your column names here

    with open('../DataFilesVarstructure/pdb_chain_uniprot.csv','rb') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        for row in dr:
            #res=u.search(str(row['SP_PRIMARY']),limit=1)
            #for line in res.split("\n")[1:-1]:
                #res_id, res_Entry_Name, res_status, res_protein_names, res_gene_names, res_organism, Length = line.split("\t")
                #to_db = [(row['PDB'], row['CHAIN'],row['SP_PRIMARY'],row['RES_BEG'],row['RES_END'],row['PDB_BEG'],row['PDB_END'],row['SP_BEG'],row['SP_END'],res_Entry_Name)]
            #to_db = [(row['PDB'], row['CHAIN'],row['SP_PRIMARY'],row['RES_BEG'],row['RES_END'],row['PDB_BEG'],row['PDB_END'],row['SP_BEG'],row['SP_END'],row['Entry_Name'])]
            to_db = [(row['PDB'], row['CHAIN'],row['SP_PRIMARY'],row['RES_BEG'],row['RES_END'],row['PDB_BEG'],row['PDB_END'],row['SP_BEG'],row['SP_END'],"")]
            cur.executemany("INSERT INTO PDB_Chain_Uniprot (PDB, CHAIN, SP_PRIMARY, RES_BEG, RES_END, PDB_BEG, PDB_END, SP_BEG, SP_END, Swissprot_Id) VALUES (?, ?,?,?,?,?,?,?,?,?);",to_db)
            #print(to_db)
    con.commit()
    con.close()

    logging.info('Start.')
    logging.info('Command line: {}'.format(' '.join(sys.argv)))

if __name__ == '__main__':
    main()
