# encoding: utf-8

'''
Converts weltmodell file for import into neo4j with the batch importer.

binary relations are split are created with the verb as relation between the nouns
all other with the IN_STATE relation between noun and statement

@author: Michael A. Huelfenhaus
'''
import sys
import csv
import hashlib
import re

from getopt import getopt, GetoptError

help_message = '''
usage: python extract_binary_rels_doubles.py <weltmodell_tsv_file> <result_tsv_file_in_state> <result_tsv_file_binary>

Needs sorted noun state file
cat noun_state.csv | sort -t$'\t' -k 1,1 -k 5,5 > noun_state_sorted.csv

Converts weltmodell file for import into neo4j with the batch importer.

binary relations are split are created with the verb as relation between the nouns
all other with the IN_STATE relation between noun and statement

double relations from the same frame but different statment are used only once -> only first and its pmi value

e.g.
be  {___} may be under {___}    {___} may be under {sun}    country [country, sun]  721773  52311   3121    1644927 21  33435   14  2098370619  1.744369007845882   0.09266054477531005 24.421166109842346  2001

be  {___} may be under {___}    {country} may be under {___}    sun [country, sun]  2676879 4003    2614    1189271 34  14876   14  2098370619  2.245996347903166   0.11930689219081306 31.443948870644327  2001
'''

re_verb = re.compile('\} (may .*?) \{');

max_pmi = 0.899047333178
min_pmi = 2.5076055075e-08

def normalize_pmi (pmi):
    '''
    normalize pmi value to value between 0 and 1 where 1 is the max value seen
    '''

    return (pmi - min_pmi) / (max_pmi - min_pmi)


def convert_wm(wm_path, result_path_in_state, result_path_binary):
    '''
    Converts a weltmodell tsv file into a conceptnet plain json file.
    '''
    line_count = 0

    last_concepts = ''
    last_frame = ''
    last_row = ''
    # start writing result files
    with open(result_path_in_state, 'w') as result_file_in_state:
        with open(result_path_binary, 'w') as result_file_binary:
            # start files
            result_file_in_state.write('word:string:nouns\tterm:string:stats\ttype\tpmi:float\tweight:float\n')
            result_file_binary.write('word:string:nouns\tword:string:nouns\ttype\tpmi:float\tweight:float\n')

             # read wm file
            with open(wm_path, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')

                for row in reader:
                    # print row
                    # filter for binary relations
                    concepts = row[4][1:-1].split(', ')
                    #print len(concepts) , row[4]
                    if len(concepts) == 2:


                        match = re.search(re_verb, row[2])
                        try:
                            verb = match.group(1)
                            norm_pmi = normalize_pmi(float(row[14]))
                            line = concepts[0].strip() + '\t' + concepts[1].strip() + '\t' + verb.replace(' ','_').upper() + '\t' + row[14] + '\t' + str(norm_pmi)
                            # skip entry if last line had same frame and concepts even PMI is different
                            if (row[1] == last_frame and concepts == last_concepts):
                                # print row
                                # print last_row
                                pass
                            else:
                                result_file_binary.write(line + '\n')
                        except Exception, e:
                            print row

                        last_concepts = concepts
                        last_frame = row[1]
                        last_row = row
                    else: 
                        norm_pmi = normalize_pmi(float(row[14]))
                        line = row[3] + '\t' + row[2] + '\t' + 'IN_STATE' + '\t' + row[14] + '\t' + str(norm_pmi)
                        result_file_in_state.write(line + '\n')

                    line_count += 1
                    if line_count  % 1000 == 0:
                        print line_count, 'relation lines converted'
    print line_count, ' lines wrote. Result written to', result_path_in_state, ' and ' + result_path_binary 

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
    if len(args) != 3:
        print >> sys.stderr, help_message
        sys.exit(2)

    wm_path = args[0]
    result_path_in_state = args[1]
    result_path_binary = args[2]

    convert_wm(wm_path, result_path_in_state, result_path_binary)