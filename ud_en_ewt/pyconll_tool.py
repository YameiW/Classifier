### getting started
# https://pyconll.readthedocs.io/en/stable/pyconll/unit/token.html
# Loading CoNLL-U
import pyconll
dev=pyconll.load_from_file("en_ewt-ud-dev.conllu")

count=0

for sentence in dev:
    for word in sentence:
        if word.lemma =="the":
            type(word)
            count +=1

print(count)

