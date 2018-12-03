# Tokenization

Various pipelines for re-tokenizing koondkorpus.
## Layers
* **v16_1_words:**
  Words obtained by EstNLTK 1.6 NLP pipeline (commit nr)

  **Script:** [create_v16_1_words.py](create_v16_1_words.py) runs `PlainWordTagger` on koondkorpus in EstNLTK PostgreSQL collection.

  **Tagger:** [`PlainWordTagger`](plain_word_tagger.py) tags EstNLTK Text object with words layer ignoring all existing layers and using 
only raw text as an input.

## Notebooks

* [tokenization.ipynb](tokenization.ipynb) notebook contains an experiment of extracting all words from the koondkorpus.
