# -*- coding: utf-8 -*-

#GP: Generator Polynomial, MP: Message Polynomial
# test:
GP = [0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45]

#DC: Data Codewords, ECC: Error Correction Codewords
def get_ECC(DC, ECC_num):
    po2 = get_power_of_2_list()
    log = get_log_list(po2)
    
    # ..... get the correct GP according to ECC_num
    
    remainder = DC
    for i in range(len(DC)):
        remainder = divide(remainder, GP)
    return remainder
    
def divide(MP, GP):
    a = len(MP) - len(GP)
    if a < 0:
        MP += [0] * (-a)
    elif a > 0:
        GP += [0] * a
    
    log(MP[0])
    
def XOR():
    pass
    
def get_power_of_2_list():
    po2 = [1]
    for i in range(255):
        a = po2[i] * 2
        if a > 255:
            a ^= 285
        po2.append(a)
    return po2
    
def get_log_list(po2):
    log = [None]*256
    for i in range(255):
        log[po2[i]] = i
    return log
    
# test:
dc = '32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17'
