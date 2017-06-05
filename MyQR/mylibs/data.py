# -*- coding: utf-8 -*-

import re
from MyQR.mylibs.constant import char_cap, required_bytes, mindex, lindex, num_list, alphanum_list, grouping_list, mode_indicator

RE_numpat = re.compile('[0-9]+')
RE_alpnumpat = re.compile(r'[' + re.escape('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:') + r']+')
RE_chinesepat = re.compile('[\u4E00-\u9FA5\uFB00-\uFFFD\u3000-\u303F]+')
RE_bytespat = re.compile('[\x00-\xff]+')

ModeNameList = ['numeric', 'alphanumeric', 'byte', 'kanji']

ModePattern = {
    'numeric':RE_numpat,
    'alphanumeric':RE_alpnumpat,
    'byte':RE_bytespat,
    'kanji':RE_chinesepat
}

# ecl: Error Correction Level(L,M,Q,H)
def encode(ver, ecl, str):
    mode_encoding = {
            'numeric': numeric_encoding,
            'alphanumeric': alphanumeric_encoding,
            'byte': byte_encoding,
            'kanji': chinese_encoding
            }
    # analyse all modes.
    tmpstr = str
    code_list = []
    while tmpstr:
        mode, span = analyse(tmpstr)
        if not mode:
            break
        print('line 16: mode:', mode)
        code_list.append({
            'str':tmpstr[span],
            'mode':mode,
            'mode_encoding':mode_encoding[mode](tmpstr[span])})
        tmpstr = tmpstr[span.stop:]
    
    totalbits = get_required_bits(ver, code_list)

    tmpver = ver
    while 8*required_bytes[tmpver-1][lindex[ecl]] < totalbits:
        tmpver += 1
    if tmpver > ver:
        ver = tmpver
    
    # try it again
    totalbits = get_required_bits(ver, code_list)
    while 8*required_bytes[tmpver-1][lindex[ecl]] < totalbits:
        tmpver += 1
    if tmpver > ver:
        ver = tmpver

    code = ''
    for code_item in code_list:
        str, mode, mode_encoding = code_item['str'], code_item['mode'], code_item['mode_encoding']
        if mode == 'kanji':
            code += mode_indicator[mode] + '0001' + get_cci(ver, mode, str) + mode_encoding
        else:
            code += mode_indicator[mode] + get_cci(ver, mode, str) + mode_encoding
    # code = mode_indicator[mode] + get_cci(ver, mode, str) + mode_encoding[mode](str)
    
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
    
def analyse(data):
    # analyse mode
    if not data:
        return None
    mode = None
    for mode_name in ModeNameList:
        match = ModePattern[mode_name].match(data)
        if match:
            mode = mode_name
            break
    if not mode:
        raise ValueError('Invalid data to match: %s' % data)
    span = match.span()
    return mode, slice(span[0], span[1])

def numeric_encoding(str):   
    str_list = [str[i:i+3] for i in range(0,len(str),3)]
    code = ''
    for i in str_list:
        rqbin_len = 10
        if len(i) == 1: 
            rqbin_len = 4
        elif len(i) == 2:
            rqbin_len = 7
        code_temp = bin(int(i))[2:]
        code += ('0'*(rqbin_len - len(code_temp)) + code_temp)
    return code
    
def alphanumeric_encoding(str):
    code_list = [alphanum_list.index(i) for i in str]
    code = ''
    for i in range(1, len(code_list), 2):
        c = bin(code_list[i-1] * 45 + code_list[i])[2:]
        c = '0'*(11-len(c)) + c
        code += c
    if i != len(code_list) - 1:
        c = bin(code_list[-1])[2:]
        c = '0'*(6-len(c)) + c
        code += c
    
    return code
    
def byte_encoding(str):
    code = ''
    for i in str:
        c = bin(ord(i.encode('iso-8859-1')))[2:]
        c = '0'*(8-len(c)) + c
        code += c
    return code
    
def chinese_encoding(str):
    gb2312 = str.encode('gb2312')
    code = ''
    span1 = (0xa1,0xaa)
    span2 = (0xb0,0xfa)
    spansecond = (0xa1,0xfe)
    for i in range(0, len(gb2312), 2):
        first,second = gb2312[i], gb2312[i+1]
        if span1[0] <= first <= span1[1]:
            if not spansecond[0] <= second <= spansecond[1]:
                raise ValueError('Invalid chinese character : %s' % str(i//2))
            # type 1
            first = first - 0xa1
            second = second - 0xa1
            tmpcode = bin(first*0x60+second)[2:]
            tmpcode_len = len(tmpcode)
            tmpcode = '0'*(13-tmpcode_len) + tmpcode
            code += tmpcode

        elif span2[0] <= first <= span2[1]:
            if not spansecond[0] <= second <= spansecond[1]:
                raise ValueError('Invalid chinese character : %s' % str(i//2))
            # type 2
            first = first - 0xa6
            second = second - 0xa1
            tmpcode = bin(first*0x60+second)[2:]
            tmpcode_len = len(tmpcode)
            tmpcode = '0'*(13-tmpcode_len) + tmpcode
            code += tmpcode
    return code

# cci: character count indicator  
def get_cci(ver, mode, str):
    if 1 <= ver <= 9:
        cci_len = (10, 9, 8, 8)[mindex[mode]]
    elif 10 <= ver <= 26:
        cci_len = (12, 11, 16, 10)[mindex[mode]]
    else:
        cci_len = (14, 13, 16, 12)[mindex[mode]]
        
    cci = bin(len(str))[2:]
    cci = '0' * (cci_len - len(cci)) + cci
    return cci
    
def get_required_bits(ver, code_list):
    totalbits = 0
    for i in code_list:
        if i['mode'] == 'kanji':
            totalbits += 8
        else:
            totalbits += 4
        totalbits += len(get_cci(ver, i['mode'], i['str']))
        totalbits += len(i['mode_encoding'])
    return totalbits
    
if __name__ == '__main__':
    s = '123456789'
    v, datacode = encode(1, 'H', s)
    print(v, datacode)