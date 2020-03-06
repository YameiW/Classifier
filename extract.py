
import pyconll
import pandas as pd


def extractN(input_file):
    trial_doc = pyconll.load_from_file(input_file)

    noun_ls = []
    for sentence in trial_doc:
        for word in sentence:
            if word.upos == "NOUN":
                noun_dict = {"n_word": word.form, "n_lemma": word.lemma, "n_id": word.id, "det": "",
                             "num": "", "adj": "", "mod_n_word": "", "mod_n_lemma": "", "sen_len": len(sentence), "sen_id": sentence.id}
                for mod_word in sentence:
                    if mod_word.head == word.id:
                        if mod_word.upos == "ADJ":
                            noun_dict["adj"] = mod_word.form
                        if mod_word.upos == "NUM":
                            noun_dict["num"] = mod_word.form
                        if mod_word.upos == "NOUN":
                            noun_dict["mod_n_word"] = mod_word.form
                            noun_dict["mod_n_lemma"] = mod_word.lemma
                        elif mod_word.upos == "DET":
                            noun_dict["det"] = mod_word.form
                noun_ls.append(noun_dict)

    df_noun = pd.DataFrame(noun_ls)
    df_noun.to_csv("./"+"noun_"+input_file.replace("conllu", "csv"))


def extractAdj(input_file):
    trial_doc = pyconll.load_from_file(input_file)

    adj_ls = []
    for sentence in trial_doc:
        for word in sentence:
            if word.upos == "ADJ":
                adj_dict = {"adj_word": word.form, "adj_lemma": word.lemma, "adj_id": word.id,
                            "mod_adj": "", "n_word": "", "n_lemma": "", "n_id": "", "sen_len": len(sentence), "sen_id": sentence.id}
                for item in sentence:
                    if item.id == word.head and item.upos == "NOUN":
                        adj_dict["n_word"] = item.form
                        adj_dict["n_lemma"] = item.lemma
                        adj_dict["n_id"] = item.id
                    elif item.head == word.head and item.upos == "ADJ" and item != word:
                        adj_dict["mod_adj"] = item.form
                adj_ls.append(adj_dict)

    df_adj = pd.DataFrame(adj_ls)
    df_adj.to_csv("./"+"adj_"+input_file.replace("conllu", "csv"))


extractN("en_ewt-ud-dev.conllu")
extractAdj("en_ewt-ud-dev.conllu")

extractN("en_ewt-ud-test.conllu")
extractAdj("en_ewt-ud-test.conllu")

extractN("en_ewt-ud-train.conllu")
extractAdj("en_ewt-ud-train.conllu")

