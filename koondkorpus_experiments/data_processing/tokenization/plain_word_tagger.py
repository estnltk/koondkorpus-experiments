from estnltk.taggers import Tagger, TokensTagger, CompoundTokenTagger, WordTagger


class PlainWordTagger(Tagger):
    """This is like EstNLTK WordTagger, but doesn't need any input layers"""

    conf_param = ['tokens_tagger', 'compound_tokens_tagger', 'word_tagger']
    input_layers = []

    def __init__(self, output_layer='words'):
        self.output_layer = output_layer

        self.tokens_tagger = TokensTagger()
        self.compound_tokens_tagger = CompoundTokenTagger()
        self.word_tagger = WordTagger(output_layer=self.output_layer)

    def _make_layer(self, text, layers, status):
        tokens = self.tokens_tagger.make_layer(text=text)
        compound_tokens = self.compound_tokens_tagger.make_layer(text=text, layers={'tokens': tokens})
        words = self.word_tagger.make_layer(text=text,
                                            layers={'tokens': tokens, 'compound_tokens': compound_tokens})
        return words
