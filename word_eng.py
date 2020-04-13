import pandas as pd
noun_df = pd.read_csv("./data_csv/noun_en_ewt-ud.csv")
noun_df.head()

################################################################## Noun_df ##############################################################################

# length

noun_df["n_word_len"] = noun_df["n_word"].map(len)

noun_df = noun_df.fillna("")

noun_df["adj_len"] = noun_df["adj"].map(len)
noun_df["mod_n_word_len"] = noun_df["mod_n_word"].map(len)
noun_df["mod_n_lemma_len"] = noun_df["mod_n_lemma"].map(len)

# count
n_word_count = noun_df["n_word"].value_counts()
n_word_count_1 = n_word_count.to_dict()
noun_df["n_word_count"] = noun_df["n_word"].map(n_word_count_1)

n_lemma_count = noun_df["n_lemma"].value_counts()
n_lemma_count_1 = n_lemma_count.to_dict()
noun_df["n_lemma_count"] = noun_df["n_lemma"].map(n_lemma_count_1)

det_count = noun_df["det"].value_counts()
det_count_1 = det_count.to_dict()
noun_df['det_count'] = noun_df['det'].map(det_count_1)

num_count = noun_df["num"].value_counts()
num_count_1 = num_count.to_dict()
noun_df["num_count"] = noun_df["num"].map(num_count_1)

import numpy as np
noun_df = noun_df.replace("", np.nan, regex=True)

adj_count = noun_df["adj"].value_counts()
adj_count_1 = adj_count.to_dict()
noun_df["adj_count"] = noun_df["adj"].map(adj_count_1)


mod_noun_word_count = noun_df["mod_n_word"].value_counts()
mod_noun_word_count_1 = mod_noun_word_count.to_dict()
noun_df["mod_n_word_count"] = noun_df["mod_n_word"].map(
    mod_noun_word_count_1)


mod_noun_lemma_count = noun_df["mod_n_lemma"].value_counts()
mod_noun_lemma_count_1 = mod_noun_lemma_count.to_dict()
noun_df["mod_n_lemma_count"] = noun_df["mod_n_lemma"].map(
    mod_noun_lemma_count_1)

# a noun starts with a vowel or a consonant

noun_df["n_lemma"].head()
h_ls = []
for i in range(len(noun_df)):
    if noun_df['n_lemma'][i].startswith("h" or "H"):
        h_ls.append(noun_df["n_lemma"][i])

h_ls = set(h_ls)
h_ls = list(h_ls)
len(h_ls)  # 241

h_vowel_ls = ["hr", "hh", "honor", "herb", "hour", "heir", "html"]

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


# to rearrange columns
noun_df = noun_df[['n_word', 'n_word_len', 'n_word_count', 'n_firstSound', 'n_lemma', 'n_lemma_count', 'det', 'det_count',
                   'num', 'num_count', 'adj', 'adj_len', 'adj_count', 'mod_n_word', 'mod_n_word_len', 'mod_n_word_count',
                   'mod_n_lemma', 'mod_n_lemma_len', 'mod_n_lemma_count', 'n_id', 'sen_len', 'sen_id']]

noun_df.head()

noun_df.to_csv("./data_csv/noun_en_ewt-ud_1.csv")

################################################################ Adj_df #####################################################################
adj_df = pd.read_csv("./data_csv/adj_en_ewt-ud.csv")
adj_df.head()

# length
adj_df["adj_word_len"] = adj_df["adj_word"].map(len)

adj_df = adj_df.fillna("")

adj_df["mod_adj_len"] = adj_df["mod_adj"].map(len)
adj_df["n_word_len"] = adj_df["n_word"].map(len)

# count
adj_count = adj_df["adj_word"].value_counts()
adj_count_1 = adj_count.to_dict()
adj_df["adj_word_count"] = adj_df["adj_word"].map(adj_count_1)

adj_df = adj_df.replace("", np.nan, regex=True)

mod_adj_count = adj_df["mod_adj"].value_counts()
mod_adj_count_1 = mod_adj_count.to_dict()
adj_df["mod_adj_count"] = adj_df["mod_adj"].map(mod_adj_count_1)

noun_word_count = adj_df["n_word"].value_counts()
noun_word_count_1 = noun_word_count.to_dict()
adj_df["n_word_count"] = adj_df["n_word"].map(noun_word_count_1)

noun_lemma_count = adj_df["n_lemma"].value_counts()
noun_lemma_count_1 = noun_lemma_count.to_dict()
adj_df["n_lemma_count"] = adj_df["n_lemma"].map(noun_lemma_count_1)

# to rearrange columns
adj_df = adj_df[['adj_word', 'adj_word_len', 'adj_word_count', 'adj_lemma', 'mod_adj', 'mod_adj_len', 'mod_adj_count', 'n_word', 'n_word_len', "n_word_count",
                 'n_lemma', 'n_lemma_count', 'adj_id', 'n_id', 'sen_len', 'sen_id']]

adj_df.to_csv("./data_csv/adj_en_ewt-ud_1.csv")

