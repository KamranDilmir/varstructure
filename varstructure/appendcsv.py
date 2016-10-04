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

    with open('../DataFilesVarstructure/pdb_chain_uniprot_1.csv','r') as csvinput:
        with open('../DataFilesVarstructure/pdb_chain_uniprot_2.csv', 'w') as csvoutput:
            writer = csv.writer(csvoutput)

            for row in csv.reader(csvinput):
                column_count = len(row)
                print(column_count)
                if column_count == 9:
                    if row[0] == "PDB":
                        writer.writerow(row + ["Entry_Name"])
                        print(row)
                    else:
                        res=u.search(str(row[2]),limit=1)
                        print(res)
                        if res != "" :
                            for line in res.split("\n")[1:-1]:
                                if(line != ""):
                                    print(line)
                                    res_id, res_Entry_Name, res_status, res_protein_names, res_gene_names, res_organism, Length = line.split("\t")
                                    strList =list()
                                    strList.append(res_Entry_Name)
                                    writer.writerow(row + strList)
if __name__ == '__main__':
    main()
