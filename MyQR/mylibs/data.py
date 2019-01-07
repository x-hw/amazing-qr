# -*- coding: utf-8 -*-

from MyQR.mylibs.constant import char_cap, required_bytes, mindex, lindex, num_list, alphanum_list, grouping_list, mode_indicator

# ecl: Error Correction Level(L,M,Q,H)
def encode(ver, ecl, str):
    mode_encoding = {
            'numeric': numeric_encoding,
            'alphanumeric': alphanumeric_encoding,
            'byte': byte_encoding,
            'kanji': kanji_encoding
            }

    ver, mode = analyse(ver, ecl, str)

    print('line 16: mode:', mode)

    code = mode_indicator[mode] + get_cci(ver, mode, str) + mode_encoding[mode](str)

    # Add a Terminator
    rqbits = 8 * required_bytes[ver-1][lindex[ecl]]
    b = rqbits - len(code)
    code += '0000' if b >= 4 else '0' * b

    # Make the Length a Multiple of 8
    while len(code) % 8 != 0:
        code += '0'

    # Add Pad Bytes if the String is Still too Short
    while len(code) < rqbits:
        code += '1110110000010001' if rqbits - len(code) >= 16 else '11101100'

    data_code = [code[i:i+8] for i in range(len(code)) if i%8 == 0]
    data_code = [int(i,2) for i in data_code]

    g = grouping_list[ver-1][lindex[ecl]]
    data_codewords, i = [], 0
    for n in range(g[0]):
        data_codewords.append(data_code[i:i+g[1]])
        i += g[1]
    for n in range(g[2]):
        data_codewords.append(data_code[i:i+g[3]])
        i += g[3]

    return ver, data_codewords

def analyse(ver, ecl, str):
    if all(i in num_list for i in str):
        mode = 'numeric'
    elif all(i in alphanum_list for i in str):
        mode = 'alphanumeric'
    else:
        mode = 'byte'

    m = mindex[mode]
    l = len(str)
    for i in range(40):
        if char_cap[ecl][i][m] > l:
            ver = i + 1 if i+1 > ver else ver
            break

    return ver, mode

def numeric_encoding(s):
    str_list = [s[i:i+3] for i in range(0, len(s), 3)]
    bin_len = (4, 7, 10)
    return ''.join([_int2bin(int(x), bin_len[len(x)-1]) for x in str_list])

def alphanumeric_encoding(s):
    code_list = [alphanum_list.index(x) for x in s]

    codes = []
    for i in range(1, len(code_list), 2):
        codes.append(_int2bin(code_list[i-1] * 45 + code_list[i], 11))

    if len(code_list) % 2 == 1:
        codes.append(_int2bin(code_list[-1], 6))

    return ''.join(codes)

def byte_encoding(s):
    return ''.join([_int2bin(ord(x.encode('shift_jis')), 8) for x in s])
    # return ''.join([_int2bin(ord(x.encode('iso-8859-1')), 8) for x in s])

def kanji_encoding(str):
    pass

# cci: character count indicator
def get_cci(ver, mode, str):
    if 1 <= ver <= 9:
        cci_len = (10, 9, 8, 8)[mindex[mode]]
    elif 10 <= ver <= 26:
        cci_len = (12, 11, 16, 10)[mindex[mode]]
    else:
        cci_len = (14, 13, 16, 12)[mindex[mode]]

    return _int2bin(len(str), cci_len)

def _int2bin(i, l):
    return bin(i)[2:].rjust(l, '0')

if __name__ == '__main__':
    s = '123456789'
    v, datacode = encode(1, 'H', s)
    print(v, datacode)
