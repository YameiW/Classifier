import pyconll
import pandas as pd

def extractN(input_file):
    trial_doc = pyconll.load_from_file(input_file)

    noun_ls = []
    for sentence in trial_doc:
        for word in sentence:
            if word.upos == "NOUN":
                noun_dict = {'n_word':word.form, 'n_id':word.id, 
                'n_type':word.deprel,'det':'','num':'','clf':[],'adj':[],
                'nmod':[],'sen_len':len(sentence),'sen_id':sentence.id}
                for mod_word in sentence:
                    if mod_word.head == word.id:
                        if mod_word.upos == 'DET':
                            noun_dict['det'] = mod_word.form
                        elif mod_word.upos == 'NUM':
                            noun_dict['num'] = mod_word.form
                        elif mod_word.deprel == 'clf':
                            for mod_two in sentence:
                                if mod_two.head == mod_word.id:
                                    noun_dict['clf'].append(mod_two.form)
                            noun_dict['clf'].append(mod_word.form)
                        elif mod_word.upos == 'ADJ':
                            noun_dict['adj'].append(mod_word.form)
                        elif mod_word.deprel == 'nmod':
                            for mod_two in sentence:
                                if mod_two.head == mod_word.id:
                                   noun_dict['nmod'].append(mod_two.form)
                            noun_dict['nmod'].append(mod_word.form)

                noun_ls.append(noun_dict)
            
                
    df_noun =pd.DataFrame(noun_ls)
    df_noun.to_csv(input_file.replace(".conllu", "_noun.csv"))


folder = "/home/yamei/pjkt/classifier/ud_ch_gsdsimp/data_csv/"
extractN(folder+'zh_gsdsimp-ud.conllu')