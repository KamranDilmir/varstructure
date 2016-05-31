# -*- coding: utf-8 -*-

from string import whitespace
from argparse import ArgumentParser
from version import varstructure_version
from string import whitespace
import logging
import os
import string
import sys
import vcf

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--version", action='version', version='%(prog)s ' + varstructure_version)
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
    outputfile.write("chr\tpos\tid\tref\talt\tgene\tfeature\tfeature_type\tconsequence\n")

    vcf_row = {}

    vcf_reader = vcf.Reader(open(args.vcf, 'r'))
    for record in vcf_reader:
        current_chr = record.CHROM
        current_id = record.ID
        current_pos = record.POS
        current_ref = record.REF
        current_alt = ','.join(str(v) for v in record.ALT)

        # VEP fields
        current_gene, current_feature = '',''
        current_feature_type, current_consequence = '',''
        if "CSQ" in record.INFO:
            csq = record.INFO['CSQ']

            # BELOW: THERE ARE A COUPLE OF OPTIONS TO PROCEED
            # For going through annotations for all transcript
            for current_csq_element in csq:
                current_csq = current_csq_element.split('|')
                current_gene = current_csq[0]
                current_feature = current_csq[1]
                current_feature_type = current_csq[2]
                current_consequence = current_csq[3]
                out_str = [ current_chr, str(current_pos), str(current_id), current_ref, current_alt,
                            current_gene, current_feature, current_feature_type, current_consequence]
                out_str = [x or 'None' for x in out_str]
                outputfile.write("\t".join(out_str))
                outputfile.write("\n")

        else:
            current_gene, current_feature = '',''
            current_feature_type, current_consequence = '',''
            out_str = [ current_chr, str(current_pos), str(current_id), current_ref, current_alt,
                        current_gene, current_feature, current_feature_type, current_consequence]
            out_str = [x or 'None' for x in out_str]
            outputfile.write("\t".join(out_str))
            outputfile.write("\n")

    outputfile.close()

   # print "Hello!"

    logging.info('Start.')
    logging.info('Command line: {}'.format(' '.join(sys.argv)))

    # logging.info()

if __name__ == '__main__':
    main()
