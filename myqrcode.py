# -*- coding: utf-8 -*-

import data, ECC, structure, matrix, draw, os

# ecl: Error Correction Level(L,M,Q,H)
def get_qrcode(ecl, str):
    if ecl not in 'LMQH':
        print('Level Error: please choose one of L,M,Q,H!')
    else:
        try:
            # Data Coding
            ver, data_codewords = data.encode(ecl, str)

            # Error Correction Coding
            ecc = ECC.encode(ver, ecl, data_codewords)
            
            # Structure final bits
            final_bits = structure.structure_final_bits(ver, ecl, data_codewords, ecc)
            
            # Get the QR Matrix
            qrmatrix = matrix.get_qrmatrix(ver, ecl, final_bits)
                
            # Draw the picture and Save it, then return the absolute path
            return draw.draw_qrcode(os.path.abspath('.'), qrmatrix)
            
        except UnicodeEncodeError:
            print('Input Error: please read the README file for the supported characters!!')


if __name__ == '__main__':
    import argparse, os
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument('WORDs', help='The words to produce you QR-code picture, like a URL or a sentence. Please read the README file for the supported characters.')
    argparser.add_argument('-l', '--level', help='Use this argument to choose an Error-Correction-Level: L(Low), M(Medium), Q(Quartile), H(High). Otherwise, just use the default one: Q')
    args = argparser.parse_args()
    
    # the default level is Q
    ecl = args.level if args.level else 'Q'
    path = get_qrcode(ecl, args.WORDs)
    if path is not None:
        print('Succeed! Check out your QR-code at', path)