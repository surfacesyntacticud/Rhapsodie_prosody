import grewpy
from grewpy import Corpus, CorpusDraft

fichier_conllu = "/CONLLU_final/Rhap_M2003.conllu"


grewpy.set_config("sud")
corpus = Corpus(fichier_conllu)
draft_conllu=CorpusDraft(corpus)

indice_id = 1
for i in range (len(draft_conllu)):
    sentence = draft_conllu[i]
    features = sentence.features
    meta = sentence.meta
    sent_id = meta["sent_id"].split("-")[0]
    nombre_sentid =  meta["sent_id"].split("-")[1]
    premiere_partie = sent_id.split("_")[0]
    deuxieme_partie = sent_id.split("_")[1]
    nouveau_sentid = f"{premiere_partie}-{deuxieme_partie}"
    meta["sent_id"] = f"{sent_id}-{indice_id}"
    
    indice_id += 1
    
conll_string= draft_conllu.to_conll()
fichier = f"/CONLLU_intermediaire/{nouveau_sentid}.conllu"

with open(fichier, 'w') as file:
    file.write(conll_string)