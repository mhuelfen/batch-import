# encoding: utf-8

'''
Converts some coneptnet data for import into neo4j with the batch importer.

@author: Michael A. Huelfenhaus
'''
import sys
import csv
import hashlib
import re

from getopt import getopt, GetoptError

help_message = '''
usage: python extract_binary_rels.py <conceptnet_tsv_file> <result_tsv_file_cn_rels>

Converts weltmodell file for import into neo4j with the batch importer.

binary relations are split are created with the verb as relation between the nouns
all other with the IN_STATE relation between noun and statement
'''

causal_rels = ['/r/UsedFor','/r/Causes','/r/HasSubevent','/r/HasFirstSubevent',
    '/r/HasLastSubevent','/r/HasPrerequisite','/r/MotivatedByGoal','/r/CreatedBy',
    '/r/CapableOf']

def get_words_from_concept (concept):
    words = concept.split('/')[-1].split('_')
    return words


def convert_cn(cn_path, result_path_cn_rels):
    '''
    Converts a weltmodell tsv file into a conceptnet plain json file.
    '''
    line_count = 0
    single_word_rel_count = 0

    # start writing result files
    with open(result_path_cn_rels, 'w') as result_file_in_state:

        # start files
        result_file_in_state.write('word:string:nouns\tword:string:nouns\ttype\n')
        # result_file_binary.write('word:string:nouns\tword:string:nouns\ttype\tpmi:float\n')

         # read wm file
        with open(cn_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')

            for row in reader:
                # print row
                # make sure concept is english
                if (row[2].split('/')[2] == 'en' and row[3].split('/')[2] == 'en'):
                    rel = row[1]
                    start = get_words_from_concept(row[2])
                    end = get_words_from_concept(row[3])
                    if (rel in causal_rels):
                        # print rel, start, end
                        line_count += 1
                        if (len(start) == 1 and len(end) == 1):
                            single_word_rel_count += 1
                            line = start[0] + '\t' + end[0] + '\t' + rel[3:]
                            print line
                            result_file_in_state.write(line + '\n')

                    # filter for binary relations
                    # concepts = row[4][1:-1].split(', ')
                    #print len(concepts) , row[4]


                    if line_count  % 1000 == 0:
                        print line_count, 'relation lines converted', single_word_rel_count,'single word rels'


    print line_count, ' lines wrote. Result written to', result_path_cn_rels, single_word_rel_count,'single word rels'

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

    cn_path = args[0]
    result_path_cn_rels = args[1]
    # result_path_binary = args[2]

    convert_cn(cn_path, result_path_cn_rels)