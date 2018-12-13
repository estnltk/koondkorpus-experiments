# Tokenization

Various pipelines for re-tokenizing koondkorpus.
## Collection `koondkorpus_base`
### Layers
* **v16_1_words:**
  Words obtained by EstNLTK 1.6 NLP pipeline (commit 47505126d7b7a4339113adfdc64576a10c7b1411)

  **Script:** [create_v16_1_words.py](create_v16_1_words.py) runs `PlainWordTagger` on koondkorpus in EstNLTK PostgreSQL collection.

  **Tagger:** [`PlainWordTagger`](plain_word_tagger.py) tags EstNLTK `Text` object with words layer ignoring all existing layers and using 
only raw text as an input.

## Collection `koondkorpus_words_v16_1`
**Script:** [create_koondkorpus_words_v16_1.py](create_koondkorpus_words_v16_1.py) creates this collection.

For every word in `v16_1_words` layer of `koondkorpus_base` collection there is an element in `koondkorpus_words_v16_1`
collection. This element is a sentence that contains the word with `target` layer that marks the position of the word in
the sentence and has the `normalized_form` attribute. The word text string and the normalized form is also saved as
the collection metadata in the `word` and `normalized_form` columns.

## Notebooks

* [tokenization.ipynb](tokenization.ipynb) notebook contains an experiment of extracting all words from the koondkorpus.
