import pandas as pd
import numpy as np

noun_df = pd.read_csv("./ud_en_ewt/data_csv/merged_noun.csv",index_col=0)
noun_df.head()



################################################################## Noun_df ##############################################################################


## n_word starting with a consonant or vowel

h_ls = []
for index, row in noun_df.iterrows():
    if row[0].startswith("h" or "H"):
        h_ls.append(row[0])

h_ls = set(h_ls)
h_ls = list(h_ls)
len(h_ls)  # 288

h_vowel_ls = ["hz","hr","hh","hpl","hca","htp","hmb","hd","h","hnd","honor", "herb", "hour", "heir", "html","hrs","heirs","hours","herbs","honors"]


def vowelConsonant(word):
    ch = word.lower()[0]
    if(ch == 'i' or ch == 'O' or ch == 'o' or ch == 'U' or ch == 'u'
       or word.lower() in h_vowel_ls):
        return "Vowel"
    else:
        return "Consonant"

noun_df["n_firstSound"] = noun_df["n_word"].map(vowelConsonant)

# to try to use a method to transcribe english into ipa 
# import epitran
# epi = epitran.Epitran('eng-Latn')
# vowel=['i','e','ɑ','æ','a','ɛ','o','ɔ','ʊ','u','ʌ','ə','ɪ','ɹ̩','n̩']

# def vowelConsonant(word):
#     if epi.trans_list(word)[0] in vowel:
#         return 'vowel'
#     else:
#         return 'consonant'

# noun_df['n_firstSound'] = noun_df['n_word'].map(vowelConsonant)


## length

def lens(strcol):
    strcol = strcol.replace(" ","").split(",")
    return ", ".join([str(len(a))for a in strcol])


noun_df["n_word_len"] = noun_df["n_word"].map(len)

noun_df = noun_df.fillna("")
noun_df["adj_len"] = noun_df["adj"].map(lens)
noun_df['ncomp_word_len']=noun_df["ncomp"].map(lens)
noun_df['ncomp_lemma_len']=noun_df['ncomp_lemma'].map(lens)
noun_df['nmod_word_len']=noun_df['nmod'].map(lens)
noun_df['nmod_lemma_len']=noun_df["nmod_lemma"].map(lens)

noun_len_df = noun_df[["n_word","n_firstSound","n_word_len","adj","adj_len","ncomp","ncomp_word_len","ncomp_lemma","ncomp_lemma_len",
                        "nmod","nmod_word_len","nmod_lemma","nmod_lemma_len",
                        "n_id","sen_id"]]

noun_len_df.to_csv("./ud_en_ewt/data_csv/en_ewt-ud_noun_len.csv")



## count

## count n_word, n_lemma, det, num
noun_df['n_word'] = noun_df['n_word'].str.lower() 
n_word_count = noun_df["n_word"].value_counts()
n_word_count_1 = n_word_count.to_dict()
del n_word_count_1[""]
noun_df["n_word_count"] = noun_df["n_word"].map(n_word_count_1)

noun_df["n_lemma"] = noun_df["n_lemma"].str.lower() 
n_lemma_count = noun_df["n_lemma"].value_counts()
n_lemma_count_1 = n_lemma_count.to_dict()
del n_lemma_count_1[""]
noun_df["n_lemma_count"] = noun_df["n_lemma"].map(n_lemma_count_1)

noun_df["det"] = noun_df["det"].str.lower() 
det_count = noun_df["det"].value_counts()
det_count_1 = det_count.to_dict()
del det_count_1[""]
noun_df['det_count'] = noun_df['det'].map(det_count_1)

noun_df["num"] = noun_df["num"].astype(str)
noun_df["num"] = noun_df["num"].str.lower() 
num_count = noun_df["num"].value_counts()
num_count_1 = num_count.to_dict()
del num_count_1[""]
noun_df["num_count"] = noun_df["num"].map(num_count_1)

noun_count_one_df = noun_df[["n_word","n_firstSound","n_word_count","n_lemma","n_lemma_count","det","det_count",
                            "num","num_count","n_id","sen_id"]]

noun_count_one_df.to_csv("./ud_en_ewt/data_csv/en_ewt-ud_noun_count_one.csv")


## count adj, ncomp, ncomp_lemma, nmod, nmod_lemma

noun_df = noun_df.fillna("")

def counts(ls):
    counted = list(ls)
    col = []
    for i in counted:
        col.extend(i.replace(" ","").split(","))
    
    counted_dic= dict()
    for w in col:
        if w in counted_dic.keys():
            counted_dic[w] +=1
        else:
            counted_dic[w] =1
    del counted_dic[""]
    counted_df = pd.DataFrame(list(counted_dic.items()),columns=["word","count"])
    return counted_df

adj_count_df = counts(noun_df["adj"])
adj_count_df["type"] = "adj"
ncomp_count_df = counts(noun_df['ncomp'])
ncomp_count_df["type"] = "ncomp"
ncomp_lemma_count_df = counts(noun_df['ncomp_lemma'])
ncomp_lemma_count_df["type"] = "ncomp_lemma"
nmod_count_df = counts(noun_df["nmod"])
nmod_count_df["type"] = "nmod"
nmod_lemma_count_df = counts(noun_df['nmod_lemma'])
nmod_lemma_count_df["type"] = "nmod_lemma"

noun_count_two_df = pd.concat([adj_count_df,ncomp_count_df,ncomp_lemma_count_df,nmod_count_df,nmod_lemma_count_df])

noun_count_two_df.to_csv("./ud_en_ewt/data_csv/en_ewt-ud_noun_count_two.csv")


################################################################ Adj_df #####################################################################
import pandas as pd
adj_df = pd.read_csv("./ud_en_ewt/data_csv/merged_adj.csv",index_col=0)
adj_df.head()

# length
adj_df["adj_word_len"] = adj_df["adj_word"].map(len)
adj_df = adj_df.fillna("")
adj_df["n_word_len"] = adj_df["n_word"].map(len)

# count
adj_count = adj_df["adj_word"].value_counts()
adj_count_1 = adj_count.to_dict()
adj_df["adj_word_count"] = adj_df["adj_word"].map(adj_count_1)

# adj_df = adj_df.replace("", np.nan, regex=True)

noun_word_count = adj_df["n_word"].value_counts()
noun_word_count_1 = noun_word_count.to_dict()
del noun_word_count_1[""]
adj_df["n_word_count"] = adj_df["n_word"].map(noun_word_count_1)

noun_lemma_count = adj_df["n_lemma"].value_counts()
noun_lemma_count_1 = noun_lemma_count.to_dict()
del noun_lemma_count_1[""]
adj_df["n_lemma_count"] = adj_df["n_lemma"].map(noun_lemma_count_1)

# to rearrange columns
adj_df = adj_df[['adj_word', 'adj_word_len', 'adj_word_count', 'adj_lemma', 'adj_comb', 'num_adj','n_word', 'n_word_len', "n_word_count",
                 'n_lemma', 'n_lemma_count', 'adj_id', 'n_id', 'sen_len', 'sen_id']]

adj_df.to_csv("./ud_en_ewt/data_csv/en_ewt-ud_adj.csv")

