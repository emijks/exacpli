import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        # read `ExACpLI_values.txt` and get `self.pli_data` dictionary object (reference database)
        # {
        #     gene(str): pLI(float)
        # }

        self.pli_data = {}
        script_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(script_dir, 'data/ExACpLI_values.txt')) as f:
            f.readline()
            for line in f.readlines():
                self.pli_data[line.split()[0]] = float(line.split()[1])


    def annotate(self, input_data):
        # function called iterativly for each row in input_vcf, presented as `input_data`(dict)
        # `input data` example
        # {
        #     'uid': 1, 
        #     'chrom': 'chr19', 
        #     'pos': 11100236, 
        #     'ref_base': 'C', 
        #     'alt_base': 'T', 
        #     'note': None, 
        #     'coding': 'Y', 
        #     'hugo': 'LDLR', 
        #     'transcript': 'ENST00000558518.6', 
        #     'so': 'SYN', 
        #     'cchange': 'c.81C>T', 
        #     'achange': 'p.Cys27=', 
        #     'all_mappings': '{"LDLR": [["P01130", "p.Cys27=", "SYN", "ENST00000455727.6", "c.81C>T"], ["P01130", "p.Cys27=", "SYN", "ENST00000535915.5", "c.81C>T"], ["P01130", "p.Cys27=", "SYN", "ENST00000545707.5", "c.81C>T"], ["", "p.Cys27=", "SYN", "ENST00000557933.5", "c.81C>T"], ["P01130", "p.Cys27=", "SYN", "ENST00000558013.5", "c.81C>T"], ["P01130", "p.Cys27=", "SYN", "ENST00000558518.6", "c.81C>T"]]}', 
        #     'mapping_parser': <cravat.inout.AllMappingsParser object at 0x7f875f055a90>
        # }

        gene = input_data['hugo']
        if gene in self.pli_data:
            return {
                'pli': self.pli_data[gene]
            }

        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
