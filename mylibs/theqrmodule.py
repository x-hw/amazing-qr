# -*- coding: utf-8 -*-

from mylibs import data, ECC, structure, matrix, draw

# ver: Version (from 1 to 40)
# ecl: Error Correction Level (L,M,Q,H)
def get_qrcode(ver, ecl, str, save_place, pic_exits = False):
    # ver == 0: default that is depending on str and ecl
    if ver not in range(41):
        print('Version Error: please choose a version from 1 to 40!')
    if ecl not in 'LMQH':
        print('Level Error: please choose one of L,M,Q,H!')
    else:
        try:
            # Data Coding
            ver, data_codewords = data.encode(ver, ecl, str)

            # Error Correction Coding
            ecc = ECC.encode(ver, ecl, data_codewords)
            
            # Structure final bits
            final_bits = structure.structure_final_bits(ver, ecl, data_codewords, ecc)
            
            # Get the QR Matrix
            qrmatrix = matrix.get_qrmatrix(ver, ecl, final_bits)
                
            # Draw the picture and Save it, then return the absolute path
            unit_len = 3 if pic_exits else 9
            return ver, draw.draw_qrcode(save_place, qrmatrix, unit_len)
            
        except UnicodeEncodeError:
            print('Input Error: please read the README file for the supported characters!!')