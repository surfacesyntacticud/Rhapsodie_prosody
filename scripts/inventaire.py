'''
Ce script prend comme input un fichier csv avec des tokes et leurs pronunciations, corrige les pronunciations
et en faire un inventaire qui exporte dans un csv.

Commande pour le lancer :

_____
python3.11 inventaire.py -c /Users/maria23paz/Documents/Stage/lexique_proso_clean.csv -o Inventaire_final.csv
_____
'''

import pandas as pd
import argparse
from transformation import dico_transformation  

'''Remplace les caractères indésirables dans les prononciations'''
def modifier_prononciation(liste_prononciation):
    n_set_pronon=set()
    for pron in liste_prononciation:
        nueva_pron=pron
        for key, value in dico_transformation.items():
            if key in nueva_pron:
                nueva_pron=nueva_pron.replace(key, value)
        n_set_pronon.add(nueva_pron)
        n_lista_pronon=list(n_set_pronon)
    return n_lista_pronon

'''Crée une liste avec le token et toutes ses prononciations'''
def inventaire(df):
    pronunciations = df.groupby('Form')['Pronunciation'].apply(list).to_dict()
    lignes = []  

    for form, liste_pronun in pronunciations.items():
        pronunciations_modifiees = modifier_prononciation(liste_pronun)
        lignes.append({'Form': form, 'Pronunciations': ', '.join(pronunciations_modifiees)})

    return lignes


def main ():
    parser =argparse.ArgumentParser(description="Ajoutez le csv à traiter")
    parser.add_argument('-c', '--csv', help= "Ajoutez l'input de l'inventaire")
    parser.add_argument('-o', '--output', help="Ajoutez le nom du fichier d'output")
    args = parser.parse_args()
    
    
    df = pd.read_csv(args.csv)
    lignes=inventaire(df)
    inventaire_df = pd.DataFrame(lignes)
    inventaire_df.to_csv(args.output, index=False)
   
    
if __name__== "__main__" :
    main()    

