# -*- coding: utf-8 -*-
import csv, sqlite3
import logging
from argparse import ArgumentParser
import sys
import vcf
from vcf_parser import VCFParser


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


    con = sqlite3.connect("PDB_Chain_Uniprot.db")
    cur = con.cursor()

    cur.execute("DROP TABLE Input_VCF_CSQ;") # remove the table if it already Exist

    #VEP Annotation
    cur.execute("CREATE TABLE Input_VCF_CSQ (Chrom,POS,Vep_Id,REF,ALT_Full,QUAL,FILTER);")

    vcf_row = {}
    vcf_reader = vcf.Reader(open(args.vcf, 'r'))

    # CSQ
    len_csq_remove = vcf_reader.infos['CSQ'].desc.find(":")
    csq_header = vcf_reader.infos['CSQ'].desc[0:len_csq_remove+2]
    current_csq_header = vcf_reader.infos['CSQ'].desc.replace(csq_header,"").split('|')
    print(current_csq_header)

    for current_csq_sub_header in current_csq_header:
        print(current_csq_sub_header)
        cur.execute('ALTER TABLE Input_VCF_CSQ ADD COLUMN ' + str(current_csq_sub_header))
        con.commit()

    for record in vcf_reader:
        #','.join(str(v) for v in record.ALT)
        to_db_master = [str(record.CHROM), str(record.POS),str(record.ID),str(record.REF),"",str(record.QUAL),""]

        if "CSQ" in record.INFO:
            csq = record.INFO['CSQ']
            current_csq_sub_element=[]
            # For going through annotations for all transcript
            for current_csq_element in csq:
                #current_csq = current_csq_element.split('|')
                current_csq_sub_element = current_csq_element.split("|")

                print(to_db_master)

                #VALUES(?,?,?,?,?,?,?)",to_db_master)
                cur.executemany("INSERT INTO Input_VCF_CSQ \
                                 VALUES (?,?,?,?,?,?,?,?,?,?,\
                                        ?,?,?,?,?,?,?,?,?,?,\
                                        ?,?,?,?,?,?,?,?,?,?,\
                                        ?,?,?,?,?,?,?,?,?,?,\
                                        ?,?,?,?,?,?,?,?,?,?,?)",\
                                        ((to_db_master + current_csq_sub_element),))
                con.commit()
        else :
            to_db_csq_child =["","","","","","","","","","",\
                       "","","","","","","","","","",\
                       "","","","","","","","","","",\
                       "","","","","","","","","","",\
                       "","","",""]
            print(to_db_master)
            print(to_db_csq_child)

            cur.executemany("INSERT INTO Input_VCF_CSQ \
                             VALUES (?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,?)",\
                                    ((to_db_master + to_db_csq_child),))
            con.commit()

    con.close()

    logging.info('Start.')
    logging.info('Command line: {}'.format(' '.join(sys.argv)))

if __name__ == '__main__':
    main()
