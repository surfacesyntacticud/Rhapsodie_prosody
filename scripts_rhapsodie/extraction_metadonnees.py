import grewpy
from grewpy import Corpus, CorpusDraft
import re 
import os
import argparse
from bs4 import BeautifulSoup
from dico_dialogues import dico_dialogues


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
    for xml_doc, draft_conllu, nom_file in zip(liste_fichiers_xml, liste_drafts, liste_filename):
        with open(xml_doc, 'r') as fichier: 
            soup = BeautifulSoup(fichier, 'lxml-xml')
            
            interactivity = soup.find("Interactivity")
            planningtype = soup.find("PlanningType")
            involvement = soup.find("Involvement")
            socialcontext = soup.find("SocialContext")
            eventstructure = soup.find("EventStructure")
            channel = soup.find("Channel")
            
            interactivity = interactivity.text if interactivity else "unknown"
            planningtype = planningtype.text if planningtype else "unknown"
            involvement = involvement.text if involvement else "unknown"
            socialcontext = socialcontext.text if socialcontext else "unknown"
            eventstructure = eventstructure.text if eventstructure else "unknown"
            channel = channel.text if channel else "unknown"
            
            for i in range(len(draft_conllu)):
                sentence = draft_conllu[i]
                meta = sentence.meta
                sent_id = meta["sent_id"].split("-")[0]
                sent_parts = sent_id.split("_")
                
                if len(sent_parts) == 2:
                    premiere_partie, deuxieme_partie = sent_parts
                else:
                    premiere_partie, deuxieme_partie = "unknown", "unknown"
                
                meta['type_production'] = 'dialogue' if 'D' in sent_id else 'monologue'
                
                role = name = fullname = familysocialrole = age = sex = education = "unknown"
                
                if 'M' in nom_file:
                    actor = soup.find("Actor")
                    if actor:
                        role = actor.find("Role").text if actor.find("Role") else "unknown"
                        name = actor.find("Name").text if actor.find("Name") else "unknown"
                        fullname = actor.find("FullName").text if actor.find("FullName") else "unknown"
                        familysocialrole = actor.find("FamilySocialRole").text if actor.find("FamilySocialRole") else "unknown"
                        age = actor.find("Age").text if actor.find("Age") else "unknown"
                        sex = actor.find("Sex").text if actor.find("Sex") else "unknown"
                        education = actor.find("Education").text if actor.find("Education") else "unknown"
                
                elif 'D' in nom_file:
                    print(nom_file)
                    dialogue_id = sent_id.split('-')[0].replace("Rhap_", "")
                    print(dialogue_id)
                    if dialogue_id in dico_dialogues:
                        speaker_key = meta['speaker']
                        
                        if speaker_key in dico_dialogues[dialogue_id]:
                            print(speaker_key)
                            identifiant =f"§{dico_dialogues[dialogue_id][speaker_key]}"
                            
                            print(identifiant)
                            actors = soup.find_all("Actor")
                            
                            actor = None
                            for a in actors:
                                name_tag = a.find("Name")
                                if name_tag and name_tag.text.strip() == identifiant:
                                    actor = a
                                    break
                                 
                            if actor:
                                role = actor.find("Role").text if actor.find("Role") else "unknown"
                                print(role)
                                name = actor.find("Name").text if actor.find("Name") else "unknown"
                                fullname = actor.find("FullName").text if actor.find("FullName") else "unknown"
                                age = actor.find("Age").text if actor.find("Age") else "unknown"
                                sex = actor.find("Sex").text if actor.find("Sex") else "unknown"
                                education = actor.find("Education").text if actor.find("Education") else "unknown"
                
                meta.update({
                    "interactivity": interactivity.lower(),
                    "planning_type": planningtype.lower(),
                    "involvement": involvement.lower(),
                    "social_context": socialcontext.lower(),
                    "event_structure": eventstructure.lower(),
                    "channel": channel.lower(),
                    "role": role.lower(),
                    "name": name,
                    "fullname": fullname,
                    "family_social_role": familysocialrole.lower(),
                    "age": age.lower(),
                    "sex": sex.lower(),
                    "education": education.lower(),
                    "sound_url": f"https://rhapsodie.modyco.fr/rp/waves/{premiere_partie}-{deuxieme_partie}.mp3"
                })
                
                ordered_meta = {
                    "sent_id": meta.get("sent_id", "unspecified"),
                    "old_id": meta.get("old_id", "unspecified"),
                    "type": meta.get("type_production", "unspecified"),
                    "prosody": meta.get("prosody", "yes"),
                    "speaker": meta.get("speaker", "L1"),
                    "speaker_id": meta.get("name", "unspecified").strip() or "unspecified",
                    "speaker_fullname": meta.get("fullname", "unspecified").strip() or "unspecified",
                    "speaker_role": meta.get("role", "unspecified").strip() or "unspecified",
                    "speaker_age": meta.get("age", "unspecified").strip() or "unspecified",
                    "speaker_sex": meta.get("sex", "unspecified"),
                    "speaker_education": meta.get("education", "unspecified"),
                    "speaker_family_social_role": meta.get("family_social_role", "unspecified").strip() or "unspecified",
                    "interactivity": meta.get("interactivity", "unspecified"),
                    "planning_type": meta.get("planning_type", "unspecified"),
                    "involvement": meta.get("involvement", "unspecified"),
                    "social_context": meta.get("social_context", "unspecified"),
                    "event_structure": meta.get("event_structure", "unspecified"),
                    "channel": meta.get("channel", "unspecified"),
                    "sound_url": meta.get("sound_url", "unspecified"),
                    "macrosyntax": meta.get("macrosyntax", ""),
                    "text": meta.get("text", "")
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