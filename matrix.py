# -*- coding: utf-8 -*-

from mylibs.constant import *

def get_qrmatrix(ver, ecl, bits):
    num = (ver - 1) * 4 + 21
    qrmatrix = [([None] * num * num)[i:i+num] for i in range(num * num) if i % num == 0]

    # Add the Finder Patterns & Add the Separators
    add_finder_and_separator(qrmatrix)
    
    # Add the Alignment Patterns
    add_alignment(ver, qrmatrix)
    
    # Add the Timing Patterns
    add_timing(qrmatrix)
    
    # Add the Dark Module and Reserved Areas
    add_dark_and_reserving(ver, qrmatrix)
    
    # Place the Data Bits
    place_bits(bits, qrmatrix)
    
    # Data Masking
    
    
    return qrmatrix

def add_finder_and_separator(m):             
    for i in range(8):
        for j in range(8):
            if i in (0, 6):
                m[i][j] = m[-i-1][j] = m[i][-j-1] = 0 if j == 7 else 1
            elif i in (1, 5):
                m[i][j] = m[-i-1][j] = m[i][-j-1] = 1 if j in (0, 6) else 0  
            elif i == 7:
                m[i][j] = m[-i-1][j] = m[i][-j-1] = 0
            else:
                m[i][j] = m[-i-1][j] = m[i][-j-1] = 0 if j in (1, 5, 7) else 1
    
def add_alignment(ver, m):
    if ver > 1:
        coordinates = alig_location[ver-2]
        for i in coordinates:
            for j in coordinates:
                if m[i][j] is None:
                    add_an_alignment(i, j, m)
            
def add_an_alignment(row, column, m):
    for i in range(row-2, row+3):
        for j in range(column-2, column+3):
            m[i][j] = 1 if i in (row-2, row+2) or j in (column-2, column+2) else 0
    m[row][column] = 1
    
def add_timing(m):
    for i in range(8, len(m)-8):
        m[i][6] = m[6][i] = 1 if i % 2 ==0 else 0
    
def add_dark_and_reserving(ver, m):
    for j in range(9):
        m[8][j] = m[8][-j-1] = m[j][8] = m[-j-1][8] = 0
    m[8][6] = m[6][8] = m[-8][8] = 1
    
    if ver > 6:
        for i in range(6):
            for j in (-9, -10, -11):
                m[i][j] = m[j][i] = 0
  
def place_bits(bits, m):
    bit = (int(i) for i in bits)

    up = True
    for a in range(len(m)-1, 0, -2):
        a = a-1 if a <= 6 else a
        irange = range(len(m)-1, -1, -1) if up else range(len(m))
        for i in irange:
            for j in (a, a-1):
                if m[i][j] is None:
                    m[i][j] = next(bit)
        up = not up
  
if __name__ == '__main__':
    m = get_qrmatrix(7,'H',1)
    for i in range(len(m)):
        print(m[i])