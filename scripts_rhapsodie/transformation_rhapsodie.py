'''Enlever les caractères des tokens'''
dico_transformation={
    "-" : "",
    " " : ""
}

lista_transformation = ["-", "'", " ", "__0__", "&", "nan"]

'''Transforme des tokens des fichiers tabulaires'''
dico_contracte = {
    "c": "c'",
    "d": "d'",
    "l": "l'",
    "s": "s'",
    "m": "m'",
    "t": "t'",
    "qu": "qu'",
    "j": "j'",
    "jusqu": "jusqu'"
    
}

dico_reponse = {
    "yes": "Yes",
    "pause": "Pause",
    "strong": "Strong",
    "weak": "Weak",
    "W":"Weak",
    "S": "Strong",
    "I": "In",
    "L": "Last",
    "B": "Begin", 
    "H": "Yes",
    "_": "Pause",
    "%": "Overlap",
    "para_disfl":"ParaDisfl",
    "para_coord":"ParaCoord",
    "para_intens": "ParaIntens",
    "para_dform": "ParaDform",
    "para_reform": "ParaReform",
    "para_hyper": "ParaHyper",
    "para_negot": "ParaNegot",
    "pred_inherited": "PredInherited",
    "root_inherited": "RootInherited",
    "sub_inherited": "SubInherited",
    "dep_inherited": "DepInherited",
    "obj_inherited": " ObjInherited",
    "obl_inherited": "OblInherited",
    "ad_inherited": "AdInherited"  
    
}
