import grewpy
import pandas as pd
import grewpy
from grewpy import Corpus, CorpusDraft
import re
import os
import argparse
import pprint

def obtenir_conllu(corpus_dir):  
    liste_fichiers = []  
    liste_filename = []
    liste_non_ordonnee = os.listdir(corpus_dir)
    liste_ordonne = sorted(liste_non_ordonnee)
    for filename in liste_ordonne:
        if filename == ".DS_Store":
            continue
        treebank_path = os.path.join(corpus_dir, filename)
        liste_filename.append(filename)
        
        try:
            grewpy.set_config("sud")
            corpus = Corpus(treebank_path)
            draft = CorpusDraft(corpus)
            liste_fichiers.append(draft) 
        except Exception as error:
            print(f"Oups ! ce fichier ne marche pas {treebank_path}: {error}")
    #print(liste_filename)
    return liste_fichiers, liste_filename

def trouver_compose(liste_drafts):
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
                    # print(form_divised)
                    if dico_copie['form'] not in dico_decomposition.keys():
                        if '' not in form_divised:  
                            dico_decomposition[dico_copie['form']] = [mot for mot in form_divised if mot != '']
                        
                    
            # dico_verification[sent_id] = dico_decomposition
    print(f'dico_decomposition = {dico_decomposition}')
    return liste_drafts, dico_decomposition
                
def nettoyer_dico(dico_decomposition):
    liste_interdites = ["c'est-à-dire", ]
    pass

def exporter_corpus(liste_drafts, output_dir, liste_filename): 
    '''Exporte le corpus. Prend comme argument la liste de drafts, la liste de noms des fichiers et le directoire d'output'''          
    os.makedirs(output_dir, exist_ok=True)
    for filename, draft in zip(liste_filename, liste_drafts):
            output_path = os.path.join(output_dir, filename)
            
            conll_string=draft.to_conll()
            try:
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(conll_string)
                print(f"Fichier exporté : {output_path}")
            except Exception as error:
                print(f"Oups ! Erreur lors de l'exportation du fichier: {error}")
                    
                    
def main():
    liste_conllu, liste_filename = obtenir_conllu("/Rhapsodie/Dialogues_mrw")
    liste_drafts, dico_decomposition = trouver_compose(liste_conllu)
    exporter_corpus(liste_drafts, '/Rhapsodie/Dialogues_sanstiret', liste_filename)
   
    
if __name__== "__main__" :
    main() 