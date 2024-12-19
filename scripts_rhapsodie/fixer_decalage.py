import pandas as pd
import grewpy
from grewpy import Corpus, CorpusDraft
import re
import os
import argparse
from dict_decomposiion_dialogues import dico_decomposition



def obtenir_conllu(corpus_dir):
    '''Crée la liste de fichiers conllu et la liste de noms de fichiers pour les exporter après''' 
    liste_fichiers = []  
    liste_filename = []
    liste_non_ordonnee = os.listdir(corpus_dir)
    liste_ordonne = sorted(liste_non_ordonnee)
    for filename in liste_ordonne:
        if filename == ".DS_Store":
            continue
        fichier_path = os.path.join(corpus_dir, filename)
        try:
            liste_filename.append(filename)
            liste_fichiers.append(fichier_path) 
        except Exception as error:
            print(f"Oups ! ce fichier ne marche pas {fichier_path}: {error}")
    
    return liste_fichiers, liste_filename

def obtenir_lignes(liste_fichiers):
    '''Pour chaque fichier crée une liste de lignes et ajoute cette liste à une liste générale'''
    toutes_les_lignes = []
    for fichier_conllu in liste_fichiers:
        with open(fichier_conllu, 'r') as fichier:
            lineas = fichier.readlines()
            toutes_les_lignes.append(lineas)
            #print(toutes_les_lignes)
    return toutes_les_lignes

def lignes_repetees(liste_listes):
    '''Si trouve une clé du dictionnaire décomposer_tokens, crée des lignes répétées selon la quantité d'éléments qui se trouvent dans le value '''
    toutes_modifiees = []
    for liste in liste_listes:
        lignes_modifiees =  []
        for ligne in liste:
            lignes_modifiees.append(ligne)
            for key, value in dico_decomposition.items():
                if key in ligne and ligne[0] != "#":
                    longueur_value = len(value) - 1
                    for i in range (longueur_value):
                        lignes_modifiees.append(ligne)
                        #print(lignes_modifiees)
        toutes_modifiees.append(lignes_modifiees)
    #print(toutes_modifiees)
    return toutes_modifiees

def decomposer_mots(liste_listes):
    '''Décompose les mots souhaités et change les relations de dépendence'''
    troisieme_modifiee = False
    quatrieme_modifiee = False
    for liste in liste_listes:
        print(liste)
        for index in range(len(liste) - 1):
            try:
                premiere_actual = liste[index].split("\t")
                deuxieme_line = liste[index + 1].split("\t")
                troisieme_line = liste[index + 2].split("\t")
                quatrieme_line = liste[index + 3].split("\t")
            except IndexError:
                continue  
            
        

            id_actual = premiere_actual[0]
            id_next = deuxieme_line[0]
            
            for key, value in dico_decomposition.items():
                if id_actual == id_next and key in premiere_actual[1]:
                    premiere_actual[1] = value[0]
                    premiere_actual[2] = value[0]
                    deuxieme_line[1] = value[1]
                    deuxieme_line[2] = value[1]
                    deuxieme_line[6] = id_actual
                    deuxieme_line[7] = "flat@dev"

                    if len(value) > 2 and id_actual == troisieme_line[0]:
                        troisieme_line[1] = value[2]
                        troisieme_line[2] = value[2]
                        troisieme_line[6] = id_actual
                        troisieme_line[7] = "flat@dev"
                        troisieme_modifiee = True

                    if len(value) > 3 and id_actual == quatrieme_line[0]:
                        quatrieme_line[1] = value[3]
                        quatrieme_line[2] = value[3]
                        quatrieme_line[6] = id_actual
                        quatrieme_line[7] = "flat@dev"
                        quatrieme_modifiee = True

                    liste[index] = "\t".join(premiere_actual)
                    liste[index + 1] = "\t".join(deuxieme_line)

                    if troisieme_modifiee:
                        liste[index + 2] = "\t".join(troisieme_line)
                        troisieme_modifiee = False  

                    if quatrieme_modifiee:
                        liste[index + 3] = "\t".join(quatrieme_line)
                        quatrieme_modifiee = False  

                    break 
    return liste_listes

def fixer_id (liste_listes):
    '''Met dans le bon ordre les id de chaque tree'''
    dernier_id = 0
    for liste in liste_listes:
        for index, line in enumerate(liste):
            if line.startswith("#"):
                dernier_id = 0
                continue

            partes = line.split("\t")
            primer = partes[0].strip()
            if primer.isdigit():
                dernier_id += 1
                partes[0] = str(dernier_id)
                liste[index] = "\t".join(partes)
    return liste_listes

def exporter_corpus(liste_listes, output_dir, liste_filename): 
    '''Exporte le corpus. Prend comme argument la liste de drafts, la liste de noms des fichiers et le directoire d'output'''            
    os.makedirs(output_dir, exist_ok=True)
    for filename, liste in zip(liste_filename, liste_listes):
            output_path = os.path.join(output_dir, filename)
            
            try:
                with open(output_path, 'w', encoding='utf-8') as file:
                    for linea in liste:
                        file.write(linea)
                print(f"Fichier exporté : {output_path}")
            except Exception as error:
                print(f"Oups ! Erreur lors de l'exportation du fichier: {error}")
                continue
            
def main():
    
    parser = argparse.ArgumentParser(description="Ajoutez les directoires des fichiers conllu")
    parser.add_argument('-c','--dir_conllu', help="Ajoutez le chemin du directoire des fichiers conllu")
    parser.add_argument('-o','--output_dir', help="Ajoutez le chemin du directoire d'output")
    args = parser.parse_args()
    
    liste_fichiers, liste_filename = obtenir_conllu(args.dir_conllu)
    lignes = obtenir_lignes(liste_fichiers)
    lignes_modifiees = lignes_repetees(lignes)
    mots_decomposes = decomposer_mots(lignes_modifiees)
    id_fixes= fixer_id(mots_decomposes)
    
    exporter_corpus(id_fixes, args.output_dir, liste_filename)
    
    
if __name__== "__main__" :
    main() 