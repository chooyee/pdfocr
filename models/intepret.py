import pandas as pd
import csv
import spacy
from infra.logger import Logger
import en_core_web_trf
# print(dataframe)
# for ind in dataframe.index:
#     print(dataframe[3][ind])
#     find_name(dataframe[3][ind])
# # data = dataframe.style.set_properties(align="left")
# #Converting it in a excel-file
# dataframe.to_csv("output.csv")

def read_text(dataframe):
    try:
        bankNames =[]
        bankAccs = []
        print(dataframe)
        for ind in dataframe.index:            
            print(dataframe[dataframe.columns[-1]][ind])
            bname, bacc = find_name(dataframe[dataframe.columns[-1]][ind])
            bankNames += bname
            bankAccs += bacc 
        return bankNames, bankAccs
    except Exception as e:
        print("Oops!", str(e), "occurred.")
        print("Oops!", e.__class__, "occurred.")
        Logger.Error(str(e))

def find_name(str):
    bankName = []
    bankAcc = []
    
    nlp = en_core_web_trf.load()
    #nlp = spacy.load("en_core_web_trf") 
    # nlp = spacy.load("en_core_web_sm") 
    ruler = nlp.add_pipe("entity_ruler")
    patterns = [{"label": "ORG", "pattern": "AmBank (M) Berhad"},
                {"label": "ORG", "pattern": "CIMB Bank Berhad"},
                {"label": "ORG", "pattern": "Public Bank Berhad"},
                {"label": "ORG", "pattern": "Malayan Banking Berhad"},
                {"label": "ORG", "pattern": "Bank Islam Malaysia"},
                {"label": "ORG", "pattern": "Alliance Bank Malaysia"},
                {"label": "ORG", "pattern": "Agro Bank Malaysia"},
                {"label": "ORG", "pattern": "Hong Leong Bank Berhad"},
                {"label": "ORG", "pattern": "RHB Bank Berhad"}]
    ruler.add_patterns(patterns)
    nlp.add_pipe("merge_entities")
    doc = nlp(str)
    for token in doc:
        ent = [token.text, token.ent_iob_, token.ent_type_]
        if (token.text.strip()!=''):
            # print(ent)
            if token.ent_type_=='ORG':
                bankName.append(token.text)
            elif  (token.ent_type_=='CARDINAL' or token.ent_type_=='') and len(token.text)>2 and token.text.isnumeric():
                bankAcc.append(token.text)
    return bankName, bankAcc
    # mytuple = (bankName, bankAcc)

    # print(mytuple)