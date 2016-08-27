# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw

# test:
m1 = [[1]*7+[0]*7+[1]*7,
      [1,0,0,0,0,0,1]+[0]*7+[1,0,0,0,0,0,1],
      [1,0,1,1,1,0,1]+[0]*7+[1,0,1,1,1,0,1],
      [1,0,1,1,1,0,1]+[0]*7+[1,0,1,1,1,0,1],
      [1,0,1,1,1,0,1]+[0]*7+[1,0,1,1,1,0,1],
      [1,0,0,0,0,0,1]+[0]*7+[1,0,0,0,0,0,1],
      [1]*7+[0,1,0,1,0,1,0]+[1]*7,
      [0]*21,
      [0]*6+[1]+[0]*14,
      [0]*21,
      [0]*6+[1]+[0]*14,
      [0]*21,
      [0]*6+[1]+[0]*14,
      [0]*21,
      [1]*7+[0]*14,
      [1,0,0,0,0,0,1]+[0]*14,
      [1,0,1,1,1,0,1]+[0]*14,
      [1,0,1,1,1,0,1]+[0]*14,
      [1,0,1,1,1,0,1]+[0]*14,
      [1,0,0,0,0,0,1]+[0]*14,
      [1]*7+[0]*14
      ]

def draw_qrcode(qrmatrix):
    x, y = 0, 0
    unit_len = 9
    pic = Image.new('1', [len(qrmatrix)*unit_len]*2, 'white')
    draw = ImageDraw.Draw(pic)
    
    for a in range(len(qrmatrix)):
        for b in range(len(qrmatrix[a])):
            if qrmatrix[a][b]:
                draw.rectangle([x,y,x+unit_len,y+unit_len], fill = 0)
            x += unit_len
        x, y = 0, y+unit_len

    pic.save('qrcode.jpg')
    pic.show()

# test:
draw_qrcode(m1)