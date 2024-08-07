import grewpy
from grewpy import Corpus, CorpusDraft
import re 
import os
import argparse
from bs4 import BeautifulSoup


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

def obtenir_xml(xml_dir):
    '''Crée la liste de fichiers xml'''
   
    liste_fichiers_xml = [] 
    liste_non_ordonnee = os.listdir(xml_dir)
    liste_ordonnee = sorted(liste_non_ordonnee)
    for filename in liste_ordonnee:
        if filename == ".DS_Store":
            continue
        nom_fichier = os.path.join(xml_dir, filename)
        liste_fichiers_xml.append(nom_fichier)
    #print(liste_fichiers)
    return liste_fichiers_xml



def creation_metadonnees(liste_fichiers_xml, liste_drafts, liste_filename):
    '''Extrait les metadonnees des fichiers xml et les ajoute au conllu'''
    for xml_doc, draft_conllu in zip(liste_fichiers_xml, liste_drafts):
        with open(xml_doc, 'r') as fichier: 
            soup = BeautifulSoup(fichier, 'lxml-xml')
            interactivity = soup.find("Interactivity").text
            planningtype = soup.find("PlanningType").text
            involvement = soup.find("Involvement").text
            socialcontext = soup.find("SocialContext").text
            eventstructure = soup.find("EventStructure").text
            channel = soup.find("Channel").text
            
            actor = soup.find("Actor")
            role = actor.find("Role").text
            name = actor.find("Name").text
            fullname = actor.find("FullName").text
            familysocialrole = actor.find("FamilySocialRole").text
            age = actor.find("Age").text 
            sex = actor.find("Sex").text
            education = actor.find("Education").text

            for i in range(len(draft_conllu)):
                sentence = draft_conllu[i]
                meta = sentence.meta
                sent_id = meta["sent_id"].split("-")[0]
                premiere_partie = sent_id.split("_")[0]
                deuxieme_partie = sent_id.split("_")[1]

                meta["interactivity"] = interactivity.lower()
                meta["planning_type"] = planningtype.lower()
                meta["involvement"] = involvement.lower()
                meta["social_context"] = socialcontext.lower()
                meta["event_structure"] = eventstructure.lower()
                meta["channel"] = channel.lower()
                meta["role"] = role.lower()
                meta["name"] = name
                meta["fullname"] = fullname
                meta["family_social_role"] = familysocialrole.lower()
                meta["age"] = age if age != '' else "unknown"
                meta["sex"] = sex.lower()
                meta["education"] = education.lower()
                meta["sound_url"] = f"https://rhapsodie.modyco.fr/rp/waves/{premiere_partie}-{deuxieme_partie}.mp3"
                    
                ordered_meta = {
                    "sent_id": meta["sent_id"],
                    "speaker_id": meta["name"],
                    "speaker_fullname": meta["fullname"],
                    "speaker_role": meta["role"],
                    "speaker_age": meta["age"],
                    "speaker_sex": meta["sex"],
                    "speaker_education": meta["education"],
                    "speaker_family_social_role": meta["family_social_role"],
                    "interactivity": meta["interactivity"],
                    "planning_type": meta["planning_type"],
                    "involvement": meta["involvement"],
                    "social_context": meta["social_context"],
                    "event_structure": meta["event_structure"],
                    "channel": meta["channel"],
                    "sound_url": meta["sound_url"],
                    "macrosyntax": meta.get("macrosyntax", ""),
                    "text": meta["text"],
                }

                sentence.meta = ordered_meta
                        
    return liste_drafts

def exporter_corpus(liste_drafts, output_dir, liste_filename): 
    '''Exporte le corpus. Prend comme argument la liste de drafts, la liste de noms des fichiers et le directoire d'output'''          
    os.makedirs(output_dir, exist_ok=True)
    for filename, draft in zip(liste_filename, liste_drafts):
        output_path = os.path.join(output_dir, filename)
        conll_string = draft.to_conll()
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(conll_string)
            print(f"Fichier exporté : {output_path}")
        except Exception as error:
            print(f"Oups ! Erreur lors de l'exportation du fichier: {error}")

def main():
    parser = argparse.ArgumentParser(description="Ajoutez les directoires des fichiers conllu et fichiers tabulaires")
    parser.add_argument('-x','--dir_xml', help="Ajoutez le chemin du directoire des fichiers tabulaires")
    parser.add_argument('-c','--dir_conllu', help="Ajoutez le chemin du directoire des fichiers conllu")
    parser.add_argument('-o','--output_dir', help="Ajoutez le chemin du directoire d'output")
    args = parser.parse_args()
    
    liste_conllu, liste_filename = obtenir_conllu(args.dir_conllu)
    liste_xml = obtenir_xml(args.dir_xml)
    metadonnees = creation_metadonnees(liste_xml, liste_conllu, liste_filename)
    exporter_corpus(metadonnees, args.output_dir, liste_filename)
    
if __name__== "__main__" :
    main()