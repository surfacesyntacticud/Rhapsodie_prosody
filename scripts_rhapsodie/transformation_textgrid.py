import tgt
import grewpy
from grewpy import Corpus, CorpusDraft
import re 
import os
import argparse
from dico_textgrid import dico_textgrid

def obtenir_conllu(corpus_dir): 
    '''Crée la liste de fichiers conllu et la liste de noms de fichiers pour les exporter après'''
    
    liste_drafts = []  
    liste_non_ordonnee = os.listdir(corpus_dir)
    liste_ordonne = sorted(liste_non_ordonnee)
    for filename in liste_ordonne:
        if filename == ".DS_Store":
            continue
        treebank_path = os.path.join(corpus_dir, filename)
        
        try:
            grewpy.set_config("sud")
            corpus = Corpus(treebank_path)
            draft = CorpusDraft(corpus)
            liste_drafts.append(draft) 
        except Exception as error:
            print(f"Oups ! ce fichier ne marche pas {treebank_path}: {error}")
    #print(liste_filename)
    return liste_drafts

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

def data_textgrid(liste_fichiers_textgrid, liste_filename):
    objets_textgrid = []
    for fichier, nom_fichier in zip(liste_fichiers_textgrid, liste_filename): 
        textgrid_object = tgt.io.read_textgrid(fichier)
        objets_textgrid.append(textgrid_object)
        print(f"fichier {nom_fichier}lu !")
    
    return objets_textgrid

def modification_pivot (objets_textgrid):
    '''Separe les tokens composés dans le tier pivot selon dico_textgrid'''
    
    for textgrid_object in objets_textgrid:
        if 'word' not in [tier.name for tier in textgrid_object]:
            word = textgrid_object.get_tier_by_name("pivot") 
        else:
            word = textgrid_object.get_tier_by_name("pivot") 
            
        phones = textgrid_object.get_tier_by_name("phone")
        for interval in word :
        #print(type(interval))
            for cle in dico_textgrid.keys():
                if cle in interval.text and interval.text != "aujourd'hui":
                    tmin_texte = interval.start_time
                    tmax_texte = interval.end_time
                    texte = interval.text
                    #print(tmin_texte, texte)
                    token_pivot = texte.split("'")
                    premier_token = token_pivot[0] + "'"
                    deuxieme_token = token_pivot[1]
                    #print(token_pivot[1])
                    for phoneme in phones:
                        # print(phoneme)
                        for key, value in dico_textgrid.items():
                            if phoneme.text == value:
                                tmin_phone = phoneme.start_time
                                tmax_phone =phoneme.end_time
                                phon_texte = phoneme.text
                                
                                if key in texte:
                                    try:
                                        if tmin_texte == tmin_phone:
                                            start1 = tmin_texte
                                            end1 = tmax_phone
                                            start2 = tmax_phone
                                            end2 = tmax_texte
                                            #print(f"original :token_pivot {texte}, token_phon {phoneme.text}, tmin pivot {tmin_texte}, tmin_phone {tmin_phone}, tmax_phone {tmax_phone}")
                                            interval.text = premier_token
                                            interval.end_time = end1
                                            # interval1 = tgt.core.Interval(start1, end1, premier_token)
                                            interval2 = tgt.core.Interval(start2, end2, deuxieme_token)
                                            #pivot.delete_annota_between_timepoints(tmin_texte, tmax_texte)
                                            
                                            # pivot.add_interval(interval1)
                                            word.add_interval(interval2) 
                                    except Exception as error:
                                        print(error)
                                        continue
    return objets_textgrid

def modification_word(objets_textgrid, liste_filename):
    seps = [" ", "-", "'"]
    for textgrid_object, nom in zip(objets_textgrid, liste_filename):
        if 'word' not in [tier.name for tier in textgrid_object]:
            word = textgrid_object.get_tier_by_name("words") 
        else:
            word = textgrid_object.get_tier_by_name("word") 
            
        pivot = textgrid_object.get_tier_by_name("pivot")
        
        for interval in word:
            for sep in seps:
                if sep in interval.text:
                    xmin_word, xmax_word = interval.start_time, interval.end_time
                    # print(interval.text)

                    
                    pivot_intervals = []
                    for intervalo in pivot:
                        if intervalo.text != "":
                            if '$' not in intervalo.text:
                                start_pivot = intervalo.start_time
                                end_pivot = intervalo.end_time
                                text = intervalo.text
                                if '-' in text:
                                    texte_propre = text.replace('-', "")
                                elif '$L1' in text or '$L2' in text:
                                    texte_propre = text.replace('$L1', '').replace('$L2', '')
                                else:
                                    texte_propre = text    
                                if (intervalo.start_time >= xmin_word and intervalo.end_time <= xmax_word):
                                    pivot_intervals.append((start_pivot, end_pivot, texte_propre))
                    
                    if not pivot_intervals:
                        continue
                    
                    word.delete_annotations_between_timepoints(xmin_word, xmax_word)
                    for (xmin, xmax, text_final) in pivot_intervals:
                       
                        overlap = False
                        for existing_interval in word:
                            existing_xmin, existing_xmax = existing_interval.start_time, existing_interval.end_time
                            if not (xmax <= existing_xmin or xmin >= existing_xmax): 
                                overlap = True
                                break
                        
                        if not overlap:  
                            intervalo = tgt.core.Interval(xmin, xmax, text_final)
                            word.add_interval(intervalo)
            
    return objets_textgrid

def ajouter_tier (objets_textgrid):
    for textgrid_object in objets_textgrid:
        debut = textgrid_object.start_time
        fin = textgrid_object.end_time
        token = tgt.core.IntervalTier(start_time=debut, end_time=fin, name='tokenId', objects=None)
        textgrid_object.add_tier(token)
        
    return objets_textgrid

def creation_id(objets_textgrid, liste_drafts):
    dernier_align_end = 0.0
    for textgrid_object, draft_conllu in zip(objets_textgrid, liste_drafts):
        if 'word' not in [tier.name for tier in textgrid_object]:
            word = textgrid_object.get_tier_by_name("words") 
        else:
            word = textgrid_object.get_tier_by_name("word") 
        
        token_id = textgrid_object.get_tier_by_name("tokenId")
        for interval in word: 
            for i in range (len(draft_conllu)):
                sentence = draft_conllu[i]
                features = sentence.features
                meta = sentence.meta
                sent_id = meta["sent_id"]
                tree_id = sent_id.split('-')[1]
                print(sent_id)
                if 'prosody' in meta and meta['prosody'] == 'yes':
                    for id, dico in features.items():
                            if interval.text.lower() == dico.get('form').lower():
                                if 'AlignBegin' and 'AlignEnd' in dico:
                                        if float(interval.start_time) >= float(dico.get('AlignBegin', dernier_align_end)) and float(interval.end_time) <= float(dico.get('AlignEnd')):
                                            try:
                                                # print(tree_id, id, interval.text, dico.get('form'), interval.start_time, interval.end_time)
                                                start = interval.start_time
                                                end = interval.end_time
                                                mon_id = str(tree_id)+":"+str(id)
                                                
                                                dernier_align_end = float(dico.get('AlignEnd'))
                                                intervalo = tgt.core.Interval(start, end, mon_id)
                                                    #print(intervalo)
                                                token_id.add_interval(intervalo)
                                                    
                                                    #print(token_id)
                                            except Exception as error:
                                                #print(error)
                                                continue
                else:
                    continue
    return objets_textgrid       
        

def exporter_corpus(objects_textgrid, output_dir, liste_filename): 
    '''Exporte le corpus. Prend comme argument la liste de drafts, la liste de noms des fichiers et le directoire d'output'''          
    os.makedirs(output_dir, exist_ok=True)
    for filename, textgrid in zip(liste_filename, objects_textgrid):
            output_path = os.path.join(output_dir, filename)
            
            try:
                 tgt.io.write_to_file(textgrid, output_path, format='short')
                 print( f"Le fichier a été exporté ! {output_path}")
            except Exception as error:
                print(f"Oups ! Erreur lors de l'exportation du fichier: {error}") 

def main():
    
    parser = argparse.ArgumentParser(description="Ajoutez les directoires des fichiers conllu et fichiers tabulaires")
    parser.add_argument('-t','--dir_textgrid', help="Ajoutez le chemin du directoire des fichiers tabulaires")
    parser.add_argument('-c','--dir_conllu', help="Ajoutez le chemin du directoire des fichiers conllu")
    parser.add_argument('-o','--output_dir', help="Ajoutez le chemin du directoire d'output")
    args = parser.parse_args()
    
    liste_conllu = obtenir_conllu(args.dir_conllu)
    liste_textgrid, liste_filename = obtenir_textgrid(args.dir_textgrid)
    objets_textgrid = data_textgrid(liste_textgrid, liste_filename)
    pivot_modifie = modification_pivot(objets_textgrid)
    objets_modifies = modification_word(pivot_modifie, liste_filename)
    tier_ajoute = ajouter_tier(objets_modifies)
    id_crees = creation_id(tier_ajoute, liste_conllu)
    
    exporter_corpus(id_crees, args.output_dir, liste_filename)
    
    
if __name__== "__main__" :
    main()                    