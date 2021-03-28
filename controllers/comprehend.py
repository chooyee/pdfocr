from models.pdf import decrypt_pdf, convert_img
from db.sqlite import ConMan 
from models.ocr import ocr_table
from models.intepret import read_text
from infra.logger import Logger
import uuid
import os
import datetime

class Comprehend:
    
    def __init__(self):
        pass

    def Start(self, filename, password=None, decrypt=False):
        try:
            listdate = datetime.datetime.now().strftime("%Y-%m-%d")

            unique_filename = str(uuid.uuid4())
            folderPath = './temp/' 
            decryptedPdfFileName = folderPath+ unique_filename + ' _decrypted.pdf'

            if (decrypt):            
                decrypt_pdf(filename, decryptedPdfFileName, password)
                #decrypt_pdf('Laporan-CCIS-Akaun-Mule-Bank23-07-2020.pdf', decryptedPdfFileName, 'CCID20200723')

            images = convert_img(decryptedPdfFileName, folderPath + unique_filename)

            j = 0
            with ConMan() as con:
                for i in range(len(images)):
                    # if (j==1):
                    print(folderPath + unique_filename + '_page'+ str(j) +'.jpg')
                    dataframe = ocr_table(folderPath + unique_filename + '_page'+ str(j) +'.jpg')
                    print('=============================Read text======================================')
                    bankNames, bankAccs = read_text(dataframe)
                    if (len(bankNames) != len(bankAccs)):                        
                        sql, param = self._cleanBatchRecordSql(unique_filename)
                        con.Execute(sql, param)
                        raise Exception('Number of banks and account number does not match!')
                        break;
                    print('=============================Massage======================================')
                    params = self._massage(bankNames, bankAccs, listdate, unique_filename)
                    #insert into sqlite
                
                    sql = '''insert into conlist (uuid, listdate, bankname, bankaccno) values (?,?,?,?)'''
                    print('=============================Insert======================================')
                    con.Execute(sql, params)
                    j = j+1
        except Exception as e:
            print("Oops!", str(e), "occurred.")
            print("Oops!", e.__class__, "occurred.")
            Logger.Error(str(e))

    def _cleanBatchRecordSql(self, uuid):
        sql = "delete * from conlist where uuid = ?"
        param = (uuid)
        return sql, param

    def _massage(self, bankNames, bankAccs, listdate, uuid):
        params = []
        for i in range(len(bankNames)):
            params.append((uuid, listdate, bankNames[i], bankAccs[i] ))
        return params
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass