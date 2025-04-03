import pandas as pd
import grewpy
from grewpy import Corpus, CorpusDraft
import re
import os
import argparse

def obtenir_conllu(corpus_dir): 
    '''Crée la liste de fichiers conllu et la liste de noms de fichiers pour les exporter après'''
    
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