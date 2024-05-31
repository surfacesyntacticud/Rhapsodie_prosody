# StageModyco

#### division.ipynb

Ce notebook, principalement, permet de :

1. Extraire toutes les syllabes d'un fichier conllu. 
2. Corrige les syllabes, au cas où il y aurait des caractères ind'esirables.
3. Divise les syllabes en attaque, noyau et code.
Ces résultats sont gardés dans un csv. 

Additionnellement, avec lui vous pourrez :

1. Extraire tous les caractères des syllabes.
2. Compter la quantité d'occurrences de chaque caractère, celle-ci se présente dans un dictionnaire. 
3. Trouver toutes les syllabes qui possèdent des caractère indésirable. 


#### modification.py

Ce script permet de : 

1. Faire le transfert des features phonétiques du token gouverneur d'une syllabe ayant l'upos "PUNCT" au token suivant.
2. Corriger les syllabes qui présentent des caractères bizarres à partir du fichier csv issu de _division.ipynb_
3. Ajouter la division en attaque, noyeau et code de chaque syllabe à partir du fichier csv.
4. Créer une clé "phoneticform" qui possède la concatenation des syllabes. Celle-ci correspond à la forme phonetique du token.
5. Enlever le premier caractère des phoneticforms qui se trouvent dans un token ayant le trait "ExternalOnset=True" et faire son transfert au phoneticform précédent, ayant un upos différent de 'PUNCT".
6. Indiquer la position de la syllabe à l'intérieur du token depuis la droite et depuis la gauche. Ces positions se trouvent 
dans des clés StepsFromLeft et StepsFromRight.


#### inventaire.py

Ce script permet de faire un invetaire des tokens avec leurs prononciations :

1. Il remplace des caractères indésirables dans des prononciations. et ajoute celles-ci à un set pour éviter les duplications. Il utilise transformation.py pour le faire.
2. Crée un inventaire sous forme de dictionnaire.
3. Crée un csv avec les colonnes "Forms" et "Pronunciations".