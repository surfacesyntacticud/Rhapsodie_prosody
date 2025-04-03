import pandas as pd
import grewpy
from grewpy import Corpus, CorpusDraft
import re
import os
import argparse
from dico_dialogues_conllu_textgrid import dictionnaires
from transformation_rhapsodie import dico_reponse, lista_transformation, dico_contracte
from obtenir_exporter_conllu import obtenir_conllu, exporter_corpus
from itertools import pairwise

def obtenir_tabular(tabular_dir):
    '''Crée la liste de fichiers tabulaires'''
    liste_fichiers = [] 
    liste_non_ordonnee = os.listdir(tabular_dir)
    liste_ordonnee = sorted(liste_non_ordonnee)
    for filename in liste_ordonnee:
        if filename == ".DS_Store":
            continue
        nom_fichier = os.path.join(tabular_dir, filename)
        liste_fichiers.append(nom_fichier)
    #print(liste_fichiers)
    return liste_fichiers
                

def obtenir_data_tabular(liste_tabular):
    '''Extrait des listes issues des colonnes des fichiers tabulaires. Pour chaque fichier crée une liste de tuples 
    contenant le id du tree, la forme du token, les annotations prosodiques et les informations macrosyntaxiques'''
    liste_tuples = []
    for fichier_micro_macro in liste_tabular:
        df_tabular = pd.read_csv(fichier_micro_macro, delimiter='\t')
        liste_df_tabular = df_tabular["Token"]
        tokens_tabular =[str(token) for token in liste_df_tabular]
        tmin = df_tabular["Tmin"]
        tmax = df_tabular["Tmax"]
        tree_id = df_tabular["Tree_ID"]
        groupe_type = df_tabular["Group_type"]
        proeminence_initial = df_tabular["Prominence_initial"]
        proeminence_finale = df_tabular["Prominence_final"]
        hesitation = df_tabular["Hesitation"]
        nucleus = df_tabular["Nucleus"]
        prenucleus = df_tabular["Prenucleus"]
        gov_nucleus = df_tabular["Gov_nucleus"]
        innucleus = df_tabular["Innucleus"]
        gov_postnucleus = df_tabular["Gov_postnucleus"]
        iu_parenthesis = df_tabular["IU_parenthesis"]
        iu_graft = df_tabular["IU_graft"]
        iu_embedded = df_tabular["IU_embedded"]
        associated_nucleus = df_tabular["Associated_nucleus"]
        intro_iu = df_tabular["Intro_IU"]
        layer = df_tabular["Layer"]
        para = df_tabular["Type_para"]
        inherited = df_tabular["Type_inherited"]
        iu = df_tabular['IU']
        gov_innucleus = df_tabular['Gov_innucleus']
        period = df_tabular['Period']
        period_tone = df_tabular['Period_tone']
        package = df_tabular['Package']
        package_type = df_tabular['Package_type']
        package_tone = df_tabular['Package_tone']
        group = df_tabular['Group']
        group_tone = df_tabular['Group_tone']
        foot = df_tabular['Foot']
        foot_type = df_tabular['Foot_type']
        foot_tone = df_tabular['Foot_tone']
        pause = df_tabular['Pause_length']
        
        
    
        for i, token in enumerate(tokens_tabular):
            for key, value in dico_contracte.items():
                if token == key:
                    tokens_tabular[i] = value
                    
        tuples = list(zip(tree_id,tokens_tabular, tmin, tmax, groupe_type, proeminence_initial, proeminence_finale, hesitation,  
                          nucleus, prenucleus, gov_nucleus, innucleus, gov_postnucleus, iu_parenthesis, iu_graft, iu_embedded, associated_nucleus, intro_iu, layer, para, inherited,
                          iu, gov_innucleus, period, period_tone, package, package_type, package_tone, group, 
                          group_tone, foot, foot_type, foot_tone, pause))
        liste_tuples.append(tuples)

    return liste_tuples

def tupla_tabular(liste_tuples):
    '''Crée une liste de listes de tuples ayant seulement les tokens souhaités'''
    liste_tuples_propres = []
    
    for tuples in liste_tuples:
        trois_ensemble_propre = []
        for element in tuples:
            if element[1] not in lista_transformation:
                trois_ensemble_propre.append(element)
        liste_tuples_propres.append(trois_ensemble_propre)
    
    return liste_tuples_propres


def creation_alignement(liste_drafts, liste_tuples, liste_filename):
    '''Ajoute les informations du fichier tabulaire au conllu'''
    # print(liste_drafts)
    # print(liste_tuples)
    # print(liste_filename)
    for nom_fichier, dico_correspondance in dictionnaires.items():
        # print(nom_fichier)
        # print("----")
        # print(dico_correspondance)
        for draft_conllu, filename, sublist in zip(liste_drafts, liste_filename, liste_tuples):
            tuples_deja_faites = set()
            real_filename = filename.split("_")[1].split(".")[0]
            if nom_fichier == real_filename:
                print(f" Traitement de nom_dico = {nom_fichier}--nom_conllu = {real_filename}")
                for i in range(len(draft_conllu)):
                    sentence = draft_conllu[i]
                    features = sentence.features
                    meta = sentence.meta
                    sent_id = meta["sent_id"]
                    tree_id = float(sent_id.split('-')[1])
                    
                        # print(f"{nom_fichier}, {nom_file}")
                    for id_conll, id_tabulaire in dico_correspondance.items():
                        if tree_id == float(id_conll):
                            # print(f"trees_id{tree_id}, {id_conll}")
                            if id_tabulaire == "no_prosodic":
                                meta['prosody'] = "no"
                            else:
                                meta['prosody'] = "yes"
                            
                            for dico in features.values():
                                if dico.get('upos') == 'PUNCT' or dico.get('form') == "__0__":
                                    continue
                                if id_tabulaire != "no_prosodic":
                                    if isinstance(id_tabulaire, list):
                                        tuplas_relevantes = [tupla for tupla in sublist if int(tupla[0]) in id_tabulaire]
                                    # print(tuplas_relevantes)
                                    for tupla in tuplas_relevantes:
                                        if tupla not in tuples_deja_faites:
                                            if dico.get('form') == str(tupla[1]):               
                                                                    dico['AlignBegin'] = str(tupla[2])
                                                                    dico['AlignEnd'] = str(tupla[3])
                                                                    dico['RhythmGroup'] = str(tupla[4])
                                                                    dico['ProminenceInitial'] = str(tupla[5])
                                                                    dico['ProminenceFinal'] = str(tupla[6])
                                                                    dico['Hesitation'] = str(tupla[7])
                                                                    dico['Nucleus'] = str(tupla[8])
                                                                    dico['Prenucleus'] = str(tupla[9])
                                                                    dico['GovNucleus'] = str(tupla[10])
                                                                    dico['Innucleus'] = str(tupla[11])
                                                                    dico['GovPostnucleus'] = str(tupla[12])
                                                                    dico['IU_parenthesis'] = str(tupla[13])
                                                                    dico['IU_graft'] = str(tupla[14])
                                                                    dico['IU_embedded'] =str(tupla[15])
                                                                    dico['AssociatedNucleus'] = str(tupla[16])
                                                                    dico['Intro_IU'] =str(tupla[17])
                                                                    dico['Layer'] = str(tupla[18])
                                                                    dico['TypePara'] = str(tupla[19])
                                                                    dico['TypeInherited'] = str(tupla[20])
                                                                    dico['IU'] = str(tupla[21])
                                                                    dico['GovInnucleus'] = str(tupla[22])
                                                                    dico['Period'] = str(tupla[23])
                                                                    dico['Period_tone'] = str(tupla[24])
                                                                    dico['Package'] =str(tupla[25])
                                                                    dico['Package_type'] = str(tupla[26])
                                                                    dico['PackageTone'] =str(tupla[27])
                                                                    dico['Group'] = str(tupla[28])
                                                                    dico['GroupTone'] = str(tupla[29])
                                                                    dico['Foot'] = str(tupla[30])
                                                                    dico['FootType'] = str(tupla[31])
                                                                    dico['FootTone'] = str(tupla[32])
                                                                    dico['NextBreakLength'] = str(tupla[33])
                                                                    
                                                                    tuples_deja_faites.add(tupla)
                                                                    
                                                                    break
     
                                      
    return liste_drafts

def effacer_valeurs(liste_drafts):
    '''Efface des clé qui ont de valeurs qui ne sont pas nécessaires comme "nan" et "O"'''
    for draft_conllu in liste_drafts:
        for i in range(len(draft_conllu)):
            sentence = draft_conllu[i]
            features = sentence.features
            for id, dico in features.items():
                dico_copie = dico.copy()
                for key, value in dico_copie.items() :
                    if dico[key] == "O":
                        dico.pop(key)
                    elif dico[key] == "nan":
                        dico.pop(key)
    return liste_drafts

def transformer_valeurs(liste_drafts):
    '''Corrige le format des valeurs ajoutées selon le dictionnaire "dico_reponse"'''
    for draft_conllu in liste_drafts:
        for i in range(len(draft_conllu)):
            sentence = draft_conllu[i]
            features = sentence.features
            for id, dico in features.items():
                dico_copie = dico.copy()
                for key, value in dico_copie.items() :
                     for llave, valor in dico_reponse.items():
                        if value == llave:
                            dico[key] = valor 
                    
        
    return liste_drafts


def main():
    
    parser = argparse.ArgumentParser(description="Ajoutez les directoires des fichiers conllu et fichiers tabulaires")
    parser.add_argument('-t','--dir_tabulaire', help="Ajoutez le ch emin du directoire des fichiers tabulaires")
    parser.add_argument('-c','--dir_conllu', help="Ajoutez le chemin du directoire des fichiers conllu")
    parser.add_argument('-o','--output_dir', help="Ajoutez le chemin du directoire d'output")
    args = parser.parse_args()
    
    liste_conllu, liste_filename = obtenir_conllu(args.dir_conllu)
    liste_tabular = obtenir_tabular(args.dir_tabulaire)
    liste_tuples = obtenir_data_tabular(liste_tabular)
    liste_tuples_propres = tupla_tabular(liste_tuples)
   
    
    drafts_alignes = creation_alignement(liste_conllu, liste_tuples_propres, liste_filename)
    effacer = effacer_valeurs(drafts_alignes)
    transformation = transformer_valeurs(effacer)
    exporter_corpus(transformation, args.output_dir, liste_filename)
    
    #python3.11 creation_alignements_dialogues.py -t /Users/maria23paz/Documents/Stage/Rhapsodie/Tabular_dialogues -c /Users/maria23paz/Documents/Stage/Rhapsodie/dialogues_dep -o /Users/maria23paz/Documents/Stage/Rhapsodie/dialogues_tabulairefix
if __name__== "__main__" :
    main() 

