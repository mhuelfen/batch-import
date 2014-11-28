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
usage: python extract_binary_rels.py <weltmodell_tsv_file> <result_tsv_file_in_state> <result_tsv_file_binary>

Converts weltmodell file for import into neo4j with the batch importer.

binary relations are split are created with the verb as relation between the nouns
all other with the IN_STATE relation between noun and statement
'''

re_verb = re.compile('\} (may .*?) \{');


# def make_json_line(wm_line, concepts):
#     '''
#     Transforms an weltmodell line into a conceptnet json line.
#     '''
#     # extract realtion

#     rel = wm_line[1].replace('{___}','').strip().replace(' ','_')

#     rel_url = base_rel_url + rel
#     start_url = base_concept_url + concepts[0].strip().replace(' ','_')
#     end_url = base_concept_url + concepts[1].strip().replace(' ','_')

#     features = '["' + start_url + ' ' + rel_url + ' -","' + start_url + ' ' + rel_url + ' -","' + '- ' +rel_url + ' ' + end_url + '"]'

#     uri = '/a/[' + rel_url + ',' + start_url + ',' + end_url + ']'

#     norm_pmi = wm_line[14]
#     weight = norm_pmi

#     # TODO add all verbargs to surface text
#     surface_text = wm_line[19]

#     # make id
#     id_str = make_id(uri, weight, surface_text)

#     json_items= [uri, weight, dataset, end_url, surface_text, start_url, license,
#         id_str
# , source_uri, sources, context, features, rel_url]
#     #make json line
#     json_line = '{'
#     json_line += '"uri": "' + uri + '",'
#     json_line += '"weight": ' + norm_pmi + ','
#     json_line += '"dataset": "' + dataset + '",'
#     json_line += '"surfaceText": "' + surface_text + '",'
#     json_line += '"start": "' + start_url + '",'
#     json_line += '"license": "' + license + '",'
#     json_line += '"id": "' + id_str + '",'
#     json_line += '"source_uri": "' + source_uri + '",'
#     json_line += '"sources": ' + sources + ','
#     json_line += '"context": "' + context + '",'
#     json_line += '"features": ' + features + ','
#     json_line += '"rel": "' + rel_url + '"'
#     json_line += '}'

#     # print wm_line
#     return json_line


def convert_wm(wm_path, result_path_in_state, result_path_binary):
    '''
    Converts a weltmodell tsv file into a conceptnet plain json file.
    '''
    line_count = 0
    # start writing result files
    with open(result_path_in_state, 'w') as result_file_in_state:
        with open(result_path_binary, 'w') as result_file_binary:
            # start files
            result_file_in_state.write('word:string:nouns\tterm:string:stats\ttype\tpmi:float\n')
            result_file_binary.write('word:string:nouns\tword:string:nouns\ttype\tpmi:float\n')

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
                            line = concepts[0].strip() + '\t' + concepts[1].strip() + '\t' + verb.replace(' ','_').upper() + '\t' + row[14]
                            result_file_binary.write(line + '\n')
                        except Exception, e:
                            print row
                    else: 
                        line = row[3] + '\t' + row[2] + '\t' + 'IN_STATE' + '\t' + row[14]
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