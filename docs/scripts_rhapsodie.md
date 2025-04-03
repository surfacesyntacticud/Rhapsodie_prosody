### Scripts Rhapsodie

Ces scripts sont présentés selon l'ordre d'utilisation. Les monologues et les dialogues ont été enrichis.
#### separer_conll.py 
1. Divise les fichiers _dev_, _test_ et _train_ selon l'identifiant de chaque monologue, par exemple "Rhap-M0001".

#### obtenir_exporter_conllu.py
Ce fichier est importé plusieurs fois pour ouvrir et exporter les fichiers conllu.
1. Crée la liste des drafts issus des fichiers conllu, ainsi que la liste de noms de chaque fichier
2. Exporte le corpus.

#### trouver_mots_composes.py 
Ce script automatise ce qui a été fait à la main sur les dialogues. 
1.  Trouve des mots composés.
2. Crée un dictionnaire avec ces mots où la clé correspond au mots composé et la valeur correspond à une liste avec les tokens issus de la décomposition.
3. Enleve le tiret dans des tokens du type '-ce'.

Le dictionnaire résultat de ce script sera utilisé par fixer_decalage.py

#### fixer_decalage1.py
Ce script a été créé en raison des différences entre le fichier conllu et le fichier tabulaire. Le fichier conllu possédait des tokens composés, lors que tous les tokes du fichier tabulaire étaient séparés. Chacun de ces tokens possède des informations prosodiques et syntaxiques pertinentes, ainsi que les alignements (tmin, tmax) avec le TextGrid, raison pour laquelle il s'avère important de séparer des tokens dans le conllu et ainsi assurer l'extraction des informations mentionnées.  

1. Extrait les lignes du fichier conllu.

2. Si trouve une clé du dictionnaire _décomposer-tokens_, crée des lignes répétées selon la quantité d'éléments qui se trouvent dans le value. Ce dictionnaire a été créés manuellement. Chacun des fichiers a été verifié soigneusement pour identifier les tokes à décomposer.

3. Dans les lignes répétées, attribue les tokens (les valeurs du dictionnaire) et les lemma et change leur relation de dépendance à "flat@dev".

#### dialogues_old_id.py
1. Crée un nouveau sent_id pour chaque arbre en ordre ascendant. L'objectif est d'éviter les sent_id de type "Rhap_D0001-20bis". Celui-ci est stocké dans la variable "old_id" qui s'affichera dans les métadonnées.

#### creation_alignements.py
Utilise le dictionnaire *dico_dialogues_conllu_textgrig.py.* Ce dictionnaire a été fait à la main pour établir une correspondance entre l'id des arbres dans le fichier conllu et l'id des arbres dans le fichier tabulaire. 

1. Extrait les infomations du fichier tabulaire et les ajoute aux features du conllu. Pour le faire, tient compte de la forme du token et de l'id du tree. Pour chaque fichier crée une liste de tuples 
contenant les annotations suivantes: 
*(tree_id,tokens_tabular, tmin, tmax, groupe_type, proeminence_initial, proeminence_finale, hesitation, nucleus, prenucleus, gov_nucleus, innucleus, gov_postnucleus, iu_parenthesis, iu_graft, iu_embedded, associated_nucleus, intro_iu, layer, para, inherited, iu, gov_innucleus, period, period_tone, package, package_type, package_tone, group, group_tone, foot, foot_type, foot_tone, pause)*

2. Efface les features qui ont des valeurs comme "nan" ou "0".

3. Corrige le format des valeurs ajoutées selon le dictionnaire "dico_reponse", dans "transformation rhapsodie".

#### transformation_textgrid.py
1. Sépare les tokens composés sur le tier word, comme "d'avant" et "vis-à-vis". Pour créer une correspondance entre les tokens séparés du conllu et le textgrid. 

2. Crée le tier TokenId.

3. Selon les intervalles des tokens (tmin, tmax), des id pour les tokens sur le TextGrid ont été créés avec l'id de l'arbre et l'id du token sur le fichier conllu. Par exemple _5:14_ fait références au token _14_ de l'arbre _5_. Cette partie a dû être complétée manuellement, étant donné qu'il y avait des intervalles incorrects sur le fichier tabulaire.

#### alignement_punct.py
1. Crée des alignements pour les tokens ayant l'upos PUNCT, pour le bon fonctionnement de _SLAM3.py_ et _fill-conllus-prosody.ipynb_.

#### recomposition_conllu.py
1. Remet ensemble les tokens décomposés de type "Saint-Jean", ayant la partie du discours flat@dev.
2. Réorganise les syllabes et les features prosodiques pour le nouveau token recomposé.

#### convertir_millisecondes.py
1. Change tous les "AlignBegin" et "AlignEnd" de millisecondes à secondes.

#### extraction_metadonnees.py
Ce script utilise *dico_dialogues.py* pour extraire les identifiants des acteurs selon le speaker de chaque sentence (L1, L2, L3).
1. Extrait les metadonnees des fichiers xml et les ajoute au conllu. Prend des valeurs comme _interactivity, plannigtype, involvement, socialcontext, eventstructure, channel, actor, role, name, fullname, familysocialrole, age, sex, education_

#### not_none_values.py
1. Ajoute la valeur numérique 0, lorsqu'il y a une annotation prosodique issue de _fill-conllus-prosody.ipynb_ ayant la valeur _None_. Ce pas est nécessaire pour la conversion à la version syllabifiée du courpus. [Lire la procédure pour obtenir la version prosodique du conllu ici](https://github.com/surfacesyntacticud/tools/tree/master/prosody)
 

Pour les dialogues, certaines sentences ne contiennent pas d’informations prosodiques, car elles se chevauchent avec d’autres sentences (Ces arbres auront l'annotation _Overlap_). De plus, il convient de noter que SLAM3 a réussi à attribuer la majorité des étiquettes pour les monologues, mais plusieurs tokens dans les dialogues n’ont pas pu être annotés, donc c'est normal que quelques arbres aient seulement quelques informations prosodiques.










