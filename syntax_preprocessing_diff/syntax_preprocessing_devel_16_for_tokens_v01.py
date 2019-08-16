import json
from time import time
import argparse
import os

from estnltk.text import Text
from estnltk.text import Layer
from estnltk.taggers import MorphExtendedTagger
from estnltk.converters.CG3_exporter import export_CG3

from estnltk.core import abs_path

fs_to_synt_rules_file = abs_path('rewriting/syntax_preprocessing/rules_files/tmorftrtabel.txt')
subcat_rules_file = abs_path('rewriting/syntax_preprocessing/rules_files/abileksikon06utf.lx')
allow_to_remove_all = False


def words_sentences(token, analyses):
    """Construct a Text object containing one word, words layer, sentences layer and morph_analysis layer.

    """
    text = Text(token)
    words = Layer('words', text_object=text)
    words.add_annotation((0, len(token)))
    text.add_layer(words)

    sentences = Layer('sentences', text_object=text, enveloping='words')
    base_span = words[0].base_span
    sentences.add_annotation([base_span])
    text.add_layer(sentences)

    morph_attributes = ['lemma', 'root', 'root_tokens', 'ending', 'clitic', 'partofspeech', 'form']
    morph = Layer('morph_analysis', attributes=morph_attributes, text_object=text, parent='words', ambiguous=True)
    for analysis in analyses:
        morph.add_annotation(base_span, **analysis)
    text.add_layer(morph)

    return text


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


def syntax_preprocessing_for_tokens(fs_to_synt_rules_file, subcat_rules_file, allow_to_remove_all, in_file, out_file):
    tagger = MorphExtendedTagger(fs_to_synt_rules_file=fs_to_synt_rules_file,
                                 subcat_rules_file=subcat_rules_file,
                                 allow_to_remove_all=allow_to_remove_all)
    assert not os.path.exists(out_file), 'Output file "' + out_file + '" already exists.'
    with open(out_file, 'w') as out_f:
        t0 = time()
        t1 = t0
        for i, (token, analysis) in enumerate(yield_tokens_analysis(in_file)):
            text = words_sentences(token, analysis)
            tagger.tag(text)

            result = export_CG3(text)
            print(json.dumps((token, result), ensure_ascii=False), file=out_f)

            if i % 200 == 0:
                if i:
                    print('.', end='', flush=True)
                    if i % 10000 == 0:
                        t2 = time()
                        print('{:10,d} tokens, {:.3f} ({:.3f}) ms/token, {}'.format(i, 1000 * (t2 - t0) / i,
                                                                                    1000 * (t2 - t1) / 10000, token))
                        t1 = t2
    print(i + 1, 'lines written to ', out_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="Run syntax preprocessing on all morphologically analyzed tokens.")
    parser.add_argument('in_f', type=str, help='Input file.')
    parser.add_argument('out_f', type=str, help='Output file.')
    args = parser.parse_args()

    syntax_preprocessing_for_tokens(fs_to_synt_rules_file, subcat_rules_file,
                                    allow_to_remove_all,
                                    args.in_f, args.out_f)
