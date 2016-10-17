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
    cur.execute("DROP TABLE Input_VCF_ANN ;") # remove the table if it already Exist

    #VEP Annotation
    cur.execute("CREATE TABLE Input_VCF_CSQ (Chrom,POS,Vep_Id,REF,ALT_Full,QUAL,FILTER);")
    #SNPeff Annotation
    cur.execute("CREATE TABLE Input_VCF_ANN (Chrom,POS,Vep_Id,REF,ALT_Full,QUAL,FILTER);")

    vcf_row = {}
    vcf_reader = vcf.Reader(open(args.vcf, 'r'))

    #my_parser = VCFParser(infile=args.vcf, split_variants=True, check_info=True)
    #my_parser = VCFParser(infile=args.vcf, split_variants=True, check_info=True)
    #my_parser = VCFParser(infile=args.vcf)
    #for line in my_parser.metadata.print_header():
        #if "CSQ" in line['info_dict']:
            #csq = line['info_dict']['CSQ']
            #print(csq)
        #print(line)
    #for variant in my_parser:
        #print('\t'.join(([variant[head] for head in my_parser.header])))

    #for variant in my_parser:
        #print(variant)
        #print(variant['CHROM'])
        #print(variant['ALT'])
        #print(variant['info_dict']['CSQ'][2])
        #break

    len_csq_remove = vcf_reader.infos['CSQ'].desc.find(":")
    csq_header = vcf_reader.infos['CSQ'].desc[0:len_csq_remove+2]

    for current_csq_header in vcf_reader.infos['CSQ'].desc.replace(csq_header,"").split('|'):
        print(current_csq_header)
        cur.execute('ALTER TABLE Input_VCF_CSQ ADD COLUMN ' + str(current_csq_header))

    len_ann_remove = vcf_reader.infos['ANN'].desc.find(":")
    ann_header = vcf_reader.infos['ANN'].desc[0:len_ann_remove+2]

    for current_ann_header in vcf_reader.infos['ANN'].desc.replace(ann_header,"").split('|'):
        sub_header =False
        #print(current_ann_header)
        for current_ann_sub_header in current_ann_header.split("/"):
            #print(current_ann_sub_header)
            cur.execute('ALTER TABLE Input_VCF_ANN ADD COLUMN ' + str(current_ann_sub_header.replace("'","").replace(".","_")))
            sub_header =True
        if sub_header == False:
            cur.execute('ALTER TABLE Input_VCF_ANN ADD COLUMN ' + str(current_ann_header.replace("'","").replace(".","_")))

    con.commit()

    for record in vcf_reader:
        #','.join(str(v) for v in record.ALT)
        to_db_master = [(record.CHROM, record.POS,record.ID,record.REF,record.ALT,record.QUAL,record.FILTER)]

        if "CSQ" in record.INFO:
            csq = record.INFO['CSQ']
            # For going through annotations for all transcript
            for current_csq_element in csq:
                #current_csq = current_csq_element.split('|')
                current_csq = current_csq_element.replace("|",",")
                cur.executemany("INSERT INTO Input_VCF_CSQ
                            VALUES (?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,?);",\
                                    to_db_master,current_csq )
                con.commit()

        else if "ANN" in record.INFO:
            ann = record.INFO['ANN']
            # For going through annotations for all transcript
            for current_ann_element in ann:
                current_ann = current_ann_element.split('|')

                for current_ann_sub_child in current_ann.split("/"):
                    #myList = ['a','b','c','d']
                    #myString = ",".join(myList )
                    to_db_ann_child = ','.join(map(current_ann_sub_child, to_db_ann_child))


                    cur.executemany("INSERT INTO Input_VCF_CSQ
                            VALUES (?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,?);",\
                                    to_db_master,to_db_ann_child )
            con.commit()

        else :
            to_db_child =[("","","","","","","","","","",\
                       "","","","","","","","","","",\
                       "","","","","","","","","","",\
                       "","","")]
        cur.executemany("INSERT INTO Input_VCF_CSQ
                VALUES (?,?,?,?,?,?,?,?,?,?,\
                        ?,?,?,?,?,?,?,?,?,?,\
                        ?,?,?,?,?,?,?,?,?,?,\
                        ?,?,?,?,?,?,?,?,?,?,?);",\
                        to_db_master,to_db_child )
        con.commit()

    con.close()

    logging.info('Start.')
    logging.info('Command line: {}'.format(' '.join(sys.argv)))

if __name__ == '__main__':
    main()
