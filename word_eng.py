import pandas as pd
import numpy as np

noun_df = pd.read_csv("./ud_en_ewt/data_csv/merged_noun.csv", index_col=0)
noun_df.head()

################################################################## Noun_df ##############################################################################


# n_word starting with a consonant or vowel

h_ls = []
for index, row in noun_df.iterrows():
    if row[0].startswith("h" or "H"):
        h_ls.append(row[0])

h_ls = set(h_ls)
h_ls = list(h_ls)
len(h_ls)  # 288

h_vowel_ls = ["hz", "hr", "hh", "hpl", "hca", "htp", "hmb", "hd", "h", "hnd", "hlep",
              "honor", "herb", "hour", "heir", "html", "hrs", "heirs", "hours", "herbs", "honors"]


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


# length

def lens(strcol):
    strcol = strcol.replace(" ", "").split(",")
    return ", ".join([str(len(a))for a in strcol])


noun_df = noun_df.fillna("")

ls_1 = ["n_word", "adj", "ncomp", "ncomp_lemma", "nmod", "nmod_lemma"]

for item in ls_1:
    noun_df[item+"_len"] = noun_df[item].map(lens)


noun_len_df = noun_df[["n_word", "n_firstSound", "n_word_len", "adj", "adj_len", "ncomp", "ncomp_len", "ncomp_lemma", "ncomp_lemma_len",
                       "nmod", "nmod_len", "nmod_lemma", "nmod_lemma_len",
                       "n_id", "sen_id"]]

noun_len_df.to_csv("./ud_en_ewt/data_csv/en_ewt-ud_noun_len.csv")


# count

# count n_word, n_lemma, det, num

noun_df = noun_df.fillna("")
ls_2 = ["n_word", "n_lemma", "det", "num"]

for item in ls_2:
    if item == "num":
        noun_df[item] = noun_df[item].astype(str)
    noun_df[item] = noun_df[item].str.lower()
    a = noun_df[item].value_counts()
    b = a.to_dict()
    if "" in b.keys():
        del b[""]
    noun_df[item+"_count"] = noun_df[item].map(b)


noun_count_one_df = noun_df[["n_word", "n_firstSound", "n_word_count", "n_lemma", "n_lemma_count", "det", "det_count",
                             "num", "num_count", "n_id", "sen_id"]]

noun_count_one_df.to_csv("./ud_en_ewt/data_csv/en_ewt-ud_noun_count_one.csv")


# count adj, ncomp, ncomp_lemma, nmod, nmod_lemma

noun_df = noun_df.fillna("")


def counts(ls):
    counted = list(ls)
    col = []
    for i in counted:
        col.extend(i.replace(" ", "").split(","))

    counted_dic = dict()
    for w in col:
        if w in counted_dic.keys():
            counted_dic[w] += 1
        else:
            counted_dic[w] = 1
    del counted_dic[""]
    counted_df = pd.DataFrame(
        list(counted_dic.items()), columns=["word", "count"])
    return counted_df


ls_3 = ["adj", "ncomp", "ncomp_lemma", "nmod", "nmod_lemma"]
ls_4 = []

for i, item in enumerate(ls_3):
    i = counts(noun_df[item])
    i["type"] = item
    ls_4.append(i)

noun_count_two_df = pd.concat(ls_4)
noun_count_two_df.to_csv("./ud_en_ewt/data_csv/en_ewt-ud_noun_count_two.csv")


################################################################ Adj_df #####################################################################
adj_df = pd.read_csv("./ud_en_ewt/data_csv/merged_adj.csv", index_col=0)
adj_df.head()

# length
adj_df = adj_df.fillna("")

ls_5 = ["adj_word", "n_word"]

for item in ls_5:
    adj_df[item+"_len"] = adj_df[item].map(len)


# count

ls_6 = ["adj_word", "n_word", "n_lemma"]

for item in ls_6:
    a = adj_df[item].value_counts()
    b = a.to_dict()
    if "" in b.keys():
        del b[""]
    adj_df[item+"_count"] = adj_df[item].map(b)


adj_df = adj_df[['adj_word', 'adj_word_len', 'adj_word_count', 'adj_lemma', 'adj_comb', 'num_adj', 'n_word', 'n_word_len', "n_word_count",
                 'n_lemma', 'n_lemma_count', 'adj_id', 'n_id', 'sen_len', 'sen_id']]

adj_df.to_csv("./ud_en_ewt/data_csv/en_ewt-ud_adj_.csv")
