import os
import grewpy
from grewpy import Corpus, CorpusDraft
import re

treebank_path="/Users/maria23paz/Downloads/SUD_French-Rhapsodie@rm_mwt"
output_dir="/Users/maria23paz/Documents/Stage/Rhapsodie/CONLLU_mrw"

grewpy.set_config("sud") # ud or basic
corpus = Corpus(treebank_path)
draft_conllu = CorpusDraft(corpus)

dico_id = {}
pattern = re.compile(r'^sent_id')
for i in range (len(draft_conllu)):
    sentence = draft_conllu[i]
#print(sentence)
    meta = sentence.meta

    for key, value in meta.items():
        if pattern.match(key): 
            id_prefijo = value.split('-')[0]
            #print(id_prefijo)
            if id_prefijo not in dico_id:
                dico_id[id_prefijo] = []
            dico_id[id_prefijo].append(sentence)
    
os.makedirs(output_dir, exist_ok=True)


for id_prefijo, trees_list in dico_id.items():
    output_path = os.path.join(output_dir, f"{id_prefijo}.conllu")
    with open(output_path, 'w') as f:
        for tree in trees_list:
            conll_string=tree.to_conll()
            f.write(conll_string + '\n')
    
    
                
        
        
        

    
    