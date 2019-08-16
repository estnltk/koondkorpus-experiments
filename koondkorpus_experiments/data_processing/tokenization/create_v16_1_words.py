# crate EstNLTK 1.6 words layer on koondkorpus_base collection in 'estonian_text_corpora' schema
# in 'estonian-text-corpora' database

from estnltk.storage import PostgresStorage
from koondkorpus_experiments.data_processing.tokenization.plain_word_tagger import PlainWordTagger


storage = PostgresStorage(pgpass_file='~/.pgpass',
                          dbname='estonian-text-corpora',
                          schema='estonian_text_corpora',
                          role='estonian_text_corpora_create')

collection = storage.get_collection('koondkorpus_base')

tagger = PlainWordTagger(output_layer='v16_1_words')

collection.create_layer(tagger=tagger, progressbar='unicode')
