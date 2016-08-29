# -*- coding: utf-8 -*-

import data, ECC, structure, matrix, draw

# ecl: Error Correction Level(L,M,Q,H)
def get_qrcode(ecl, str):
    try:
        # Data Coding
        ver, data_codewords = data.encode(ecl, str)
        ndc = 0
        for i in range(len(data_codewords)):
            ndc += len(data_codewords[i])

        # Error Correction Coding
        ecc = ECC.encode(ver, ecl, data_codewords)
        ndc = 0
        for i in range(len(data_codewords)):
            ndc += len(data_codewords[i])
        
        # Structure final bits
        final_bits = structure.structure_final_bits(ver, ecl, data_codewords, ecc)
        
        # Get the QR Matrix
        qrmatrix = matrix.get_qrmatrix(ver, ecl, final_bits)
            
        # Draw the picture
        draw.draw_qrcode(qrmatrix)
  
    except UnicodeEncodeError:
        print('Error input!!')


if __name__ == '__main__':
    # test:
    str = 'HELLO WORLD'
    str2 = 'http://www.thonky.com/qr-code-tutorial/log-antilog-table'
    err = '💩'
    get_qrcode('Q',str)