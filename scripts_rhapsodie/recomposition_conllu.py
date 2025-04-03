import grewpy
from grewpy import Corpus, CorpusDraft
import os
import re

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

def transformer_misc(misc_avant, misc_flat, token_count):
    '''Réorganise les syllabes et les features prosodiques pour le nouveau token recomposé.'''
    liste_syl_par_token = []
    misc_avant = misc_avant.replace('\n', '')
    misc_flat = misc_flat.replace('\n', '')
    misc_avant_dict = dict(item.split("=") for item in misc_avant.split("|") if "=" in item)
    misc_flat_dict = dict(item.split("=") for item in misc_flat.split("|") if "=" in item)
    
    
    align_end = misc_flat_dict.get("AlignEnd", "")
    misc_avant_dict['AlignEnd'] = align_end
    
    for key1 in misc_avant_dict.keys():
        if key1.startswith("Syl") and key1 != "SyllableCount":
            nueva_key = re.split(r'(\d+)', key1)
            liste_syl_par_token.append(nueva_key)
            
    count_syllabes = int(liste_syl_par_token[-1][1]) if liste_syl_par_token else 0
    count_final = count_syllabes + int(misc_flat_dict.get("SyllableCount", "0"))

    for key, value in misc_flat_dict.items():
        if key.startswith("Syl") and key != "SyllableCount":
            key_parts = re.split(r'(\d+)', key)  
            old_syll_num = int(key_parts[1])
            suffix = "".join(key_parts[2:])  
            new_key = f"Syl{count_syllabes + old_syll_num}{suffix}"  
            misc_avant_dict[new_key] = value
        
        else:
            if key not in ["AlignBegin", "AlignEnd", "SpaceAfter", "AttachTo", 'SyllableCount', 'Overlap']:
                new_key = f"{key}Token{token_count}"
                misc_avant_dict[new_key] = value
            elif key == 'SyllableCount':
                misc_avant_dict['SyllableCount'] = count_final
                
                

    
    # print("misc_avant_dict final:", repr("|".join(f"{k}={v}" for k, v in misc_avant_dict.items())))


    return "|".join(f"{k}={v}" for k, v in misc_avant_dict.items()) + "\n"

def cle_flatdev(liste_listes):
    '''Remet ensemble les tokens décomposés de type "Saint-Jean" ayant la partie du discours flat@dev.'''
    nouvelles_listes = []
    for liste in liste_listes:
        nouvelle_liste = []
        i = 0
        while i < len(liste):
            ligne = liste[i]
            if "flat@dev" in ligne:
                if nouvelle_liste:
                    partes_avantflat = nouvelle_liste.pop().split("\t")
                    partes_flat = ligne.split("\t")
                    
                    
                    idx, form, lemma, upos, xpos, feats, head, deprel, deps, misc = partes_flat
                    idx_avant, form_avant, lemma_avant, upos_avant, xpos_avant, feats_avant, head_avant, deprel_avant, deps_avant, misc_avant = partes_avantflat
                    
                    # misc_cols = misc.split('|')
                    # misc_avantcols = misc_avant.split('|')
                    
                    if int(head) == int(idx_avant):
                        nouvelle_form = form_avant + '-' + form 
                        token_count = len(nouvelle_form.split('-'))
                        new_misc = transformer_misc(misc_avant, misc, token_count)
                        nouvelle_ligne = "\t".join([idx_avant, nouvelle_form, nouvelle_form, upos_avant, xpos_avant, feats_avant, head_avant, deprel_avant, deps_avant, new_misc])
                        nouvelle_liste.append(nouvelle_ligne)
                    else:
                        nouvelle_liste.append("\t".join(partes_avantflat)) 
                        nouvelle_liste.append(ligne)
            
            else:
                nouvelle_liste.append(ligne)
            
            i += 1
        nouvelles_listes.append(nouvelle_liste)
    return nouvelles_listes

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
    output_dir = '../conllu_recompose'
    liste_fichiers, liste_filename = obtenir_conllu("../corpus_prosodic")
    liste_liste = obtenir_lignes(liste_fichiers)
    lignes = cle_flatdev(liste_liste)
    lignes_bon_id = fixer_id(lignes)
    lignes_round2 = cle_flatdev(lignes_bon_id)
    bon_id_round2 = fixer_id(lignes_round2)
    exporter_corpus(bon_id_round2, output_dir, liste_filename)

if __name__== "__main__" :
    main() 