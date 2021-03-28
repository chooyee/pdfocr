import pikepdf
# import module
from pdf2image import convert_from_path

def decrypt_pdf(input_path, output_path, password):
    with pikepdf.open(input_path, password=password) as pdf:
        pdf.save(output_path)

def convert_img(decrypted_pdf, unique_filename):
    # Store Pdf with convert_from_path function
    images = convert_from_path(decrypted_pdf)
    
    for i in range(len(images)):    
        # Save pages as images in the pdf
        images[i].save(unique_filename + '_page'+ str(i) +'.jpg', 'JPEG')

    return images
    
# if __name__ == '__main__':
#     unique_filename = str(uuid.uuid4())
#     folderPath = './temp/' 
#     decryptedPdfFileName = folderPath+ unique_filename + ' _decrypted.pdf'
#     decrypt_pdf('Laporan-CCIS-Akaun-Mule-Bank23-07-2020.pdf', decryptedPdfFileName, 'CCID20200723')
#     convert_img(decryptedPdfFileName, folderPath + unique_filename)