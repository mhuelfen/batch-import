# encoding: utf-8

'''
Script to convert similarity relation of the weltmodell for import into neo4j.

@author: Michael A. Huelfenhaus
'''
import sys
import csv
import hashlib
import re

from getopt import getopt, GetoptError

help_message = '''
usage: python extract_binary_rels.py <weltmodell_tsv_file> <result_tsv_file_for_rels>

Script to convert similarity relation of the weltmodell for import into neo4j.
'''

re_verb = re.compile('\} (may .*?) \{');

# to exclude to unsign. value and normalize the rest

cos_threshold = 0.88

max_cos = 1
min_cos = 1 - 0.88

mode = 'stat'

def normalize_cos(cos):
    '''
    normalize cos value to value between 0 and 1 where 1 is the max value seen and to make it compareable to pmi value
    '''

    return (1 - cos - min_cos) / cos_threshold

def convert_wm(wm_path, result_path_rels):
    '''
    Converts a weltmodell tsv file into a conceptnet plain json file.
    '''
    line_count = 0
    # start writing result files
    with open(result_path_rels, 'w') as result_file_rels:
        # start files
        if (mode == 'nouns'):
            result_file_rels.write('word:string:nouns\tterm:string:nouns\ttype\tcos:float\tweight:float\n')
        else:
            result_file_rels.write('word:string:stats\tterm:string:stats\ttype\tcos:float\tweight:float\n')
        
         # read wm file
        with open(wm_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                if (mode == 'nouns'):
                    rel = 'SIM_NOUN'
                else:
                    rel = 'SIM_STAT'

                cos = float(row[2])

                if (cos < cos_threshold):

                    norm_cos = normalize_cos(cos)

                    # print row
                    line = row[0] + '\t' + row[1] + '\t' + rel + '\t' + row[2] + '\t' + str(norm_cos)
                    result_file_rels.write(line + '\n')

                line_count += 1
                if line_count  % 1000 == 0:
                    print line_count, 'relation lines converted'
    print line_count, ' lines wrote. Result written to', result_path_rels

if __name__ == "__main__":
    '''
    This block is called when the .py file is started from the shell
    '''

    # checking command line options
    try:
        options, args = getopt(sys.argv[1:], "")
    except GetoptError:
        print >> sys.stderr, help_message
        sys.exit(2)
    
    # checking number of params     
    if len(args) != 2:
        print >> sys.stderr, help_message
        sys.exit(2)

    wm_path = args[0]
    result_path_rels = args[1]

    convert_wm(wm_path, result_path_rels)