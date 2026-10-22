# -*- coding: utf-8 -*-

import os

from PIL import Image

from amzqr.mylibs.constant import PIXELS_PER_MODULE


def draw_qrcode(abspath, qrmatrix):
    unit_len = PIXELS_PER_MODULE
    is_sq = False
    if isinstance(qrmatrix, (list, tuple)):
        try:
            n = len(qrmatrix)
            if n > 0 and all(isinstance(r, (list, tuple)) and len(r) == n for r in qrmatrix):
                is_sq = True
        except (TypeError, ValueError):
            is_sq = False

    if is_sq:
        n = len(qrmatrix)
        # Create a module-resolution image and fill it with putdata
        small_pic = Image.new("1", (n, n), "white")
        data = [0 if m else 1 for row in qrmatrix for m in row]
        small_pic.putdata(data)
        # Scaling up is much faster than drawing individual modules
        qr_scaled = small_pic.resize((n * unit_len, n * unit_len), Image.NEAREST)
        # Create the final image with a 4-module quiet zone on each side
        fs = (n + 8) * unit_len
        pic = Image.new("1", (fs, fs), "white")
        pic.paste(qr_scaled, (4 * unit_len, 4 * unit_len))
    else:
        # Fallback for non-square matrices or other iterables
        x = y = 4 * unit_len
        pic = Image.new("1", [(len(qrmatrix) + 8) * unit_len] * 2, "white")
        for line in qrmatrix:
            for module in line:
                if module:
                    draw_a_black_unit(pic, x, y, unit_len)
                x += unit_len
            x, y = 4 * unit_len, y + unit_len

    saving = os.path.join(abspath, "qrcode.png")
    pic.save(saving)
    return saving


def draw_a_black_unit(p, x, y, ul):
    # Optimization: Use bulk paste for mode-1 images with integer coordinates
    if isinstance(ul, int):
        if ul <= 0:
            return
        if p.mode == "1" and isinstance(x, int) and isinstance(y, int):
            w, h = p.size
            if x >= 0 and y >= 0 and x + ul <= w and y + ul <= h:
                p.paste(0, (x, y, x + ul, y + ul))
                return

    # Fallback to the original loop to preserve partial writes or handle other modes
    for i in range(ul):
        for j in range(ul):
            p.putpixel((x + i, y + j), 0)
