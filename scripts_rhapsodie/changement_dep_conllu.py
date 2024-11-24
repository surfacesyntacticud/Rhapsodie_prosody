
from conllu import parse
import os
from dico_dependances import dico_correspondance

def obtenir_conllu(corpus_dir):
    
    import os
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
            with open(treebank_path, 'r', encoding='utf-8') as f:
                sentences = parse(f.read())
                liste_fichiers.append(sentences)  # Aquí guardamos las oraciones parseadas
        except Exception as error:
            print(f"Oups ! Ce fichier ne marche pas {treebank_path}: {error}")

    return liste_fichiers, liste_filename

def sans_flat_dev(liste_drafts_1, liste_drafts_2):
    dico_grand_correspondance = {}
    for draft_1, draft_2 in zip(liste_drafts_1, liste_drafts_2):
        for sentence_1, sentence_2 in zip(draft_1, draft_2):
            features_1 = {token['id']: token for token in sentence_1}
            features_2 = {token['id']: token for token in sentence_2}

            meta_1 = sentence_1.metadata
            sent_id_1 = meta_1.get("sent_id")
            meta_2 = sentence_2.metadata
            sent_id_2 = meta_2.get("sent_id")
            #print(sent_id_1, sent_id_2)

            if sent_id_1 in dico_correspondance and dico_correspondance[sent_id_1] == sent_id_2:
                id_correspondance = {}
                id_utilises = set()

                
                for id_1, token_1 in features_1.items():
                    form_1 = token_1['form']
                    for id_2, token_2 in features_2.items():
                        form_2 = token_2['form']
                        if form_1 == form_2 and id_2 not in id_utilises:
                            id_correspondance[id_1] = id_2
                            id_utilises.add(id_2)
                            # print(sent_id_2 + "---------------------------")
                            # print(id_correspondance)
                            dico_grand_correspondance[sent_id_2] = id_correspondance
                            break
    #print(dico_grand_correspondance)
    return liste_drafts_2, dico_grand_correspondance

def changer_head(liste_drafts_2, dico_correspondances):
    for draft in liste_drafts_2:
        for sentence in draft:
            features = {token['id']: token for token in sentence}
            meta = sentence.metadata
            sent_id = meta.get("sent_id")
            #print(sent_id)
            for cle, dico in dico_correspondances.items():
                if sent_id == cle:
                    print(sent_id, cle)
                    for id_2, token_2 in features.items():
                        head_old = token_2['head']
                        if head_old in dico:
                            token_2['head'] = dico[head_old]
                            print(f"cambio {id_2} de {head_old} a {token_2['head']}")
    return liste_drafts_2
                        
def exporter_corpus(liste_drafts, output_dir, liste_filename):
    '''Exporta el corpus actualizado'''
    import os
    os.makedirs(output_dir, exist_ok=True)
    for filename, sentences in zip(liste_filename, liste_drafts):
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            for sentence in sentences:
                f.write(sentence.serialize())
                f.write('\n\n')  
        print(f"Fichier exporté : {output_path}")

def main():
    corpus_1 = "/Users/maria23paz/Documents/Stage/Rhapsodie/Conllu_original/"
    corpus_2 = "/Users/maria23paz/Documents/Stage/Rhapsodie/Conllu_depues_try2/"
    corpus_output = "/Users/maria23paz/Documents/Stage/Rhapsodie/Conllu_dep/"
    liste_drafts_1, liste_filename_1 = obtenir_conllu(corpus_1)
    liste_drafts_2, liste_filename_2 = obtenir_conllu(corpus_2)
    drafts_finale, gran_dico = sans_flat_dev(liste_drafts_1, liste_drafts_2)
    # print(drafts_finale)
    # print(gran_dico)
    liste_drafts_finale = changer_head(drafts_finale, gran_dico)
    exporter_corpus(liste_drafts_finale, corpus_output, liste_filename_2)

if __name__ == "__main__":
    main()