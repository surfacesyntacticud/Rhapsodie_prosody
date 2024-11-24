### Scripts Rhapsodie

Ces scripts sont présentés selon l'ordre d'utilisation. Seulement les monologues du corpus Rhapsodie ont été modifiés.

#### separer_conll.py 
1. Divise les fichiers _dev_, _test_ et _train_ selon l'identifiant de chaque monologue, par exemple "Rhap-M0001".

#### fixer_decalage.py
Ce script a été créé en raison des différences entre le fichier conllu et le fichier tabulaire. Le fichier conllu possédait des tokens composés, lors que tous les tokes du fichier tabulaire étaient séparés. Chacun de ces tokens possède des informations prosodiques et syntaxiques pertinentes, ainsi que les alignements (tmin, tmax) avec le TextGrid, raison pour laquelle il s'avère important de séparer des tokens dans le conllu et ainsi assurer l'extraction des informations mentionnées.  

1. Extrait les lignes du fichier conllu.

2. Si trouve une clé du dictionnaire _décomposer-tokens_, crée des lignes répétées selon la quantité d'éléments qui se trouvent dans le value. Ce dictionnaire a été créés manuellement. Chacun des fichiers a été verifié soigneusement pour identifier les tokes à décomposer.

3. Dans les lignes répétées, attribue les tokens (les valeurs du dictionnaire) et les lemma et change leur relation de dépendance à "flat@dev".

#### fixer_tabulaire.py
Une fois les différences de tokens composés ont été réglées, l'extraction a présenté encore des problèmes parce que les id des trees n'étaient pas les mêmes dans le fichier conllu et dans le fichier tabulaire.

1. Modifie les id des trees dans le fichier tabulaire. 
Prend en compte le dico_id_tabulaire, créé à partir des modifications manuelles, selon le cas spécifique de chaque fichier.

Vous pouvez trouver tous les changements faits dans "Description changements fichiers CoNLL-U et tabular.pdf"

#### creation_alignements.py
1.Extrait des listes issues des colonnes des fichiers tabulaires. Pour chaque fichier crée une liste de tuples 
contenant le id du tree, la forme du token, le temps initial, le temps final, le type de groupe rythmique, la prominence initial et finale de la syllabe, l'hésitation le cas échéant et les informations macrosyntaxiques.

2. Crée une nouvelle liste des tuples ayant seulement les tokens souhaités, on n'a pas pris en compte "___0____ ", par exemple.

3. Extrait les infomations du fichier tabulaire et les ajoute aux features du conllu. Pour le faire, tient compte de la forme du token et de l'id du tree.

4. Efface les features qui ont des valeurs comme "nan" ou "0".

5. Corrige le format des valeurs ajoutées selon le dictionnaire "dico_reponse", dans "transformation rhapsodie".

#### transformation_textgrid.py
1. Sépare les tokens composés sur le tier pivot, comme "d'avant". Pour créer une correspondance entre les tokens séparés du conllu et le textgrid. Les tokens composés ont été répérés manuellement.

2. Crée le tier TokenId.

3. Selon les intervalles des tokens (tmin, tmax), des id pour les tokens sur le TextGrid ont été créés avec l'id de l'arbre et l'id du token sur le fichier conllu. Cette partie a dû être complétée manuellement, étant donné qu'il y avait des intervalles incorrects sur le fichier tabulaire.

#### extraction_metadonnees.py
1. Extrait les metadonnees des fichiers xml et les ajoute au conllu. Prend les valeurs comme _interactivity, plannigtype, involvement, socialcontext, eventstructure, channel, actor, role, name, fullname, familysocialrole, age, sex, education_


Pour le bon fonctionnement de _SLAM3.py_ et _fill-conllus-prosody.ipynb_ ces scripts ont été utilisés :

#### alignement_punct.py
1. Crée des alignements pour les tokens ayant l'upos PUNCT.

#### change_utf.py 
1. Ce script simplement prend les fichiers et les garde en "utf-8".

### changement_sentid.py
1. Ce code a été utilisé pour trois fichiers. Il crée un nouveau sent_id en ordre, pour eviter les arbres ayant des identifiants comme "14bis".

#### Note
Le seul fichier où les syllabes, extraites avec _fill-conllus-prosody.ipynb_, n'ont pas été ajoutées correctement est _Rhap-M2001.conllu_.

### changement_dep_conllu.py
1. Dans les arbres où des tokens ont été décomposés, ce code crée un dictionnaire des id des tokens et met a jour les relations de dépendance. 

Attention, les id des arbres ont changé dans quelques occassions. Ce script prend en compte un dictionnaire de correspondances (dico_dependances.py) entre les id des arbres avant et après la décomposition. 