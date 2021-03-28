from controllers.comprehend import Comprehend 
from db.sqlite import ConMan
import os
import sys
 # unique_filename = str(uuid.uuid4())
# folderPath = './temp/' 
# decryptedPdfFileName = folderPath+ unique_filename + ' _decrypted.pdf'
# decrypt_pdf('Laporan-CCIS-Akaun-Mule-Bank23-07-2020.pdf', decryptedPdfFileName, 'CCID20200723')
# convert_img(decryptedPdfFileName, folderPath + unique_filename)
if __name__ == '__main__':
    with ConMan() as con:
        con._create_tables();
        
    params = sys.argv[1:]
    filename = params[0]
    password = params[1]
    # ocr_table(params[0])
    if not os.path.exists('temp'):
        os.makedirs('temp')
    with Comprehend() as comprehend:
        comprehend.Start(filename=filename, password=password, decrypt=True)