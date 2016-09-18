from string import whitespace
from argparse import ArgumentParser
from version import varstructure_version
from string import whitespace
import logging
import os
import string
import sys
#Bioservices Library
from bioservices import UniProt
from bioservices import PDB
#BioPython Library
from Bio.PDB import *
#added for data structures
from collections import defaultdict
from collections import OrderedDict
import itertools
import pandas as pd

def AddingItemDataFram( ENSP_PDB_UNIPROT_mapping_DataFram ,strItemENSP):
    #Interface to the UniProt service
    u = UniProt(verbose=False)

   current_protein_list = u.search(strItemENSP,frmt="list")
   for current_protein in current_protein_list.split("\n"):
       if current_protein != "":
           # to get PDB ID given protein id
           mapping_Dictionary = u.mapping("ID", "PDB_ID", current_protein)
           if bool(mapping_Dictionary) == True :
               ENSP_PDB_UNIPROT_mapping_DataFram.loc[current_ENSP] = pd.Series({'ENSP':current_ENSP, 'UniProtID':ENSP_PDB_UNIPROT_mapping_Dictionary.keys(), 'PDB':ENSP_PDB_UNIPROT_mapping_Dictionary.values()})
return

def CheckItemInDataFram( ENSP_PDB_UNIPROT_mapping_DataFram, strItemENSP ):
   bool retValu=False
   if strItemENSP in ENSP_PDB_UNIPROT_mapping_DataFram:
       retValu = True

return retValu

def GetProteinIDFromDataFram(ENSP_PDB_UNIPROT_mapping_DataFram):
   str retValu=""
   if strItemENSP in ENSP_PDB_UNIPROT_mapping_DataFram:
       retValu = True

return retValu

def GetPDBinIDFromDataFram(ENSP_PDB_UNIPROT_mapping_DataFram):
   str retValu=""
   if strItemENSP in ENSP_PDB_UNIPROT_mapping_DataFram:
       retValu = True

return retValu
