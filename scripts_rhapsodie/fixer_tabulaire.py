import pandas as pd
import argparse
from dico_id_tabulaire import dico_M2006, dico_M2004, dico_M2003, dico_M2002, dico_M1003, dico_M0023, dico_M0019, dico_M0016, dico_M0014, dico_M0011, dico_M0009, dico_M0007, dico_M0008, dico_M0003

def charger_fichier(ruta_archivo, delimiter='\t'):
    '''Lit le fichier avec pandas'''
    return pd.read_csv(ruta_archivo, delimiter=delimiter)

def treeid_a_str(df, columna="Tree_ID"):
    '''Transforme le tree_id en string'''
    df[columna] = df[columna].astype(str)

def traitement_ids(df, dico_aborder, columna="Tree_ID"):
    '''Change la clé de dico_id_tabulaire pour sa valeur'''
    for i in range(len(df)):
        tree_id = df.at[i, columna]
        if pd.notna(tree_id): 
            original_id = str(tree_id).strip()
            if original_id in dico_aborder:
                df.at[i, columna] = dico_aborder[original_id]
            else:
                try:
                    original_id = str(int(float(tree_id)))
                    if original_id in dico_aborder:
                        df.at[i, columna] = dico_aborder[original_id]
                except ValueError:
                    print(f"Oups ! Mauvais tree {i}: {tree_id}")
                    
def exporter_fichier(df, ruta_archivo, delimiter='\t'):
    df.to_csv(ruta_archivo, sep=delimiter, index=False)
    
def main():
    parser = argparse.ArgumentParser(description="Ajoutez les chemins et le dictionnaire souhaité")
    parser.add_argument('-c','--fichier_micro_macro', help="Ajoutez le chemin du fichier tabulaire")
    parser.add_argument('-o','--output_fichier', help="Ajoutez le chemin d'output du fichier tabulaire")
    parser.add_argument('-d','--dico_aborder', help="Ajoutez le nom du dicctionnaire à aborder")
    args = parser.parse_args()
    
    dico_aborder = globals().get(args.dico_aborder)
    if dico_aborder is None:
        raise ValueError(f"Oups ! Le dictionnaire {args.dico_aborder} n'existe pas.")
    
    df_tabular = charger_fichier(args.fichier_micro_macro)
    treeid_a_str(df_tabular)
    traitement_ids(df_tabular, dico_aborder)
    exporter_fichier(df_tabular, args.output_fichier) 
    
if __name__ == "__main__":
    main()
                   
