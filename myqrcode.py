# -*- coding: utf-8 -*-

import draw, ecc, data

# ecl: Error Correction Level(L,M,Q,H)
def get_qrcode(ecl, str):
    try:
        ver, code = data.encode(ecl, str)
    except UnicodeEncodeError:
        print('Error input!!')


if __name__ == '__main__':
    # test:
    str = 'hello, world'
    str2 = '💩'
    get_qrcode(str2,1,2)