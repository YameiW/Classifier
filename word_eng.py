import pyconll
import pandas as pd

def extractN(input_file):
    trial_doc = pyconll.load_from_file(input_file)

    noun_ls = []
    for sentence in trial_doc:
        for word in sentence:
            if word.upos == "NOUN":
                noun_dict = {"n_word": word.form, "n_lemma": word.lemma, "n_id": word.id, "det": "",
                             "num": "", "adj": "", "mod_noun_word": "", "mod_noun_lemma":"","sen_len": len(sentence), "sen_id": sentence.id}
                for mod_word in sentence:
                    if mod_word.head == word.id:
                        if mod_word.upos == "ADJ":
                            noun_dict["adj"] = mod_word.form
                        if mod_word.upos == "NUM":
                            noun_dict["num"] = mod_word.form
                        if mod_word.upos == "NOUN":
                            noun_dict["mod_noun_word"] = mod_word.form
                            noun_dict["mod_noun_lemma"] = mod_word.lemma
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
                adj_dict = {"adj_word":word.form, "adj_lemma": word.lemma, "adj_id": word.id, 
                            "mod_adj":"","noun_word": "", "noun_lemma":"", "noun_id": "", "sen_len": len(sentence), "sen_id": sentence.id}
                for item in sentence:
                    if item.id == word.head and item.upos == "NOUN":
                        adj_dict["noun_word"] = item.form
                        adj_dict["noun_lemma"] = item.lemma
                        adj_dict["noun_id"] = item.id
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

#########################################################################################################################################################
#########################################################################################################################################################
import pandas as pd

noun_df = pd.read_csv("noun_en_ewt-ud.csv")
noun_df.head()
adj_df = pd.read_csv("adj_en_ewt-ud.csv")
adj_df.head()

################################################################## Noun_df ##############################################################################

## length 

noun_df["n_word_len"] = noun_df["n_word"].map(len)

noun_df["adj"] = noun_df["adj"].fillna("")
noun_df["adj_len"] = noun_df["adj"].map(len) 

noun_df["mod_noun_word"] = noun_df["mod_noun_word"].fillna("")
noun_df["mod_noun_word_len"] = noun_df["mod_noun_word"].map(len) 

noun_df["mod_noun_lemma"] = noun_df["mod_noun_lemma"].fillna("")
noun_df["mod_noun_lemma_len"] = noun_df["mod_noun_lemma"].map(len) 

## count 
n_word_count=noun_df["n_word"].value_counts()
n_word_count_1=n_word_count.to_dict()
noun_df["n_word_count"]=noun_df["n_word"].map(n_word_count_1)

n_lemma_count=noun_df["n_lemma"].value_counts()
n_lemma_count_1=n_lemma_count.to_dict()
noun_df["n_lemma_count"]=noun_df["n_lemma"].map(n_lemma_count_1)

num_count=noun_df["num"].value_counts()
num_count_1=num_count.to_dict()
noun_df["num_count"]=noun_df["num"].map(num_count_1)

adj_count=noun_df["adj"].value_counts()
adj_count_1=adj_count.to_dict()
noun_df["adj_count"]=noun_df["adj"].map(adj_count_1)

mod_noun_word_count=noun_df["mod_noun_word"].value_counts()
mod_noun_word_count_1=mod_noun_word_count.to_dict()
noun_df["mod_noun_word_count"]=noun_df["mod_noun_word"].map(mod_noun_word_count_1)

mod_noun_lemma_count=noun_df["mod_noun_lemma"].value_counts()
mod_noun_lemma_count_1=mod_noun_lemma_count.to_dict()
noun_df["mod_noun_word_count"]=noun_df["mod_noun_lemma"].map(mod_noun_lemma_count_1)

## a noun starts with a vowel or a consonant
## need to work on this more stopped here 3/4/20
def vowelConsonant(word):
    ch=word[0]
    if(ch=='A' or ch=='a' or ch=='E' or ch =='e' or ch=='I' 
    or ch=='i' or ch=='O' or ch=='o' or ch=='U' or ch=='u'):
        return "Vowel"
    else:
        return "Consonant"         

noun_df["noun_firstSound"]=noun_df["n_word"].map(vowelConsonant)


# to rearrange columns
# noun_df=noun_df[['n','word_id','n_len','n_count','firstSound','adj','det','sen_id']]
# noun_df=noun_df.rename(columns={"word_id":"n_id"})
# noun_df.head()

# noun_df.to_csv("noun_en_ewt-ud_1.csv")

################################################################ Adj_df #####################################################################
## count adjectives 
adj_count=adj_df["adj"].value_counts()
adj_count_1=adj_count.to_dict()
adj_df["adj_count"]=adj_df["adj"].map(adj_count_1)

# to rearrange columns
adj_df.head()
adj_df=adj_df[['adj','word_id','adj_count','noun','noun_id','sen_id']]
adj_df=adj_df.rename(columns={"word_id":"adj_id"})

adj_df.to_csv("adj_en_ewt-ud_1.csv")
