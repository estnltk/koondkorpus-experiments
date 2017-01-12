import os
import json
import argparse

from estnltk import Text
from estnltk.tokenizers.sent_tokenizer_for_koond import SentenceTokenizerForKoond

def find_tokens_in_corpora(corpora, tokens_file, sentence_tokenizer=None):
    """ Find all tokens in corpora.
    corpora: list of str
        List of corpora directories.
    tokens_file: str
        Output file name.
    sentence_tokenizer
        Tokenizer for sentences.
    """
    tokens = set()
    for corpus in corpora:
        for file in os.listdir(corpus):
            with open(os.path.join(corpus, file)) as f:
                # seda peaks saama paralleelselt teha
                tok = find_tokens_in_file(f, sentence_tokenizer)
            tokens.update(tok)

    with open(tokens_file, 'w') as f:
        for token in sorted(tokens):
            print(token, file=f)
        print('{} tokens written into {}'.format(len(tokens), tokens_file))
    
def find_tokens_in_file(f, sentence_tokenizer):
    if sentence_tokenizer is None:
        return set(Text(json.load(f)).word_texts)
    return set(Text(json.load(f), sentence_tokenizer=sentence_tokenizer).word_texts)

parser = argparse.ArgumentParser(description='Find tokens of corpora.')
parser.add_argument('corpora', metavar='corpus', type=str, nargs='+',
                    help='directory of corpus')
parser.add_argument('--out', dest='out', type=str,  metavar='outdir', 
                    help='output directory for tokens')
args = parser.parse_args()

for path in args.corpora:
    assert os.path.exists(path), 'directory does not exist: '+path
assert os.path.exists(args.out), 'output directory does not exist.'

find_tokens_in_corpora(args.corpora, os.path.join(args.out, 'tokens new sent tok.txt'), SentenceTokenizerForKoond())
find_tokens_in_corpora(args.corpora, os.path.join(args.out, 'tokens default sent tok.txt'))