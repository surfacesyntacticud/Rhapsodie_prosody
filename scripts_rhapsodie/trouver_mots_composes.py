import grewpy
import pandas as pd
import grewpy
from grewpy import Corpus, CorpusDraft
import re
import os
import argparse
import pprint
from obtenir_exporter_conllu import obtenir_conllu, exporter_corpus
from pprint import pprint


def trouver_compose(liste_drafts):
    '''Crée un disctionnaire des tokens composés pour sa séparation dans les fichier conllu'''
    dico_decomposition = {}
    
    for draft_conllu in liste_drafts:
        for i in range(len(draft_conllu)):
            sentence = draft_conllu[i]
            features = sentence.features
            meta = sentence.meta
            sent_id = meta['sent_id']
            # print(sent_id)
            # dico_verification = {}
            
            for id, dico in features.items():
                # print(dico)
                dico_copie = dico.copy()
                if '-' in dico_copie['form']:
                    
                    sans_tiret = dico_copie['form'].strip('-')
                    dico['form'] = sans_tiret
                    
                    form_divised = dico_copie['form'].split('-')
                    mot_split = []
                    for token in form_divised:
                        if "'" in token:
                            print(form_divised)
                            sans_apostrophe = token.split("'")
                            mot_split += sans_apostrophe
                        else:
                            mot_split.append(token)
                            
                    # print(form_divised)
                    if dico_copie['form'] not in dico_decomposition.keys():
                        if '' not in mot_split:  
                            dico_decomposition[dico_copie['form']] = [mot for mot in mot_split if mot != '']
                        
                    
            # dico_verification[sent_id] = dico_decomposition
    pprint(f'dico_decomposition = {dico_decomposition}')
    return liste_drafts, dico_decomposition
                
def exporter_dico(dico_decomposition):
    with open("corpus_dico_tiret.py", 'w') as f:
        f.write(str(dico_decomposition)) 

                    
                    
def main():
    liste_conllu, liste_filename = obtenir_conllu("/Users/maria23paz/Documents/Stage/Rhapsodie/conllu_mrw_derniereversion")
    liste_drafts, dico_decomposition = trouver_compose(liste_conllu)
    exporter_dico(dico_decomposition)
    exporter_corpus(liste_drafts, '/Users/maria23paz/Documents/Stage/Rhapsodie/corpus_sanstiret', liste_filename)
   
    
if __name__== "__main__" :
    main() 