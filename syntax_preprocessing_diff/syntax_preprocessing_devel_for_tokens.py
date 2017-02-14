import os
import json
from time import time
import argparse

from estnltk.syntax.syntax_preprocessing import SyntaxPreprocessing
from estnltk import Text
from estnltk.core import PACKAGE_PATH as ESTNLTK_PATH


def yield_tokens_analysis(file):
    """Reads the file created by ... and 
    yields the tuples (token, analysis).
    """
    with open(file, 'r') as f:
        for line in f:
            token, analysis_tuples = json.loads(line.rstrip('\n'))
            analysis = [{'lemma': t[0], 
                         'root': t[1], 
                         'root_tokens': t[2], 
                         'ending': t[3], 
                         'clitic': t[4], 
                         'partofspeech': t[5], 
                         'form': t[6]} for t in analysis_tuples]
            yield token, analysis


def syntax_preprocessing_for_tokens(fs_to_synt_rules_file, subcat_rules_file,
                                    allow_to_remove_all, in_file, out_file):
    pipeline = SyntaxPreprocessing(fs_to_synt=fs_to_synt_rules_file,
                                   subcat=subcat_rules_file,
                                   allow_to_remove_all=allow_to_remove_all)
    with open(out_file, 'w') as out_file:
        t0 = time()
        for i, (token, analysis) in enumerate(yield_tokens_analysis(in_file)):
            text = Text(token)
            text['words'] = [{'text': token, 'start': 0, 'end': len(token), 'analysis': analysis}]
            result = pipeline.process_Text(text)
            print(json.dumps((token, result), ensure_ascii=False), file=out_file)

            if i%200 == 0:
                print('.', end='', flush=True)
                if i%10000 == 0 and i:
                    print(i, (time()-t0)/i, token)

if __name__ == '__main__':
    fs_to_synt_rules_file = os.path.join(ESTNLTK_PATH, 'syntax/files/tmorftrtabel.txt')
    subcat_rules_file = os.path.join(ESTNLTK_PATH, 'syntax/files/abileksikon06utf.lx')
    allow_to_remove_all = False
    parser = argparse.ArgumentParser(
        description="Run syntax preprocessing on all morphologically analyzed tokens.")
    parser.add_argument('in_f', type=str, help='Input file.')
    parser.add_argument('out_f', type=str, help='Output file.')
    args = parser.parse_args()
    syntax_preprocessing_for_tokens(fs_to_synt_rules_file, subcat_rules_file, 
                                    allow_to_remove_all,
                                    args.in_f, args.out_f)