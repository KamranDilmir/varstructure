# -*- coding: utf-8 -*-

from string import whitespace
from argparse import ArgumentParser
from version import pedtools_version
from string import whitespace
import logging
import os
import string
import sys
import vcf

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--version", action='version', version='%(prog)s ' + pedtools_version)
    parser.add_argument("--vcf", type=str, dest="vcf", help="Input variant file (vcf)", required=True)
    parser.add_argument("--output", type=str, dest="out", help="Output file (tabular)", required=True)
    parser.add_argument("--log", type=str, help="Logs progress in specified file, defaults to stdout.")
    parser.add_argument("-v", "--verbosity", action="count", default=0)

    args = parser.parse_args()


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

    print "Hello!"

    logging.info('Start.')
    logging.info('Command line: {}'.format(' '.join(sys.argv)))

    # logging.info()

if __name__ == '__main__':
    main()
