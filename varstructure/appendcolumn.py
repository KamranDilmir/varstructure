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

    cur.execute("SELECT SP_PRIMARY FROM PDB_Chain_Uniprot WHERE Swissprot_Id = '' LIMIT 1000" )
    #cur.execute("SELECT SP_PRIMARY FROM PDB_Chain_Uniprot WHERE Swissprot_Id =?",(str(current_swissprot),))
    rows = cur.fetchall()
    for row in rows:
        #print(str(row[0]))
        res = u.search(str(row[0]),limit=1)
        #print(res)
        if res != "" :
            for line in res.split("\n")[1:-1]:
                if(line != ""):
                    res_id, res_Entry_Name, res_status, res_protein_names, res_gene_names, res_organism, Length = line.split("\t")
                    cur.execute("UPDATE PDB_Chain_Uniprot SET Swissprot_Id=?  WHERE SP_PRIMARY = ?",(str(res_Entry_Name),str(row[0]),))
                    con.commit()
    con.close()

if __name__ == '__main__':
    main()
