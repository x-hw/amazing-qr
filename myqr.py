# -*- coding: utf-8 -*-

import argparse, os, theqrmodule

# Alignment Pattern Locations
alig_location = [
    (6, 18), (6, 22), (6, 26), (6, 30), (6, 34), (6, 22, 38), (6, 24, 42), (6, 26, 46), (6, 28, 50), (6, 30, 54), (6, 32, 58), (6, 34, 62), (6, 26, 46, 66), (6, 26, 48, 70), (6, 26, 50, 74), (6, 30, 54, 78), (6, 30, 56, 82), (6, 30, 58, 86), (6, 34, 62, 90), (6, 28, 50, 72, 94), (6, 26, 50, 74, 98), (6, 30, 54, 78, 102), (6, 28, 54, 80, 106), (6, 32, 58, 84, 110), (6, 30, 58, 86, 114), (6, 34, 62, 90, 118), (6, 26, 50, 74, 98, 122), (6, 30, 54, 78, 102, 126), (6, 26, 52, 78, 104, 130), (6, 30, 56, 82, 108, 134), (6, 34, 60, 86, 112, 138), (6, 30, 58, 86, 114, 142), (6, 34, 62, 90, 118, 146), (6, 30, 54, 78, 102, 126, 150), (6, 24, 50, 76, 102, 128, 154), (6, 28, 54, 80, 106, 132, 158), (6, 32, 58, 84, 110, 136, 162), (6, 26, 54, 82, 110, 138, 166), (6, 30, 58, 86, 114, 142, 170)
    ]

argparser = argparse.ArgumentParser()
argparser.add_argument('WORDs', help = 'The words to produce you QR-code picture, like a URL or a sentence. Please read the README file for the supported characters.')
argparser.add_argument('-v', '--version', type = int, choices = range(1,41), help = 'The version means the length of a side of the QR-Code picture. From little size to large is 1 to 40.')
argparser.add_argument('-l', '--level', choices = list('LMQH'), help = 'Use this argument to choose an Error-Correction-Level: L(Low), M(Medium) or Q(Quartile), H(High). Otherwise, just use the default one: H')
argparser.add_argument('-p', '--picture', help = 'the picture  e.g. example_pic.jpg')
argparser.add_argument('-c', '--colorized', action = 'store_true', help = "Produce a colorized QR-Code with your picture. Just works when there is a correct '-p' or '--picture'.")
argparser.add_argument('-con', '--contrast', type = float, help = 'A floating point value controlling the enhancement of contrast. Factor 1.0 always returns a copy of the original image, lower factors mean less color (brightness, contrast, etc), and higher values more. There are no restrictions on this value. Default: 1.0')
argparser.add_argument('-bri', '--brightness', type = float, help = 'A floating point value controlling the enhancement of brightness. Factor 1.0 always returns a copy of the original image, lower factors mean less color (brightness, contrast, etc), and higher values more. There are no restrictions on this value. Default: 1.0')
args = argparser.parse_args()

def combine(qr_name, bg_name, colorized, contrast, brightness, save_place):
    from PIL import Image, ImageEnhance, ImageFilter
    
    qr = Image.open(qr_name)
    qr = qr.convert('RGBA') if colorized else qr
    
    bg0 = Image.open(bg_name).convert('RGBA')
    con = contrast if contrast else 1.0
    bg0 = ImageEnhance.Contrast(bg0).enhance(con)
    bri = brightness if brightness else 1.0
    bg0 = ImageEnhance.Brightness(bg0).enhance(bri)

    if bg0.size[0] < bg0.size[1]:
        bg0 = bg0.resize((qr.size[0]-24, (qr.size[0]-24)*int(bg0.size[1]/bg0.size[0])))
    else:
        bg0 = bg0.resize(((qr.size[1]-24)*int(bg0.size[0]/bg0.size[1]), qr.size[1]-24))    
        
    bg = bg0 if colorized else bg0.convert('1')
    
    aligs = []
    if ver > 1:
        aloc = alig_location[ver-2]
        for a in range(len(aloc)):
            for b in range(len(aloc)):
                if not ((a==b==0) or (a==len(aloc)-1 and b==0) or (a==0 and b==len(aloc)-1)):
                    for i in range(3*(aloc[a]-2), 3*(aloc[a]+3)):
                        for j in range(3*(aloc[b]-2), 3*(aloc[b]+3)):
                            aligs.append((i,j))

    for i in range(bg.size[0]):
        for j in range(bg.size[1]):
            if not ((i in (18,19,20)) or (j in (18,19,20)) or (i<24 and j<24) or (i<24 and j>bg.size[1]-25) or (i>bg.size[0]-25 and j<24) or ((i,j) in aligs) or (i%3==1 and j%3==1) or (bg0.getpixel((i,j))[3]==0)):
                qr.putpixel((i+12,j+12), bg.getpixel((i,j)))
    
    qr_name = os.path.join(save_place, os.path.splitext(bg_name)[0] + '_qrcode.jpg')
    qr.resize((qr.size[0]*2, qr.size[1]*2)).save(qr_name)
    return qr_name

# the default version depends on WORDs and level
# init as 0
ver = args.version if args.version else 0
# the default level is Q
ecl = args.level if args.level else 'H'

if not os.path.exists('temp'):
    os.makedirs('temp')
save_place = os.path.abspath('.') if not args.picture else os.path.join(os.path.abspath('.'), 'temp')
ver, qr_name = theqrmodule.get_qrcode(ver, ecl, args.WORDs, save_place, bool(args.picture))

if args.picture and args.picture[-4:]=='.gif':
    from PIL import Image
    import imageio
     
    print('it takes a while, please wait for minutes...')
     
    im = Image.open(args.picture)
    im.save('temp/0.png')
    while True:
        try:
            seq = im.tell()
            im.seek(seq + 1)
            im.save('temp/%s.png' %(seq+1))
        except EOFError:
            break
    
    imsname = []
    for s in range(seq+1):
        bg_name = 'temp/%s.png' % s
        imsname.append(combine(qr_name, bg_name, args.colorized, args.contrast, args.brightness, ''))
    
    ims = [imageio.imread(pic) for pic in imsname]
    qr_name = os.path.splitext(args.picture)[0] + '_qrcode.gif'
    imageio.mimsave(qr_name, ims)
elif args.picture:
    qr_name = combine(qr_name, args.picture, args.colorized, args.contrast, args.brightness, os.path.abspath('.'))

import shutil
if os.path.exists('temp'):
    shutil.rmtree('temp')     
if qr_name is not None:
    print('Succeed! \nCheck out your ' +str(ver) + '-' + str(ecl) + ' QR-code at', qr_name)