import grewpy
from grewpy import Corpus, CorpusDraft
from obtenir_exporter_conllu import obtenir_conllu, exporter_corpus

'''Change les valeurs None en 0'''
def not_none(conllu_new):
    for draft_conllu in conllu_new:
        for i in range(len(draft_conllu)):
            sentence = draft_conllu[i]
            features = sentence.features
            for id, dico in features.items():
                dico_copie = dico.copy()
                for k, v in dico_copie.items():
                    if v == 'None':
                        dico[k] = str(0)
    
    return conllu_new


def main():
    output_dir = './Rhapsodie/corpus_not_none'
    conllu_new, filename_new = obtenir_conllu('./Rhapsodie/corpus_metadonnes')
    conllu_old_id = not_none(conllu_new)
    
    exporter_corpus(conllu_old_id, output_dir, filename_new )

if __name__ == "__main__":
    main()