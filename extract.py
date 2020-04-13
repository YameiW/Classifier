import pyconll
import pandas as pd


def extractN(input_file):
    trial_doc = pyconll.load_from_file(input_file)

    noun_ls = []
    for sentence in trial_doc:
        for word in sentence:
            counter = 0
            counter_ncomp = 0
            counter_nmod = 0
            if word.upos == "NOUN":
                noun_dict = {"n_word": word.form, "n_lemma": word.lemma, "n_id": word.id, "det": "",
                             "num": "", "adj": [],"num_adj":"","ncomp": [], "ncomp_lemma": [], "nmod":[],"nmod_lemma":[],
                             "num_ncomp":"", "num_nmod":"",
                             "sen_len": len(sentence), "sen_id": sentence.id}
                for mod_word in sentence:
                    if mod_word.head == word.id:
                        if mod_word.upos == "ADJ":
                            counter +=1
                            noun_dict["adj"].append(mod_word.form)
                            noun_dict['num_adj'] = counter
                        if mod_word.upos == "NUM":
                            noun_dict["num"] = mod_word.form
                        if mod_word.upos == "NOUN":
                            if mod_word.deprel == "compound":
                                counter_ncomp +=1
                                noun_dict["ncomp"].append(mod_word.form)
                                noun_dict["ncomp_lemma"].append(mod_word.lemma)
                                noun_dict['num_ncomp'] = counter_ncomp
                            if mod_word.deprel == "nmod":
                                counter_nmod +=1
                                noun_dict["nmod"].append(mod_word.form)
                                noun_dict['nmod_lemma'].append(mod_word.lemma)
                                noun_dict['num_nmod'] = counter_nmod
                        elif mod_word.upos == "DET":
                            noun_dict["det"] = mod_word.form
                noun_ls.append(noun_dict)
                noun_dict['adj'] = ", ".join(noun_dict['adj'])
                noun_dict['nmod']= ", ".join(noun_dict['nmod'])
                noun_dict['nmod_lemma']= ", ".join(noun_dict['nmod_lemma'])
                noun_dict['ncomp']= ", ".join(noun_dict['ncomp'])
                noun_dict['ncomp_lemma']= ", ".join(noun_dict['ncomp_lemma'])

    df_noun = pd.DataFrame(noun_ls)
    df_noun.to_csv(input_file.replace(".conllu", "_noun.csv"))


def extractAdj(input_file):
    trial_doc = pyconll.load_from_file(input_file)

    adj_ls = []
    for sentence in trial_doc:
        for word in sentence:
            if word.upos == "ADJ":
                counter = 0
                adj_dict = {"adj_word": word.form, "adj_lemma": word.lemma, "adj_id": word.id,
                            "adj_comb": [],"adj_count":"", "n_word": "", "n_lemma": "", "n_id": "", "sen_len": len(sentence), "sen_id": sentence.id}
                for item in sentence:
                    if item.id == word.head and item.upos == "NOUN":
                        adj_dict["n_word"] = item.form
                        adj_dict["n_lemma"] = item.lemma
                        adj_dict["n_id"] = item.id
                    elif item.head == word.head and item.upos == "ADJ":
                        counter +=1
                        adj_dict["adj_comb"].append(item.form)
                        adj_dict['adj_count'] = counter
                adj_ls.append(adj_dict)
                adj_dict['adj_comb']=", ".join(adj_dict['adj_comb'])

    df_adj = pd.DataFrame(adj_ls)
    df_adj.to_csv(input_file.replace(".conllu", "_adj.csv"))




folder = "/home/yamei/pjkt/classifier/ud_en_ewt/data_csv/"
extractN(folder+"en_ewt-ud-dev.conllu")
extractAdj(folder+"en_ewt-ud-dev.conllu")

extractN(folder+"en_ewt-ud-test.conllu")
extractAdj(folder+"en_ewt-ud-test.conllu")

extractN(folder+"en_ewt-ud-train.conllu")
extractAdj(folder+"en_ewt-ud-train.conllu")

