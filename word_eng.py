import pyconll
import pandas as pd

def extractN(input_file):
    trial_doc = pyconll.load_from_file(input_file)

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

    df_noun = pd.DataFrame(noun_ls) 
    df_noun.to_csv("./"+"noun_"+input_file.replace("conllu","csv"))

def extractAdj(input_file):
    trial_doc = pyconll.load_from_file(input_file)

    adj_ls = []
    for sentence in trial_doc:
        for word in sentence:
            if word.upos == "ADJ":  
                adj_dict = {"adj": word.lemma,
                             "sen_id": sentence.id, "word_id": word.id,"noun":"", "noun_id":""}
                for head_word in sentence:
                    if head_word.id == word.head and head_word.upos=="NOUN":
                        adj_dict["noun"]=head_word.lemma
                        adj_dict["noun_id"]=head_word.id
                adj_ls.append(adj_dict)

    df_adj = pd.DataFrame(adj_ls) 
    df_adj.to_csv("./"+"adj_"+input_file.replace("conllu","csv"))


extractN("en_ewt-ud-dev.conllu")
extractAdj("en_ewt-ud-dev.conllu")

extractN("en_ewt-ud-test.conllu")
extractAdj("en_ewt-ud-test.conllu")

extractN("en_ewt-ud-train.conllu")
extractAdj("en_ewt-ud-train.conllu")

############################################################################################
############################################################################################
import pandas as pd

noun_df = pd.read_csv("noun_en_ewt-ud.csv")
noun_df.head()
adj_df = pd.read_csv("adj_en_ewt-ud.csv")
adj_df.head()


### Noun_df

## add n_length to the df
# n_len=[]
# for i in range(len(noun_df)):
#     n_len.append(len(noun_df["n"][i]))
# noun_df["n_len"]=n_len

noun_df["n_len"]=noun_df["n"].map(len)

## count nouns 
noun_count=noun_df["n"].value_counts()
noun_count_1=noun_count.to_dict()
noun_df["n_count"]=noun_df["n"].map(noun_count_1)

## a noun starts with a vowel or a consonant
def vowelConsonant(word):
    ch=word[0]
    if(ch=='A' or ch=='a' or ch=='E' or ch =='e' or ch=='I' 
    or ch=='i' or ch=='O' or ch=='o' or ch=='U' or ch=='u'):
        return "Vowel"
    else:
        return "Consonant"         

noun_df["firstSound"]=noun_df["n"].map(vowelConsonant)
noun_df.head()

## to rearrange columns
noun_df=noun_df[['n','word_id','n_len','n_count','firstSound','adj','det','sen_id']]
noun_df=noun_df.rename(columns={"word_id":"n_id"})
noun_df.head()

noun_df.to_csv("noun_en_ewt-ud_1.csv")

### Adj_df 
## count adjectives 
adj_count=adj_df["adj"].value_counts()
adj_count_1=adj_count.to_dict()
adj_df["adj_count"]=adj_df["adj"].map(adj_count_1)

# to rearrange columns
adj_df.head()
adj_df=adj_df[['adj','word_id','adj_count','noun','noun_id','sen_id']]
adj_df=adj_df.rename(columns={"word_id":"adj_id"})

adj_df.to_csv("adj_en_ewt-ud_1.csv")
