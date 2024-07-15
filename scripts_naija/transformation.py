'''Pour la transfromation des caractères indésirables'''

dico_transformation= {
   "Ω": "Om",
   "∧": "an",
   "x": "ks",
   "η": "n",
   "Η": "Et",
   "y": "j",
   "*": "X",
   "∫": "in",
   "L": "l",
   "ã": "b",
   "0": "O",
   " ": "",
   "Õ": "O~",
   "α": "al",
   "M": "m",
   "Ε": "Ep",
   "ε": "ep",
   "υ": "up",
   "∃": "Er",
   "õ": "o~",
   "ã": "a~",
   "\\": "",
   "-": "~",
   "`": "",
   "Ο": "On",
   "P": "p",
   "K": "k",
   "n~": "~n",
   "/": "",
   "ω": "om"
}

'''Pour la division des syllabes'''
#Mettre d'abord les phonemes bigraphiques les plus longs !
phonemes_bigraphiques = ["aU~","aI~","ai~","tS","aU", "OI~", "oi", "OI","a~","e~", "i~", "o~","O~", "u~", "E~", "EE", "i~", "u~", "dZ", "aI", "@@",  "eI"]
consonnes=["b","d","f","g","k", "h", "l","m","n","r","p","s", "S","t","v","z", "j","w"]

'''Pour identifier les caractères bizarres dans les syllabes'''
liste_c_indesirables=["`","T","∧","x","Η","y","*","L","B"," ","Õ","F","R","α","M","Ε","ε","K","υ","X","∃","P"]