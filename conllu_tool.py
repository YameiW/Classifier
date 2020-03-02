### Use parse() to parse into a list of sentences

from conllu import parse
data="""
# text = The quick brown fox jumps over the lazy dog.
1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
2   quick   quick  ADJ    JJ   Degree=Pos                  4   amod    _   _
3   brown   brown  ADJ    JJ   Degree=Pos                  4   amod    _   _
4   fox     fox    NOUN   NN   Number=Sing                 5   nsubj   _   _
5   jumps   jump   VERB   VBZ  Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin   0   root    _   _
6   over    over   ADP    IN   _                           9   case    _   _
7   the     the    DET    DT   Definite=Def|PronType=Art   9   det     _   _
8   lazy    lazy   ADJ    JJ   Degree=Pos                  9   amod    _   _
9   dog     dog    NOUN   NN   Number=Sing                 5   nmod    _   SpaceAfter=No
10  .       .      PUNCT  .    _                           5   punct   _   _
"""
sentences=parse(data)
sentences

from io import open
from conllu import parse_incr
data_file=open('en_ewt-ud-dev.conllu','r',encoding='utf-8')
for tokenlist in parse_incr(data_file):
    print(tokenlist) 

sentence=sentences[0]               
sentence
# TokenList<The, quick, brown, fox, jumps, over, the, lazy, dog, .>

token=sentence[0]
token
# OrderedDict([('id', 1), ('form', 'The'), ('lemma', 'the'), ('upostag', 'DET'), ('xpostag', 'DT'), ('feats', OrderedDict([('Definite', 'Def'), ('PronType', 'Art')])), ('head', 4), ('deprel', 'det'), ('deps', None), ('misc', None)])

token['form'] 
# 'The'

### New in conllu 2.0: filter() a Tokenlist

sentence=sentences[0]
# TokenList<The, quick, brown, fox, jumps, over, the, lazy, dog, .>

sentence.filter(form='quick') 
# quick

sentence.filter(feats__Degree="Pos")
# TokenList<quick, brown, lazy>

sentence.metadata

### Turn a TokenList back into CoNLL-U
sentence.serialize() # The format is not desirable 

### Turn a Tokenlist into a TokenTree 
sentence.to_tree()

### Use parse_tree() to parse into a list of dependency trees
from conllu import parse_tree
sentences= parse_tree(data)
sentences

from conllu import parse_tree_incr
for tokentree in parse_tree_incr(data_file):
    print(tokentree)

root=sentences[0]
root

root.print_tree()

root.token

children=root.children
children

root.metadata
root.serialize()

### Customizing parsing to handle strange variations of CoNLL-U
from conllu import parse
data="""
# tagset = TAG1|TAG2|TAG3|TAG4
# sentence-123
1   My       TAG1|TAG2
2   custom   TAG3
3   format   TAG4
"""

sentences=parse(data)
sentences[0][0]

sentences=parse(data,fields=["id","form","tag"])
sentences[0][0]

split_func=lambda line, i:line[i].split("|")
sentences=parse(data,fields=["id","form","tag"],field_parsers={"tag":split_func})
sentences[0][0]

sentences[0].metadata

sentences=parse(data,metadata_parsers={"tagset":lambda key,value:(key,value.split("|"))})
sentences[0].metadata

sentences=parse(data,metadata_parsers={"tagset":lambda key,value:(key,value.split("|")),"fall_back":lambda key,value:("sentence-id, key")})
sentences[0].metadata

data = """
# id=1-document_id=36:1047-span=1
1   My       TAG1|TAG2
2   custom   TAG3
3   format   TAG4
"""
sentences=parse(data,metadata_parsers={"_fallback_":lambda key,value:[pair.split("=") for pair in (key+"="+value).split("-")]})
sentences[0].metadata























# 