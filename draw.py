# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
import os

def draw_qrcode(abspath, qrmatrix):
    unit_len = 9
    x = y = 4*unit_len
    pic = Image.new('1', [(len(qrmatrix)+8)*unit_len]*2, 'white')
    draw = ImageDraw.Draw(pic)
    
    for line in qrmatrix:
        for module in line:
            if module:
                draw.rectangle([x,y,x+unit_len,y+unit_len], fill = 0)
            x += unit_len
        x, y = 4*unit_len, y+unit_len

    saving = os.path.join(abspath, 'qrcode.jpg')
    pic.save(saving)
    #pic.show()
    return saving