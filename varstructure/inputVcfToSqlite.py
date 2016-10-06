# -*- coding: utf-8 -*-
import csv, sqlite3
import logging
from argparse import ArgumentParser
import sys
import vcf


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

    cur.execute("DROP TABLE Input_VCF_CSQ ;") # remove the table if it already Exist
    #cur.execute("DROP TABLE Input_VCF_ANN ;") # remove the table if it already Exist

    #VEP Annotation
    #cur.execute("CREATE TABLE Input_VCF_CSQ (Id,Chrom,POS,Vep_Id,ref,alt_full,qual,filter,alt,csq_Allele,csq_Consequence, \
                #csq_IMPACT, csq_SYMBOL, csq_Gene, csq_Feature_type, csq_Feature,csq_Biotype, csq_Exon, csq_Intron,\
                #csq_HGVSc,csq_HGVSp,csq_cDNA_position,csq_CDS_position,csq_Protein_position,csq_Amino_acids,csq_Codons,\
                #csq_Existing_variation, csq_DISTANCE, csq_STRAND,csq_VARIANT_CLASS,csq_SYMBOL_SOURCE,csq_HGNC_ID, \
                #csq_CANONICAL,csq_TSL,csq_CCDS,csq_ENSP, csq_SWISSPROT, csq_TREMBL,csq_UNIPARC,csq_SIFT,\
                #csq_SIFT_TYPE,csq_SIFT_Score, \
                #csq_PolyPhen, csq_PolyPhen_Type, csq_PolyPhen_Score, \
                #csq_DOMAINS,csq_GMAF,csq_AFR_MAF,csq_AMR_MAF,csq_ASN_MAF,csq_EAS_MAF,csq_EUR_MAF, \
                #csq_SAS_MAF,csq_AA_MAF,csq_EA_MAF,csq_CLIN_SIG,csq_SOMATIC, \
                #csq_PHENO,csq_PUBMED,csq_MOTIF_NAME,csq_MOTIF_POS, \
                #csq_HIGH_INF_POS,csq_MOTIF_SCORE_CHANGE);") # use your column names here

    cur.execute("CREATE TABLE Input_VCF_CSQ (\
                Id,\
                Chrom,\
                POS,\
                Vep_Id,\
                ref,\
                alt_full,\
                qual,\
                filter,\
                alt,\
                csq_Allele,\
                csq_Consequence,\
                csq_IMPACT,\
                csq_Allele,\
                csq_Gene,\
                csq_Feature,\
                csq_Feature_type,\
                csq_Consequence,\
                csq_cDNA_position,\
                csq_CDS_position,\
                csq_Protein_position,\
                csq_Amino_acids,\
                csq_Codons,\
                csq_Existing_variation,\
                csq_DISTANCE,\
                csq_STRAND,\
                csq_SYMBOL,\
                csq_SYMBOL_SOURCE,\
                csq_HGNC_ID,\
                csq_BIOTYPE,\
                csq_CANONICAL,\
                csq_CCDS,\
                csq_ENSP,\
                csq_SWISSPROT,\
                csq_TREMBL,\
                csq_UNIPARC,\
                csq_SIFT,\
                csq_PolyPhen,\
                csq_EXON,\
                csq_INTRON,\
                csq_DOMAINS,\
                csq_HGVSc,\
                csq_HGVSp,\
                csq_GMAF,\
                csq_AFR_MAF,\
                csq_AMR_MAF,\
                csq_ASN_MAF,\
                csq_EUR_MAF,\
                csq_AA_MAF,\
                csq_EA_MAF,\
                csq_CLIN_SIG,\
                csq_SOMATIC,\
                csq_PUBMED,\
                csq_MOTIF_NAME,\
                csq_MOTIF_POS,\
                csq_HIGH_INF_POS,\
                csq_MOTIF_SCORE_CHANGE = '');")
    #SNPeff Annotation
    #cur.execute("CREATE TABLE Input_VCF_ANN (Id,Chrom,POS,Vep_Id,ref,alt_full,qual,filter,alt,csq_Allele,ann_Allele, \
                #ann_Annotation,ann_Annotation_Impact,ann_Gene_Name,ann_Gene_ID,ann_Feature_Type,ann_Feature_ID, \
                #ann_Transcript_BioType ann_Rank, ann_HGVSc, ann_HGVSp,ann_cDNA_pos,ann_cDNA_length,ann_CDS_pos, \
                #ann_CDS_length, ann_AA_pos, ann_AA_length, ann_Distance,ann_ERRORS,ann_WARNINGS,ann_INFO);") # use your column names here


    vcf_row = {}
    vcf_reader = vcf.Reader(open(args.vcf, 'r'))
    #ann_ID=1
    csq_ID=1
    # writing in a csv file
    for record in vcf_reader:
        current_chr = record.CHROM
        current_pos = record.POS
        current_id = record.ID
        current_ref = record.REF
        current_alt_full = record.ALT
        current_qual = record.QUAL
        current_filter = record.FILTER
        current_alt = ','.join(str(v) for v in record.ALT)

        # VEP fields
        current_csq_Allele = ''
        current_csq_Gene = ''
        current_csq_Feature = ''
        current_csq_Feature_type = ''
        current_csq_Consequence = ''
        current_csq_cDNA_position = ''
        current_csq_CDS_position = ''
        current_csq_Protein_position = ''
        current_csq_Amino_acids = ''
        current_csq_Codons = ''
        current_csq_Existing_variation = ''
        current_DISTANCE = ''
        current_csq_STRAND = ''
        current_csq_SYMBOL = ''
        current_csq_SYMBOL_SOURCE = ''
        current_csq_HGNC_ID = ''
        current_csq_BIOTYPE = ''
        current_csq_CANONICAL = ''
        current_csq_CCDS = ''
        current_csq_ENSP = ''
        current_csq_SWISSPROT = ''
        current_csq_TREMBL = ''
        current_csq_UNIPARC = ''
        current_csq_SIFT = ''
        current_csq_PolyPhen = ''
        current_csq_EXON = ''
        current_csq_INTRON = ''
        current_csq_DOMAINS = ''
        current_csq_HGVSc = ''
        current_csq_HGVSp = ''
        current_csq_GMAF = ''
        current_csq_AFR_MAF = ''
        current_csq_AMR_MAF = ''
        current_csq_ASN_MAF = ''
        current_csq_EUR_MAF = ''
        current_csq_AA_MAF = ''
        current_csq_EA_MAF = ''
        current_csq_CLIN_SIG = ''
        current_csq_SOMATIC = ''
        current_csq_PUBMED = ''
        current_csq_MOTIF_NAME = ''
        current_csq_MOTIF_POS = ''
        current_csq_HIGH_INF_POS = ''
        current_csq_MOTIF_SCORE_CHANGE = ''

        if "CSQ" in record.INFO:
            csq = record.INFO['CSQ']
            # BELOW: THERE ARE A COUPLE OF OPTIONS TO PROCEED
            # For going through annotations for all transcript
            for current_csq_element in csq:
                current_csq = current_csq_element.split('|')
                current_csq_Allele = current_csq[1]
                current_csq_Gene = current_csq[2]
                current_csq_Feature = current_csq[3]
                current_csq_Feature_type = current_csq[4]
                current_csq_Consequence = current_csq[5]
                current_csq_cDNA_position = current_csq[6]
                current_csq_CDS_position = current_csq[7]
                current_csq_Protein_position = current_csq[8]
                current_csq_Amino_acids = current_csq[9]
                current_csq_Codons = current_csq[10]
                current_csq_Existing_variation = current_csq[11]
                current_DISTANCE = current_csq[12]
                current_csq_STRAND = current_csq[13]
                current_csq_SYMBOL = current_csq[14]
                current_csq_SYMBOL_SOURCE = current_csq[15]
                current_csq_HGNC_ID = current_csq[16]
                current_csq_BIOTYPE = current_csq[17]
                current_csq_CANONICAL = current_csq[18]
                current_csq_CCDS = current_csq[20]
                current_csq_ENSP = current_csq[21]
                current_csq_SWISSPROT = current_csq[22]
                current_csq_TREMBL = current_csq[23]
                current_csq_UNIPARC = current_csq[24]
                current_csq_SIFT = current_csq[25]
                current_csq_PolyPhen = current_csq[26]
                current_csq_EXON = current_csq[27]
                current_csq_INTRON = current_csq[28]
                current_csq_DOMAINS = current_csq[29]
                current_csq_HGVSc = current_csq[30]
                current_csq_HGVSp = current_csq[31]
                current_csq_GMAF = current_csq[32]
                current_csq_AFR_MAF = current_csq[33]
                current_csq_AMR_MAF = current_csq[34]
                current_csq_ASN_MAF = current_csq[35]
                current_csq_EUR_MAF = current_csq[36]
                current_csq_AA_MAF = current_csq[37]
                current_csq_EA_MAF = current_csq[38]
                current_csq_CLIN_SIG = current_csq[39]
                current_csq_SOMATIC = current_csq[40]
                current_csq_PUBMED = current_csq[41]
                current_csq_MOTIF_NAME = current_csq[42]
                current_csq_MOTIF_POS = current_csq[43]
                current_csq_HIGH_INF_POS = current_csq[44]
                current_csq_MOTIF_SCORE_CHANGE = current_csq[45]

                cur.executemany("INSERT INTO Input_VCF_CSQ (Id,\
                Chrom,\
                POS,\
                Vep_Id,\
                ref,\
                alt_full,\
                qual,\
                filter,\
                alt,\
                csq_Allele,\
                csq_Consequence,\
                csq_IMPACT,\
                csq_Allele,\
                csq_Gene,\
                csq_Feature,\
                csq_Feature_type,\
                csq_Consequence,\
                csq_cDNA_position,\
                csq_CDS_position,\
                csq_Protein_position,\
                csq_Amino_acids,\
                csq_Codons,\
                csq_Existing_variation,\
                csq_DISTANCE,\
                csq_STRAND,\
                csq_SYMBOL,\
                csq_SYMBOL_SOURCE,\
                csq_HGNC_ID,\
                csq_BIOTYPE,\
                csq_CANONICAL,\
                csq_CCDS,\
                csq_ENSP,\
                csq_SWISSPROT,\
                csq_TREMBL,\
                csq_UNIPARC,\
                csq_SIFT,\
                csq_PolyPhen,\
                csq_EXON,\
                csq_INTRON,\
                csq_DOMAINS,\
                csq_HGVSc,\
                csq_HGVSp,\
                csq_GMAF,\
                csq_AFR_MAF,\
                csq_AMR_MAF,\
                csq_ASN_MAF,\
                csq_EUR_MAF,\
                csq_AA_MAF,\
                csq_EA_MAF,\
                csq_CLIN_SIG,\
                csq_SOMATIC,\
                csq_PUBMED,\
                csq_MOTIF_NAME,\
                csq_MOTIF_POS,\
                csq_HIGH_INF_POS,\
                csq_MOTIF_SCORE_CHANGE = '') \
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?);",\
                            csq_ID,
                            current_chr,
                            current_pos,
                            current_id,
                            current_ref,
                            current_alt_full,
                            current_qual,
                            current_filter,
                            current_alt,
                            current_csq_Allele,
                            current_csq_Gene,
                            current_csq_Feature,
                            current_csq_Feature_type,
                            current_csq_Consequence,
                            current_csq_cDNA_position,
                            current_csq_CDS_position,
                            current_csq_Protein_position,
                            current_csq_Amino_acids,
                            current_csq_Codons,
                            current_csq_Existing_variation,
                            current_DISTANCE,
                            current_csq_STRAND,
                            current_csq_SYMBOL,
                            current_csq_SYMBOL_SOURCE,
                            current_csq_HGNC_ID,
                            current_csq_BIOTYPE,
                            current_csq_CANONICAL,
                            current_csq_CCDS,
                            current_csq_ENSP,
                            current_csq_SWISSPROT,
                            current_csq_TREMBL,
                            current_csq_UNIPARC,
                            current_csq_SIFT,
                            current_csq_PolyPhen,
                            current_csq_EXON,
                            current_csq_INTRON,
                            current_csq_DOMAINS,
                            current_csq_HGVSc,
                            current_csq_HGVSp,
                            current_csq_GMAF,
                            current_csq_AFR_MAF,
                            current_csq_AMR_MAF,
                            current_csq_ASN_MAF,
                            current_csq_EUR_MAF,
                            current_csq_AA_MAF,
                            current_csq_EA_MAF,
                            current_csq_CLIN_SIG,
                            current_csq_SOMATIC,
                            current_csq_PUBMED,
                            current_csq_MOTIF_NAME,
                            current_csq_MOTIF_POS,
                            current_csq_HIGH_INF_POS,
                            current_csq_MOTIF_SCORE_CHANGE,)

                            csq_ID= csq_ID + 1
"""
        if "ANN" in record.INFO:
            csq = record.INFO['ANN']
            # BELOW: THERE ARE A COUPLE OF OPTIONS TO PROCEED
            # For going through annotations for all transcript
            for current_csq_element in csq:
                current_csq = current_csq_element.split('|')
                current_consequence = current_csq[1]
                current_gene = current_csq[3]
                current_feature_type = current_csq[5]
                current_feature = current_csq[6]
                current_protein_position = current_csq[14]
                current_amino_acid = current_csq[15]
                current_ENSP = current_csq[26]
                current_swissprot = current_csq[27]

                cur.executemany("INSERT INTO Input_VCF_ANN (Id,Chrom,POS,Vep_Id,ref,alt_full,qual,filter,alt,csq_Allele,ann_Allele, \
                            ann_Annotation,ann_Annotation_Impact,ann_Gene_Name,ann_Gene_ID,ann_Feature_Type,ann_Feature_ID, \
                            ann_Transcript_BioType ann_Rank, ann_HGVSc, ann_HGVSp,ann_cDNA_pos,ann_cDNA_length,ann_CDS_pos, \
                            ann_CDS_length, ann_AA_pos, ann_AA_length, ann_Distance,ann_ERRORS,ann_WARNINGS,ann_INFO)
                            VALUES (?, ?,?,?,?,?,?,?,?,?);" \
                            , )
                            ann_ID = ann_ID + 1
    """

    else:


        cur.executemany("INSERT INTO Input_VCF_CSQ (Id,\
        Chrom,\
        POS,\
        Vep_Id,\
        ref,\
        alt_full,\
        qual,\
        filter,\
        alt,\
        csq_Allele,\
        csq_Consequence,\
        csq_IMPACT,\
        csq_Allele,\
        csq_Gene,\
        csq_Feature,\
        csq_Feature_type,\
        csq_Consequence,\
        csq_cDNA_position,\
        csq_CDS_position,\
        csq_Protein_position,\
        csq_Amino_acids,\
        csq_Codons,\
        csq_Existing_variation,\
        csq_DISTANCE,\
        csq_STRAND,\
        csq_SYMBOL,\
        csq_SYMBOL_SOURCE,\
        csq_HGNC_ID,\
        csq_BIOTYPE,\
        csq_CANONICAL,\
        csq_CCDS,\
        csq_ENSP,\
        csq_SWISSPROT,\
        csq_TREMBL,\
        csq_UNIPARC,\
        csq_SIFT,\
        csq_PolyPhen,\
        csq_EXON,\
        csq_INTRON,\
        csq_DOMAINS,\
        csq_HGVSc,\
        csq_HGVSp,\
        csq_GMAF,\
        csq_AFR_MAF,\
        csq_AMR_MAF,\
        csq_ASN_MAF,\
        csq_EUR_MAF,\
        csq_AA_MAF,\
        csq_EA_MAF,\
        csq_CLIN_SIG,\
        csq_SOMATIC,\
        csq_PUBMED,\
        csq_MOTIF_NAME,\
        csq_MOTIF_POS,\
        csq_HIGH_INF_POS,\
        csq_MOTIF_SCORE_CHANGE = '') \
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                            ?,?,?,?,?,?,?,?,?,?);",\
                    csq_ID,
                    current_chr,
                    current_pos,
                    current_id,
                    current_ref,
                    current_alt_full,
                    current_qual,
                    current_filter,
                    current_alt,
                    current_csq_Allele,
                    current_csq_Gene,
                    current_csq_Feature,
                    current_csq_Feature_type,
                    current_csq_Consequence,
                    current_csq_cDNA_position,
                    current_csq_CDS_position,
                    current_csq_Protein_position,
                    current_csq_Amino_acids,
                    current_csq_Codons,
                    current_csq_Existing_variation,
                    current_DISTANCE,
                    current_csq_STRAND,
                    current_csq_SYMBOL,
                    current_csq_SYMBOL_SOURCE,
                    current_csq_HGNC_ID,
                    current_csq_BIOTYPE,
                    current_csq_CANONICAL,
                    current_csq_CCDS,
                    current_csq_ENSP,
                    current_csq_SWISSPROT,
                    current_csq_TREMBL,
                    current_csq_UNIPARC,
                    current_csq_SIFT,
                    current_csq_PolyPhen,
                    current_csq_EXON,
                    current_csq_INTRON,
                    current_csq_DOMAINS,
                    current_csq_HGVSc,
                    current_csq_HGVSp,
                    current_csq_GMAF,
                    current_csq_AFR_MAF,
                    current_csq_AMR_MAF,
                    current_csq_ASN_MAF,
                    current_csq_EUR_MAF,
                    current_csq_AA_MAF,
                    current_csq_EA_MAF,
                    current_csq_CLIN_SIG,
                    current_csq_SOMATIC,
                    current_csq_PUBMED,
                    current_csq_MOTIF_NAME,
                    current_csq_MOTIF_POS,
                    current_csq_HIGH_INF_POS,
                    current_csq_MOTIF_SCORE_CHANGE,)

        #cur.executemany("INSERT INTO Input_VCF_ANN (PDB, CHAIN, SP_PRIMARY, RES_BEG, RES_END, PDB_BEG, PDB_END, SP_BEG, SP_END, Swissprot_Id) VALUES (?, ?,?,?,?,?,?,?,?,?);",to_db)
        csq_ID = csq_ID + 1
        #ann_ID = ann_ID + 1


    con.commit()
    con.close()

    logging.info('Start.')
    logging.info('Command line: {}'.format(' '.join(sys.argv)))

if __name__ == '__main__':
    main()
