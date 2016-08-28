# -*- coding: utf-8 -*-

import draw, ECC, data, structure

# ecl: Error Correction Level(L,M,Q,H)
def get_qrcode(ecl, str):
    try:
        # Data Coding
        ver, data_codewords = data.encode(ecl, str)

        # Error Correction Coding
        ecc = ECC.encode(ver, ecl, data_codewords)
        
        # Structure final bits
        final_bits = structure.structure_final_bits(ver, ecl, data_codewords, ecc)
        
        # Get the QR Matrix
        
  
    except UnicodeEncodeError:
        print('Error input!!')


if __name__ == '__main__':
    # test:
    str = 'HELLO WORLD'
    str2 = '💩'
    get_qrcode('M',str)