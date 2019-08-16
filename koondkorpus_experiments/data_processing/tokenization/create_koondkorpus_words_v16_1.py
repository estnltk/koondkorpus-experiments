#! /usr/bin/env python

# see readme.md for the description

from estnltk import Text, Layer, Span
from estnltk.storage.postgres.iterators import find_examples
from estnltk.storage import PostgresStorage


storage = PostgresStorage(pgpass_file='~/.pgpass',
                          dbname='estonian-text-corpora',
                          schema='estonian_text_corpora',
                          role='estonian_text_corpora_create')

collection = storage.get_collection('koondkorpus_base')

output_collection = storage.get_collection('koondkorpus_words_v16_1',
                                           meta_fields={'normalized_form': 'str',
                                                        'word': 'str'})

output_collection.create('example sentence for every word in koondkorpus_base__v16_1_words__layer')


iter_word_examples = find_examples(collection=collection,
                                   layer='v16_1_words',
                                   attributes=['text'],
                                   output_layers=['v16_1_words'],
                                   return_text=True,
                                   return_count=False,
                                   progressbar='unicode')

with output_collection.insert() as insert:
    for example, key, span_pos, text in iter_word_examples:
        span = text['v16_1_words'][span_pos]

        sentence = None
        for sentence in text.sentences:
            if sentence.start <= span.start and span.end <= sentence.end:
                break
        assert sentence is not None

        t_new = Text(sentence.enclosing_text)

        layer = Layer(name='target', attributes=['normalized_form'], text_object=t_new)
        span_new = Span(span.start-sentence.start, span.end-sentence.start)
        span_new.normalized_form = span.normalized_form

        layer.add_span(span=span_new)

        t_new['target'] = layer

        insert(t_new, meta_data={'word': span.text, 'normalized_form': span.normalized_form})
