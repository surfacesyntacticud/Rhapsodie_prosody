'''Ce script utilise le csv issu du notebook division.ipynb comme input pour la modification des fichiers conllu. Il parcourt
les fichiers d'un directoire, fait des modifications et crée de nouveaux fichiers avec le même nom dans un directoire d'output.

Commande pour le lancer :

_____
python3.11 modification.py -i /Users/maria23paz/Documents/Stage/Prueba -o /Users/maria23paz/Documents/Stage/Prueba_output -c syllabes_divisees6.csv
_____

'''
import os
import re
import pandas as pd
import grewpy
from grewpy import Corpus, CorpusDraft, Request
from ast import literal_eval
import argparse

'''
Crée une liste de drafts et une liste de filenames à partir du directoire d'input
'''
def obtenir_corpus(corpus_dir): 
    liste_fichiers = []  
    liste_filename = []
    for filename in os.listdir(corpus_dir):
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
    
    return liste_fichiers, liste_filename
   
'''
Exporte les fichier avec les mnodifications faites
'''        
def exporter_corpus(liste_drafts, output_dir, liste_filename):           
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

'''
Transfert les features phonétiques du token gouverneur d'une syllabe ayant l'upos "PUNCT" au token suivant. 
'''
def ajustement_features(liste_draft):
    pattern = re.compile(r'^Syl\d+|^SyllableCount$|^UtteranceMeanF0$')
    for draft in liste_draft:      
        for j in range(len(draft)):  
            sentence = draft[j]
            features = sentence.features         
            
            tokens=[]
            for i_d, dico in features.items():
                tokens.append(dico.copy()) 
                
            for i in range(1,len(tokens)-1):
                dictionnaire_actuel=tokens[i]
                #print(dictionnaire_actuel)
                dictionnaire_suivant=tokens[i+1]
                keys_a_mover=[]
                
                if dictionnaire_actuel.get('upos') == 'PUNCT':
                    for key in dictionnaire_actuel:
                        if pattern.match(key):
                        #print(dictionnaire_actuel)
                            keys_a_mover.append(key)
                    
                    for key in keys_a_mover:
                        #print(key) 
                        if key not in dictionnaire_suivant:
                            dictionnaire_suivant[key] = dictionnaire_actuel[key]
                            
                    tokens[i]= {key:value for key, value in dictionnaire_actuel.items() if key not in keys_a_mover}
                    
                                
            for (id, dictionnaire), dico_nouveau in zip(features.items(), tokens):
                features[id] = dico_nouveau         
                        
    return liste_draft  

'''
Corrige les syllabes qui présentaient des caractères bizarres à partir d'un fichier csv.
'''       
def trans_syllabe(liste_draft, original, transformees):
    pattern= re.compile(r'^Syl\d+$')
    for draft in liste_draft:
        for i in range(len(draft)):
            sentence = draft[i]
            features = sentence.features
            
            for id, dico in features.items():
                for key in dico:
                    if pattern.match(key):
                        for syllabe, nouvelle in zip(original, transformees):
                                if dico[key]== syllabe:
                                    dico[key]=nouvelle
                                
    return liste_draft

'''
Ajoute la division en  attaque, noyeau et coda de chaque syllabe à partir d'un fichier csv.
'''
def ajouter_division(liste_draft, transformees, divisees):
    pattern= re.compile(r'^Syl\d+$') 
    for draft in liste_draft:                    
        for i in range(len(draft)):
            sentence = draft[i]
            features = sentence.features
            
            for i_d, dico in features.items(): 
                dico_copy = dico.copy()  
                
                for key in dico_copy: 
                        if pattern.match(key):  
                            for syllabe_nouv, syllabe_sep in zip(transformees, divisees):
                                if dico_copy[key] == syllabe_nouv:
                                    syllabe_parts = literal_eval(syllabe_sep)
                                    onset = syllabe_parts[0] if len(syllabe_parts) >= 2 else None
                                    nucleus = syllabe_parts[1] if len(syllabe_parts) >= 2 else (syllabe_parts[0] if len(syllabe_parts) == 1 else None)
                                    coda = syllabe_parts[2] if len(syllabe_parts) == 3 else None
                                    
                                    temp_dico = {}

                                    if onset:
                                        temp_dico[f"{key}Onset"] = onset
                                    else:
                                        temp_dico[f"{key}Onset"] = "None"
                                        
                                    if nucleus:
                                        temp_dico[f"{key}Nucleus"] = nucleus
                                    else:
                                        temp_dico[f"{key}Nucleus"] = "None"
                                        
                                    if coda:
                                        temp_dico[f"{key}Coda"] = coda
                                    else:
                                        temp_dico[f"{key}Coda"] = "None"
                                    dico.update(temp_dico)                                
                                    break 
    return liste_draft
  
'''Crée une clé "phoneticform" qui possède la concatenation des syllabes'''        

def concatener_syllabes(liste_draft):
    pattern= re.compile(r'^Syl\d+$') 
    for draft in liste_draft:                   
        for i in range(len(draft)):
            sentence = draft[i]
            features = sentence.features
            for i_d, dico in features.items():
                syllabes_concatenees=[] 
                dico_copy = dico.copy()  
                for key in dico_copy: 
                    if pattern.match(key):
                        syllabes_concatenees.append(dico[key])
                        dico['phoneticform'] = ''.join(syllabes_concatenees)
                        
    return liste_draft


'''
Enlève le premier caractère des phoneticsforms qui se trouvent dans un token ayant le trait "ExternalOnset=True" et le transfert au phoneticform précédent. 
'''


def trouver_non_punct(tokens):
    if not tokens:
        return None
    if tokens[-1].get('upos') != 'PUNCT':
        return tokens[-1]
    return trouver_non_punct(tokens[:-1])
    

def ajustement_external(liste_draft, liste_filename):
    pattern = re.compile(r'^Syl\d+ExternalOnset')

    for filename, draft in zip(liste_filename, liste_draft):
        
        for j in range(1, len(draft)):
            sentence = draft[j]
            features = sentence.features
            tokens = []
            
            try:
                for i_d, dico in features.items():
                    tokens.append(dico.copy())

                for i in range(len(tokens)):
                    dictionnaire_actuel = tokens[i]
                    dictionnaire_precedent = tokens[i-1] if i > 0 else None


                    for key in dictionnaire_actuel:
                        if pattern.match(key):
                            
                            phonetic_form_actuelle = dictionnaire_actuel.get('phoneticform')
                            if not dictionnaire_precedent:
                                if phonetic_form_actuelle:
                                    nouvelle_phform_actuel = phonetic_form_actuelle[1:]
                                    dictionnaire_actuel['phoneticform'] = nouvelle_phform_actuel
                                
                            if dictionnaire_precedent:
                                
                                if dictionnaire_precedent.get('upos') != 'PUNCT':
                                    if dictionnaire_actuel.get('upos') != 'PUNCT':
                                        phonetic_form_actuelle = dictionnaire_actuel.get('phoneticform')
                                        phonetic_form_precedente = dictionnaire_precedent.get('phoneticform')

                                    if phonetic_form_actuelle and phonetic_form_precedente:
                                        premier_caracter = phonetic_form_actuelle[0]
                                        nouvelle_phform_precedent = phonetic_form_precedente + premier_caracter
                                        nouvelle_phform_actuel = phonetic_form_actuelle[1:]
                                        dictionnaire_actuel['phoneticform'] = nouvelle_phform_actuel
                                        dictionnaire_precedent['phoneticform'] = nouvelle_phform_precedent

                                elif dictionnaire_precedent.get('upos') == 'PUNCT':
                                    dictionnaire_precedent = trouver_non_punct( tokens[:i])
                                    
                                    if dictionnaire_precedent:
                                        phonetic_form_actuelle = dictionnaire_actuel.get('phoneticform')
                                        phonetic_form_precedente = dictionnaire_precedent.get('phoneticform')

                                        if phonetic_form_actuelle and phonetic_form_precedente:
                                            premier_caracter = phonetic_form_actuelle[0]
                                            nouvelle_phform_precedent = phonetic_form_precedente + premier_caracter
                                            nouvelle_phform_actuel = phonetic_form_actuelle[1:]
                                            dictionnaire_actuel['phoneticform'] = nouvelle_phform_actuel
                                            dictionnaire_precedent['phoneticform'] = nouvelle_phform_precedent

                for (id, dictionnaire), dico_nouveau in zip(features.items(), tokens):
                    features[id] = dico_nouveau

            except Exception as error:
                print(f"Oups ! Erreur dans le fichier {filename} à la phrase {j} : {error} Voici les features: {features}")
                print("________________________________")

    return liste_draft
        
'''
Indique la position de la syllabe à l'intérieur du token depuis la droite et depuis la gauche. Ces positions se trouvent 
dans des clés StepsFromLeft et StepsFromRight. 
'''                             
def steps_syllabes1(liste_draft):
    pattern= re.compile(r'^Syl\d+$')
    for draft in liste_draft:                    
        for i in range(len(draft)):
            sentence = draft[i] 
            features = sentence.features 
            
            for i_d, dico in features.items(): 
                syllabes_steps=[]
                dico_copy = dico.copy()
                
                for key in dico_copy: 
                        if pattern.match(key):
                            syllabes_steps.append(dico[key])
                
                for i, syllab in enumerate(syllabes_steps):                    
                    izquierda = i + 1 
                    derecha = len(syllabes_steps) - i 
                    tempo_dico={}
                    if izquierda is not None and derecha is not None:
                        tempo_dico[f'Syl{i+1}StepsFromLeft']=str(i+1)
                        tempo_dico[f'Syl{i+1}StepsFromRight']=str(len(syllabes_steps) - i)
                    dico.update(tempo_dico)    
                    
                
    return liste_draft 
     
def main():
    parser = argparse.ArgumentParser(description="Ajoutez les directoires input, output et le csv pour la correction")
    parser.add_argument('-i','--corpus_dir', help="Ajoutez le chemin du directoire d'input")
    parser.add_argument('-o','--output_dir', help="Ajoutez le chemin du directoire d'output")
    parser.add_argument('-c', '--csv', help= 'Ajoutez le csv pour la correction')
    args = parser.parse_args()
    
    draft0, liste_filename = obtenir_corpus(args.corpus_dir)
    

    df = pd.read_csv(args.csv)
    original = df["Syllabes_originales"]
    transformees = df["Syllabes_transformees"]
    divisees = df["Division"]
    
    draftA=ajustement_features(draft0)
    draft1=trans_syllabe(draftA, original, transformees)
    draft2=ajouter_division(draft1, transformees, divisees)
    draft3=concatener_syllabes(draft2)
    draft4=ajustement_external(draft3, liste_filename)
    draft5=steps_syllabes1(draft4)
    
    exporter_corpus(draft5, args.output_dir, liste_filename)

if __name__== "__main__" :
    main()   