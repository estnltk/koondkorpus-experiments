from regex import search
import pandas
import argparse
from tokens_analysis import yield_tokens_analysis

_pronConversions = ( ("emb\+.*",             ("det",)),
                     ("enda\+.*",            ("pos", "refl")),
                     ("enese\+.*",           ("pos", "refl")),
                     ("eikeegi.*",           ("indef",)),
                     ("eimiski.*",           ("indef",)),
                     ("emb-kumb.*",          ("det",)),
                     ("esimene.*",           ("dem",)),
                     ("iga\+.*",             ("det",)),
                     ("iga_sugune.*",        ("indef",)),
                     ("iga_.ks\+.*",         ("det",)),
                     ("ise\+.*",             ("pos", "det", "refl")),
                     ("ise_enese.*",         ("refl",)),
                     ("ise_sugune.*",        ("dem",)),
                     ("keegi.*",             ("indef",)),
                     ("kes.*",               ("inter rel",)),
                     ("kumb\+.*",            ("rel",)),
                     ("kumbki.*",            ("det",)),
                     ("kõik.*",              ("det",)),
                     ("k.ik.*",              ("det",)),
                     ("meie_sugune.*",       ("dem",)),
                     ("meie_taoline.*",      ("dem",)),
                     ("mihuke\+.*",          ("inter rel",)),
                     ("mihukene\+.*",        ("inter rel",)),
                     ("mille_taoline.*",     ("dem",)),
                     ("milli=?ne.*",         ("rel",)),
                     ("mina\+.*",            ("pers ps1",)),
                     (" ma\+.*",             ("pers ps1",)),
                     ("mina=?kene\+.*",      ("dem",)),
                     ("mina=?ke\+.*",        ("dem",)),
                     ("mingi\+.*",           ("indef",)),
                     ("mingi_sugune.*",      ("indef",)),
                     ("minu_sugune.*",       ("dem",)),
                     ("minu_taoline.*",      ("dem",)),
                     ("miski.*",             ("indef",)),
                     ("mis\+.*",             ("inter rel",)),
                     ("mis_sugune.*",        ("inter rel",)),
                     ("miski\+.*",           ("inter rel",)),
                     ("miski_sugune.*",      ("inter rel",)),
                     ("misu=?ke(ne)?\+.*",   ("dem",)),
                     ("mitme_sugune.*",      ("indef",)),
                     ("mitme_taoline.*",     ("indef",)),
                     ("mitmendik\+.*",       ("inter rel",)),
                     ("mitmes\+.*",          ("inter rel", "indef")),
                     ("mi=?tu.*",            ("indef",)),
                     ("miuke(ne)?\+.*",      ("inter rel",)),
                     ("muist\+.*",           ("indef",)),
                     ("muu.*",               ("indef",)),
                     ("m.lema.*",            ("det",)),
                     ("m.ne_sugune\+.*",     ("indef",)),
                     ("m.ni\+.*",            ("indef",)),
                     ("m.ningane\+.*",       ("indef",)),
                     ("m.ningas.*",          ("indef",)),
                     ("m.herdune\+.*",       ("indef", "rel")),
                     ("määntne\+.*",         ("dem",)),
                     ("na_sugune.*",         ("dem",)),
                     ("nende_sugune.*",      ("dem",)),
                     ("nende_taoline.*",     ("dem",)),
                     ("nihuke(ne)?\+.*",     ("dem",)),
                     ("nii_mi=?tu\+.*",      ("indef", "inter rel")),
                     ("nii_sugune.*",        ("dem",)),
                     ("niisama_sugune.*",    ("dem",)),
                     ("nii?su=?ke(ne)?\+.*", ("dem",)),
                     ("niuke(ne)?\+.*",      ("dem",)),
                     ("oma\+.*",             ("pos", "det", "refl")),
                     ("oma_enese\+.*",       ("pos",)),
                     ("oma_sugune\+.*",      ("dem",)),
                     ("oma_taoline\+.*",     ("dem",)),
                     ("palju.*",             ("indef",)),
                     ("sama\+.*",            ("dem",)),
                     ("sama_sugune\+.*",     ("dem",)),
                     ("sama_taoline\+.*",    ("dem",)),
                     ("samune\+.*",          ("dem",)),
                     ("see\+.*",             ("dem",)),
                     ("see_sama\+.*",        ("dem",)),
                     ("see_sam[au]ne\+.*",   ("dem",)),
                     ("see_sinane\+.*",      ("dem",)),
                     ("see_sugune\+.*",      ("dem",)),
                     ("selle_taoline\+.*",   ("dem",)),
                     ("selli=?ne\+.*",       ("dem",)),
                     ("setu\+.*",            ("indef",)),
                     ("setmes\+.*",          ("indef",)),
                     ("sihuke\+.*",          ("dem",)),
                     ("sina\+.*",            ("pers ps2",)),
                     (" sa\+.*",             ("pers ps2",)),
                     ("sinu_sugune\+.*",     ("dem",)),
                     ("sinu_taoline\+.*",    ("dem",)),
                     ("siuke(ne)?\+.*",      ("dem",)),
                     ("säherdune\+.*",       ("dem",)),
                     ("s.herdune\+.*",       ("dem",)),
                     ("säärane\+.*",         ("dem",)),
                     ("s..rane\+.*",         ("dem",)),
                     ("taoline\+.*",         ("dem",)),
                     ("teie_sugune\+.*",     ("dem",)),
                     ("teie_taoline\+.*",    ("dem",)),
                     ("teine\+.*",           ("dem",)),
                     ("teine_teise\+.*",     ("rec",)),
                     ("teist?_sugune\+.*",   ("dem",)),
                     ("tema\+.*",            ("pers ps3",)),
                     (" ta\+.*",             ("pers ps3",)),
                     ("temake(ne)?\+.*",     ("pers ps3",)),
                     ("tema_sugune\+.*",     ("dem",)),
                     ("tema_taoline\+.*",    ("dem",)),
                     ("too\+.*",             ("dem",)),
                     ("too_sama\+.*",        ("dem",)),
                     ("üks.*",               ("dem", "indef")),
                     (".ks.*",               ("dem", "indef")),
                     ("ükski.*",             ("dem", "indef")),
                     (".kski.*",             ("dem", "indef")),
                     ("üks_teise.*",         ("rec", "indef")),
                     (".ks_teise.*",         ("rec",))
)


def extract_pronouns(in_f, out_f):

    token_lemma_rootec = []
    #in_f = '../corpora/analysis results/analyzed.json'
    #out_f = 'results/pronoun_tagger/detected_pronouns_01.csv'
    for token, analysis in yield_tokens_analysis(in_f):
        for a in analysis:
            if a['partofspeech'] == 'P':
                token_lemma_rootec.append((token, a['lemma'], 
                                        ''.join((a['root'], '+', a['ending'], a['clitic']))))
                if len(token_lemma_rootec) > 1 and token_lemma_rootec[-2] == token_lemma_rootec[-1]:
                    del token_lemma_rootec[-1]
    
    token_lemma_type = []
    for token, lemma, root_ec in token_lemma_rootec:
        match = False
        for pattern, pronoun_type in _pronConversions:
            if search(pattern, root_ec):
                match = True
                token_lemma_type.append({'token': token, 'lemma': lemma, 'pronoun_type': pronoun_type})
                break
        if not match:
            token_lemma_type.append({'token': token, 'lemma': lemma, 'pronoun_type': None})
    
    df = pandas.DataFrame.from_records(token_lemma_type, columns=['token', 'lemma', 'pronoun_type'])
    df.to_csv(out_f, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract all pronouns from file of  analyzed tokens.")
    parser.add_argument('in_f', type=str, help='Input file.')
    parser.add_argument('out_f', type=str, help='Output file.')
    args = parser.parse_args()

    extract_pronouns(args.in_f, args.out_f)