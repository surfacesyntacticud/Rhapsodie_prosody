



import pandas as pd
import grewpy
from grewpy import Corpus, CorpusDraft
import re
import os
import argparse
from transformation_rhapsodie import dico_reponse, lista_transformation, dico_contracte


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
                

def obtenir_data_tabular(liste_tabular):
    '''Extrait des listes issues des colonnes des fichiers tabulaires. Pour chaque fichier crée une liste de tuples 
    contenant le id du tree, la forme du token, le temps initial, le temps final, le type de groupe rythmique, la prominence initial et finale de la syllabe, l'hésitation le cas échéant et 
    les informations macrosyntaxiques'''
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
        intro_iu =df_tabular["Intro_IU"]
        layer = df_tabular["Layer"]
        para = df_tabular["Type_para"]
        inherited = df_tabular["Type_inherited"]
        
    
        for i, token in enumerate(tokens_tabular):
            for key, value in dico_contracte.items():
                if token == key:
                    tokens_tabular[i] = value
                    
        tuples = list(zip(tree_id,tokens_tabular, tmin, tmax, groupe_type, proeminence_initial, proeminence_finale, hesitation,  
                          nucleus, prenucleus, gov_nucleus, innucleus, gov_postnucleus, iu_parenthesis, iu_graft, iu_embedded, associated_nucleus, intro_iu, layer, para, inherited))
        liste_tuples.append(tuples)

    return liste_tuples

def tupla_tabular(liste_tuples):
    '''Crée une liste de listes de tuples ayant seulement les tokens souhaités'''
    liste_tuples_propres = []
    
    for tuples in zip(liste_tuples):
        trois_ensemble_propre = []
        for element in tuples:
            if element[0] not in lista_transformation:
                trois_ensemble_propre.append(element)
        liste_tuples_propres.append(trois_ensemble_propre)
    
    return liste_tuples_propres
    


def creation_alignement(liste_drafts, liste_tuples):
    '''Ajoute les informations du fichier tabulaire au conllu selon l'id du tree'''
    #print(liste_drafts)
    #print(liste_tuples)
    for draft_conllu, tuples in zip(liste_drafts, liste_tuples):
        sin_bis = None
        tuples_deja_faites = set()
        for i in range(len(draft_conllu)):
            sentence = draft_conllu[i]
            features = sentence.features
            meta = sentence.meta
            sent_id = meta["sent_id"]
            if "bis" in sent_id:
                sin_bis = sent_id.replace("bis", '')
            else:
                sin_bis =sent_id
            tree_id = float(sin_bis.split('-')[1])
            
            #print(f"Procesando tree_id: {tree_id}")
            
            
            for dico in features.values():
                for t in tuples: 
                    for tupla in t:
                    #print(tupla)
                        if dico.get('upos') != 'PUNCT' and dico.get('form') != "__0__":

                            if tupla not in tuples_deja_faites : 
                                if tree_id == tupla[0] and dico.get('form') == tupla[1]:                                            
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
    
    drafts_alignes = creation_alignement(liste_conllu, liste_tuples_propres)
    effacer = effacer_valeurs(drafts_alignes)
    transformation = transformer_valeurs(effacer)
    exporter_corpus(transformation, args.output_dir, liste_filename)
    
    
if __name__== "__main__" :
    main() 

