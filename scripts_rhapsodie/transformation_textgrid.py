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

def data_textgrid(liste_fichiers_textgrid):
    objets_textgrid = []
    for fichier in liste_fichiers_textgrid: 
        textgrid_object = tgt.io.read_textgrid(fichier)
        objets_textgrid.append(textgrid_object)
    
    return objets_textgrid

def modification_pivot (objets_textgrid):
    '''Separe les tokens composés dans le tier pivot selon dico_textgrid'''
    for textgrid_object in objets_textgrid:
        pivot=textgrid_object.get_tier_by_name("pivot")
        phones = textgrid_object.get_tier_by_name("phone")
        for interval in pivot :
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
                                            pivot.add_interval(interval2) 
                                    except Exception as error:
                                        print(error)
                                        continue
    return objets_textgrid

def ajouter_tier (objets_textgrid):
    for textgrid_object in objets_textgrid:
        debut = textgrid_object.start_time
        fin = textgrid_object.end_time
        token = tgt.core.IntervalTier(start_time=debut, end_time=fin, name='tokenId', objects=None)
        textgrid_object.add_tier(token)
        
    return objets_textgrid

def creation_id (objets_textgrid, liste_drafts):
    for draft_conllu in liste_drafts:
        for i in range (len(draft_conllu)):
            sentence = draft_conllu[i]
            features = sentence.features
            meta = sentence.meta
            sent_id = meta["sent_id"]
            if "bis" in sent_id:
                sin_bis = sent_id.replace("bis", '')
            else:
                sin_bis =sent_id
            tree_id = sin_bis.split('-')[1]
            for id, dico in features.items():
                if dico.get('upos') != 'PUNCT' and dico.get('form') != '__0__':
                    for textgrid_object in objets_textgrid:
                        pivot=textgrid_object.get_tier_by_name("pivot")
                        token_id = textgrid_object.get_tier_by_name("tokenId")
                        for interval in pivot:
                            if str(interval.start_time) == dico.get('AlignBegin') and str(interval.end_time) == dico.get('AlignEnd'):
                                try:
                                    #print(tree_id, id, interval.text, dico.get('form'), interval.start_time, interval.end_time)
                                    start = interval.start_time
                                    end = interval.end_time
                                    
                                    intervalo = tgt.core.Interval(start, end, str(tree_id)+":"+str(id))
                                    #print(intervalo)
                                    token_id.add_interval(intervalo)
                                    #print(token_id)
                                except Exception as error:
                                    #print(error)
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
    objets_textgrid = data_textgrid(liste_textgrid)
    objets_modifies = modification_pivot(objets_textgrid)
    tier_ajoute = ajouter_tier(objets_modifies)
    id_crees = creation_id(tier_ajoute, liste_conllu)
    
    exporter_corpus(id_crees, args.output_dir, liste_filename)
    
    
if __name__== "__main__" :
    main()                    