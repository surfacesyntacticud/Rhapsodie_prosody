import tgt
import grewpy
from grewpy import Corpus, CorpusDraft
import re 
import os
import argparse

def obtenir_textgrid(textgrid_dir):
    '''Crée la liste de fichiers textgrid'''
    liste_filename = []
    liste_fichiers_textgrid = [] 
    liste_non_ordonnee = os.listdir(textgrid_dir)
    liste_ordonnee = sorted(liste_non_ordonnee)
    for filename in liste_ordonnee:
        if filename == ".DS_Store":
            continue
        liste_filename.append(filename)
        nom_fichier = os.path.join(textgrid_dir, filename)
        liste_fichiers_textgrid.append(nom_fichier)
    #print(liste_fichiers)
    return liste_fichiers_textgrid, liste_filename

def data_textgrid(liste_fichiers_textgrid):
    '''Lit le textgrid'''
    objets_textgrid = []
    for fichier in liste_fichiers_textgrid: 
        textgrid_object = tgt.io.read_textgrid(fichier)
        objets_textgrid.append(textgrid_object)
    
    return objets_textgrid



def exporter_corpus(objects_textgrid, output_dir, liste_filename): 
    '''Exporte le corpus en utf-8'''          
    os.makedirs(output_dir, exist_ok=True)
    for filename, textgrid in zip(liste_filename, objects_textgrid):
            output_path = os.path.join(output_dir, filename)
            
            try:
                 tgt.io.write_to_file(textgrid, output_path, format='short', encoding="utf-8")
                 print( f"Le fichier a été exporté ! {output_path}")
            except Exception as error:
                print(f"Oups ! Erreur lors de l'exportation du fichier: {error}") 

def main():
    
    parser = argparse.ArgumentParser(description="Ajoutez les directoires des fichiers conllu et fichiers tabulaires")
    parser.add_argument('-t','--dir_textgrid', help="Ajoutez le chemin du directoire des fichiers tabulaires")
    parser.add_argument('-o','--output_dir', help="Ajoutez le chemin du directoire d'output")
    args = parser.parse_args()
    
   
    liste_textgrid, liste_filename = obtenir_textgrid(args.dir_textgrid)
    objets_textgrid = data_textgrid(liste_textgrid)
    
    exporter_corpus(objets_textgrid, args.output_dir, liste_filename)
    
    
if __name__== "__main__" :
    main()           