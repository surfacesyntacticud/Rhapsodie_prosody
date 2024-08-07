import grewpy
from grewpy import Corpus, CorpusDraft
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
                
import grewpy
from grewpy import Corpus, CorpusDraft
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
                
def alignement_punct(liste_drafts):
    '''Ajoute des alignements aux tokens ayant l'upos PUNCT. Pour le faire, il prend l'AlignEnd du token précédent et l'AlignBegin du token suivant. 
    Pour ce qui est des PUNCT qui terminent la phrase, les deux alignements ont la même valeur'''
    for draft_conllu in liste_drafts:
        for i in range(len(draft_conllu)):
            sentence = draft_conllu[i]
            features = sentence.features
            tokens = []
            
            for id, dico in features.items():
                tokens.append(dico.copy())
                
            for i in range(len(tokens)):
                dictionnaire_actuel = tokens[i]
                
                
                if dictionnaire_actuel.get('upos') == "PUNCT":
                    dictionnaire_precedent = tokens[i-1] if i > 0 else None
                    dictionnaire_suivant = tokens[i+1] if i < (len(tokens) - 1) else None
                    print(dictionnaire_actuel)
                    
                    if dictionnaire_precedent and dictionnaire_suivant:
                        
                        align_begin = dictionnaire_precedent.get('AlignEnd')
                        align_end = dictionnaire_suivant.get('AlignBegin')
                    elif dictionnaire_precedent:
                      
                        align_begin = dictionnaire_precedent.get('AlignEnd')
                        align_end = align_begin  
                    elif dictionnaire_suivant:
                        
                        align_begin = dictionnaire_suivant.get('AlignBegin')
                        align_end = align_begin  
                    else:
                        
                        align_begin = None
                        align_end = None
                    
                    
                    if align_begin is not None and align_end is not None:
                        dictionnaire_actuel['AlignBegin'] = align_begin
                        dictionnaire_actuel['AlignEnd'] = align_end
            

            
            for (id, dictionnaire), dico_nouveau in zip(features.items(), tokens):
                features[id] = dico_nouveau
               
    
    return liste_drafts

def main():
    
    parser = argparse.ArgumentParser(description="Ajoutez les directoires des fichiers conllu et fichiers tabulaires")
    parser.add_argument('-c','--dir_conllu', help="Ajoutez le chemin du directoire des fichiers conllu")
    parser.add_argument('-o','--output_dir', help="Ajoutez le chemin du directoire d'output")
    args = parser.parse_args()
    
    liste_conllu, liste_filename = obtenir_conllu(args.dir_conllu)
    creation_alignement = alignement_punct(liste_conllu)
    exporter_corpus(creation_alignement, args.output_dir, liste_filename)
    
    
if __name__== "__main__" :
    main() 
