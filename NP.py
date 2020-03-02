import pyconll
import pandas as pd

input_file = "en_ewt-ud-dev.conllu"
trial_doc = pyconll.load_from_file(input_file)


## get the sentence_id, word_id, word_lemma
noun_ls = []
for sentence in trial_doc:
    for word in sentence:
        if word.upos == "NOUN":  
            noun_dict = {"n": word.lemma,
                         "sen_id": sentence.id, "word_id": word.id,"adj":"", "det":""}
            for mod_word in sentence:
                if mod_word.head == word.id:
                    if mod_word.upos == "ADJ":
                        noun_dict["adj"] = mod_word.lemma
                    elif mod_word.upos == "DET":
                        noun_dict["det"] = mod_word.lemma
            noun_ls.append(noun_dict)

df = pd.DataFrame(noun_ls) 
df.to_csv("./"+input_file.replace("conllu","csv"))