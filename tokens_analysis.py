import json
import argparse

from estnltk.vabamorf import morf

def write_tokens_analysis(in_file, out_file):
    """Reads tokens from the in_file, 
    performs morphological analysis with disambiguation=False and
    writes tokens with morphological analysis to the out_file.
    
    Every line of the out_file has the json encoded form
       token, [(lemma, root, root_tokens, ending, clitic, partofspeech, form), ...]
    for example
        ["Ühtedel", [["üks", "üks", ["üks"], "del", "", "N", "pl ad"], ["üks", "üks", ["üks"], "del", "", "P", "pl ad"]]]
    """
    token_count = 0
    analysis_count = 0
    with open(in_file, 'r') as in_f:
        with open(out_file, 'w') as out_f:
            for token in in_f:
                token = token.rstrip('\n')
                analysis = morf.analyze([token], disambiguate=False)[0]['analysis']
                analysis_short = []
                for a in analysis:
                    a_tuple = (a['lemma'],
                               a['root'], 
                               a['root_tokens'], 
                               a['ending'], 
                               a['clitic'], 
                               a['partofspeech'], 
                               a['form'])
                    if a_tuple not in analysis_short:
                        analysis_short.append(a_tuple)
                    
                print(json.dumps((token, analysis_short), ensure_ascii=False), file=out_f)
                token_count += 1
                analysis_count += len(analysis_short)        
    print('{} tokens with {} analysis written to the file "{}".'.
          format(token_count, analysis_count, out_file))


def yield_tokens_analysis(file):
    """Reads the file created by write_token_analysis and 
    yields the pairs (token, analysis).
    """
    with open(file, 'r') as f:
        for line in f:
            token, morphs = json.loads(line.rstrip('\n'))
            analysis = [{'lemma': a[0], 
                         'root': a[1], 
                         'root_tokens': a[2], 
                         'ending': a[3], 
                         'clitic': a[4], 
                         'partofspeech': a[5], 
                         'form': a[6]} for a in morphs]
            yield token, analysis


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyse all tokens in file.")
    parser.add_argument('in_file', type=str, help='The path of the input file.')
    parser.add_argument('out_file', type=str, help='The path to the output file.')
    args = parser.parse_args()

    write_tokens_analysis(args.in_file, args.out_file)