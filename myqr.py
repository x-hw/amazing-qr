# -*- coding: utf-8 -*-

import argparse, os, theqrmodule

# Alignment Pattern Locations
alig_location = [
    (6, 18), (6, 22), (6, 26), (6, 30), (6, 34), (6, 22, 38), (6, 24, 42), (6, 26, 46), (6, 28, 50), (6, 30, 54), (6, 32, 58), (6, 34, 62), (6, 26, 46, 66), (6, 26, 48, 70), (6, 26, 50, 74), (6, 30, 54, 78), (6, 30, 56, 82), (6, 30, 58, 86), (6, 34, 62, 90), (6, 28, 50, 72, 94), (6, 26, 50, 74, 98), (6, 30, 54, 78, 102), (6, 28, 54, 80, 106), (6, 32, 58, 84, 110), (6, 30, 58, 86, 114), (6, 34, 62, 90, 118), (6, 26, 50, 74, 98, 122), (6, 30, 54, 78, 102, 126), (6, 26, 52, 78, 104, 130), (6, 30, 56, 82, 108, 134), (6, 34, 60, 86, 112, 138), (6, 30, 58, 86, 114, 142), (6, 34, 62, 90, 118, 146), (6, 30, 54, 78, 102, 126, 150), (6, 24, 50, 76, 102, 128, 154), (6, 28, 54, 80, 106, 132, 158), (6, 32, 58, 84, 110, 136, 162), (6, 26, 54, 82, 110, 138, 166), (6, 30, 58, 86, 114, 142, 170)
    ]

argparser = argparse.ArgumentParser()
argparser.add_argument('WORDs', help = 'The words to produce you QR-code picture, like a URL or a sentence. Please read the README file for the supported characters.')
argparser.add_argument('-l', '--level', help = 'Use this argument to choose an Error-Correction-Level: L(Low), M(Medium) or Q(Quartile), H(High). Otherwise, just use the default one: Q')
argparser.add_argument('-v', '--version', help = 'The version means the length of a side of the QR-Code picture. From little size to large is 1 to 40.')
argparser.add_argument('-p', '--picture', help = 'the picture  e.g. example_pic.jpg')
args = argparser.parse_args()

# the default version depends on WORDs and level
# init as 0
ver = int(args.version) if args.version and int(args.version) in range(1,41) else 0
# the default level is Q
ecl = args.level if args.level and args.level in 'LMQH' else 'Q'
ver, qr_name = theqrmodule.get_qrcode(ver, ecl, args.WORDs, bool(args.picture))

if args.picture:
    from PIL import Image, ImageEnhance, ImageFilter
    
    qr = Image.open(qr_name).convert('RGBA')
    bg0 = Image.open(args.picture).convert('RGBA')

    bg0 = ImageEnhance.Contrast(bg0).enhance(1.5)
    bg0 = ImageEnhance.Brightness(bg0).enhance(1.3)

    if bg0.size[0] < bg0.size[1]:
        bg0 = bg0.resize((qr.size[0]-24, (qr.size[0]-24)*int(bg0.size[1]/bg0.size[0])))
    else:
        bg0 = bg0.resize(((qr.size[1]-24)*int(bg0.size[0]/bg0.size[1]), qr.size[1]-24))    
        
    bg = bg0#.convert('1')
    
    aligs = []
    if ver > 1:
        aloc = alig_location[ver-2]
        for a in range(len(aloc)):
            for b in range(len(aloc)):
                if not ((a==b==0) or (a==len(aloc)-1 and b==0) or (a==0 and b==len(aloc)-1)):
                    for i in range(3*(aloc[a]-2), 3*(aloc[a]+3)):
                        for j in range(3*(aloc[b]-2), 3*(aloc[b]+3)):
                            aligs += (i,j)

    for i in range(bg.size[0]):
        for j in range(bg.size[1]):
            if not ((i in (18,19,20)) or (j in (18,19,20)) or (i<24 and j<24) or (i<24 and j>bg.size[1]-25) or (i>bg.size[0]-25 and j<24) or (i in aligs and j in aligs) or (i%3==1 and j%3==1) or (bg0.getpixel((i,j))[3]==0)):
                qr.putpixel((i+12,j+12), bg.getpixel((i,j)))

    qr.resize((qr.size[0]*10, qr.size[1]*10)).save(qr_name)
if qr_name is not None:
    print('Succeed! Check out your ' +str(ver) + '-' + str(ecl) + ' QR-code at', qr_name)