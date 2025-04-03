import pandas as pd
import grewpy
from grewpy import Corpus, CorpusDraft
import re
import os
import argparse
from obtenir_exporter_conllu import obtenir_conllu, exporter_corpus

'''Crée un nouveau sent_id pour chaque arbre en ordre ascendant.
L'objectif est d'éviter les sent_id de type "Rhap_D0001-20bis". 
Celui-ci est stocké dans la variable "old_id" qui s'affichera dans les métadonnées'''
def old_id(liste_drafts):

    for draft_conllu in liste_drafts:
        indice_id = 1
        for i in range (len(draft_conllu)):
            sentence = draft_conllu[i]
            meta = sentence.meta
            old_id = meta['sent_id']
            meta['old_id'] = old_id
            
            sent_id = meta["sent_id"].split("-")[0]
            meta["sent_id"] = f"{sent_id}-{indice_id}"
            
            indice_id += 1
    return liste_drafts


def main():
    corpus_1 = "../corpus_decalage_fix"
    corpus_output = "../corpus_old_bftabular"
    liste_drafts_1, liste_filename_1 = obtenir_conllu(corpus_1)
    
    drafts_oldid= old_id(liste_drafts_1)

    
    exporter_corpus(drafts_oldid, corpus_output, liste_filename_1)

if __name__ == "__main__":
    main()                