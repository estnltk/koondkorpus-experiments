from estnltk import syllabify_words
raw = [i.strip().lower() for i in open('poolitused.txt').readlines() if i.strip()]
clean = [i.replace('-', '') for i in raw]
syls = ['-'.join([j['syllable'] for j in i]) for i in syllabify_words(clean)]
pairs = list(zip(raw, syls))
correct = len([1 for a,b in pairs if a == b])
wrong = len([1 for a,b in pairs if a != b])
print('vabamorfi mõttes oli poolitused.txt failis õigeid silbitusi', correct)
print('ja valesid', wrong)
open('wrong.csv', 'w+').writelines(['{}, {}\n'.format(a,b) for a,b in [('original', 'vabamorf')] + pairs if a != b])
open('correct.csv', 'w+').writelines(['{}, {}\n'.format(a,b) for a,b in [('original', 'vabamorf')] +  pairs if a == b])



