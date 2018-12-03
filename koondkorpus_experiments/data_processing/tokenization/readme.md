# Tokenization

[`PlainWordTagger`](plain_word_tagger.py) tags EstNLTK Text object with words layer ignoring all existing layers and using 
only raw text as an input.

[create_v16_1_words](create_v16_1_words.py) script runs `PlainWordTagger` on koondkorpus in EstNLTK PostgreSQL collection.

[tokenization](tokenization.ipynb) notebook contains an experiment of extracting all words from the koondkorpus.
