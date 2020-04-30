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
                            li = []
                            unit(word,sentence,li)
                            noun_dict['clf'] = sortli(li)
                        elif mod_word.upos == 'ADJ':
                            noun_dict['adj'].append(mod_word.form)
                        elif mod_word.deprel == 'nmod':
                            li = []
                            unit(word,sentence,li)
                            noun_dict['nmod'] = sortli(li)
                noun_dict["adj"] = ", ".join(noun_dict['adj'])
                noun_ls.append(noun_dict)
    df_noun =pd.DataFrame(noun_ls)
    df_noun.to_csv(input_file.replace(".conllu", "_noun.csv"))


def sortli(li):
    """[summary]
    This funcion sorts a list of pyconll.word objects by word.id
    Arguments:
        li a list of pyconll.word object
    Returns:
        concatenate the sorted word.form into one string
    """
    s1= ""
    d1 = {}
    for w in li:
        d1[int(w.id)]=w.form
    for i in sorted (d1.keys()):
        s1+=d1[i]
    return s1

def unit(word, sentence, outlist):
    """[summary]
    recursively find all modifiers of word in sentence and add result to nmodlist

    Arguments:
        word {[pyconll.word]} 
        sentence {[pyconll.sentence]} 
        nmodlist {[python list]} 
    """
    for mod_word in sentence:
        if mod_word.head == word.id:
            outlist.append(mod_word)
            unit(mod_word, sentence, outlist)


folder = "/home/yamei/pjkt/classifier/Multiclassifier/ud_ch_gsdsimp/data_csv/"
extractN(folder+'zh_gsdsimp-ud.conllu')