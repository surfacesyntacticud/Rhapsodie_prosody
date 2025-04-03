import pandas as pd
import grewpy
from grewpy import Corpus, CorpusDraft
import re
import os
import argparse
from obtenir_exporter_conllu import obtenir_conllu, exporter_corpus
    

def convetir_millisecondes(liste_drafts):
    '''Change les alignements de secondes à millisecondes'''
    pattern = r'AlignBegin$|AlignEnd$'
    for draft_conllu in liste_drafts:
        for i in range(len(draft_conllu)):
            sentence = draft_conllu[i]
            features = sentence.features
            for id, dico in features.items():
                dico_copie = dico.copy()
                for key, value in dico_copie.items():
                    if re.match(pattern, key):
                        # print(f"valor original {value}")
                        if '.' in value.lower():
                            value_float = float(value)
                            value = int(value_float * 1000)
                            
                            dico[key] = str(value)
                            # print(f"valor cambiado{dico[key]}")
                      
                           
    return liste_drafts

def main():
    
    parser = argparse.ArgumentParser(description="Ajoutez les directoires des fichiers conllu et fichiers tabulaires")
    parser.add_argument('-c','--dir_conllu', help="Ajoutez le chemin du directoire des fichiers conllu")
    parser.add_argument('-o','--output_dir', help="Ajoutez le chemin du directoire d'output")
    args = parser.parse_args()
    
    liste_conllu, liste_filename = obtenir_conllu(args.dir_conllu)
    converti = convetir_millisecondes(liste_conllu)
    exporter_corpus(converti, args.output_dir, liste_filename)
    
    
if __name__== "__main__" :
    main() 