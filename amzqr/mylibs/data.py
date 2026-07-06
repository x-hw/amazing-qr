# -*- coding: utf-8 -*-

from amzqr.mylibs.constant import (
    alphanum_list,
    char_cap,
    grouping_list,
    lindex,
    mindex,
    mode_indicator,
    num_list,
    required_bytes,
)


# ecl: Error Correction Level(L,M,Q,H)
def encode(ver, ecl, str):
    mode_encoding = {
        "numeric": numeric_encoding,
        "alphanumeric": alphanumeric_encoding,
        "byte": byte_encoding,
        "kanji": kanji_encoding,
    }

    ver, mode = analyse(ver, ecl, str)

    code = mode_indicator[mode] + get_cci(ver, mode, str) + mode_encoding[mode](str)

    # Add a Terminator
    rqbits = 8 * required_bytes[ver - 1][lindex[ecl]]
    b = rqbits - len(code)
    code += "0000" if b >= 4 else "0" * b

    # Make the Length a Multiple of 8
    while len(code) % 8 != 0:
        code += "0"

    # Add Pad Bytes if the String is Still too Short
    while len(code) < rqbits:
        code += "1110110000010001" if rqbits - len(code) >= 16 else "11101100"

    data_code = [code[i : i + 8] for i in range(len(code)) if i % 8 == 0]
    data_code = [int(i, 2) for i in data_code]

    g = grouping_list[ver - 1][lindex[ecl]]
    data_codewords, i = [], 0
    for n in range(g[0]):
        data_codewords.append(data_code[i : i + g[1]])
        i += g[1]
    for n in range(g[2]):
        data_codewords.append(data_code[i : i + g[3]])
        i += g[3]

    return ver, data_codewords


def analyse(ver, ecl, str):
    if all(i in num_list for i in str):
        mode = "numeric"
    elif all(i in alphanum_list for i in str):
        mode = "alphanumeric"
    else:
        mode = "byte"

    m = mindex[mode]
    l = len(str)
    fit_ver = None
    for i in range(40):
        if char_cap[ecl][i][m] > l:
            fit_ver = i + 1
            break
    if fit_ver is None:
        raise ValueError(
            f"content too long: {l} characters exceed the maximum capacity "
            f"of QR version 1-40 at error correction level {ecl}"
        )
    ver = max(ver, fit_ver)

    return ver, mode


def numeric_encoding(str):
    str_list = [str[i : i + 3] for i in range(0, len(str), 3)]
    code = ""
    for i in str_list:
        rqbin_len = 10
        if len(i) == 1:
            rqbin_len = 4
        elif len(i) == 2:
            rqbin_len = 7
        code_temp = bin(int(i))[2:]
        code += "0" * (rqbin_len - len(code_temp)) + code_temp
    return code


def alphanumeric_encoding(str):
    code_list = [alphanum_list.index(i) for i in str]
    code = ""
    # Pair up chars: each pair encodes to 11 bits via v1*45 + v2.
    for i in range(1, len(code_list), 2):
        c = bin(code_list[i - 1] * 45 + code_list[i])[2:]
        c = "0" * (11 - len(c)) + c
        code += c
    # Trailing unpaired char (odd length) encodes to 6 bits. Judge by length
    # parity, not by the loop variable `i`: when len==1 the loop body never
    # runs and `i` is unbound, so the old `if i != len(code_list) - 1` check
    # raised UnboundLocalError instead of encoding the single char.
    if len(code_list) % 2 == 1:
        c = bin(code_list[-1])[2:]
        c = "0" * (6 - len(c)) + c
        code += c

    return code


def byte_encoding(str):
    code = ""
    for i in str:
        c = bin(ord(i.encode("iso-8859-1")))[2:]
        c = "0" * (8 - len(c)) + c
        code += c
    return code


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

    cci = bin(len(str))[2:]
    cci = "0" * (cci_len - len(cci)) + cci
    return cci


if __name__ == "__main__":
    s = "123456789"
    v, datacode = encode(1, "H", s)
    print(v, datacode)
