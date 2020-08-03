#!/usr/local/bin/python3

# pip3 install -U --user numpy pillow
# pip3 install --user git+https://www.github.com/hbldh/hitherdither
# pip3 install colour-science

import colour
import hitherdither
import numpy
import sys

from PIL import Image, ImageFilter


VDC_EMUATOR_PALETTE = [
    0x000000, # Dark Black
    0x6B6B6B, # Light Black
    0x0000B9, # Dark Blue
    0x6B6BFF, # Light Blue
    0x00B800, # Dark Green
    0x6AFE6A, # Light Green
    0x00B9B9, # Dark Cyan
    0x6BFFFF, # Light Cyan
    0xB80000, # Dark Red
    0xFE6A6A, # Light Red
    0xB900B9, # Dark Purple
    0xFF6BFF, # Light Purple
    0xB86A00, # Dark Yellow
    0xFEFE6A, # Light Yellow
    0xB9B9B9, # Dark White
    0xFFFFFF, # Light White
]

CGA_PALETTE = [
    0x000000, # Dark Black
    0x0000AA, # Dark Blue
    0x00AA00, # Dark Green
    0x00AAAA, # Dark Cyan
    0x555555, # Light Black
    0x5555FF, # Light Blue
    0x55FF55, # Light Green
    0x55FFFF, # Light Cyan
    0xAA0000, # Dark Red
    0xAA00AA, # Dark Purple
    0xAA5500, # Dark Yellow
    0xAAAAAA, # Dark White
    0xFF5555, # Light Red
    0xFF55FF, # Light Purple
    0xFFFF55, # Light Yellow
    0xFFFFFF, # Light White
]

VDC_OFFICIAL_PALETTE = [
    0x000000, # Dark Black
    0x404040, # Light Black
    0x0000A0, # Dark Blue
    0x4040FC, # Light Blue
    0x00A000, # Dark Green
    0x40FC40, # Light Green
    0x00A0A0, # Dark Cyan
    0x40FFFF, # Light Cyan
    0xA00000, # Dark Red
    0xFF4040, # Light Red
    0xA000A0, # Dark Purple
    0xFF40FF, # Light Purple
    0xA06000, # Dark Yellow
    0xFFFF40, # Light Yellow
    0xA0A0A0, # Dark White
    0xFFFFFF, # Light White
]

def cell_palettes(palette):
    n = len(palette)
    for i in range(n):
        for j in range(i+1, n):
            yield hitherdither.palette.Palette([palette[i], palette[j]])

def sRGB_to_Lab(srgb):
    return colour.XYZ_to_Lab(colour.sRGB_to_XYZ(srgb))

def image_to_Lab(image):
    srgb = numpy.array(image)
    srgb = srgb.reshape(-1, 3)*(1/256)
    return sRGB_to_Lab(srgb)

def dithers(palettes, cell):
    for i, palette in enumerate(palettes):
        dith = hitherdither.ordered.yliluoma.yliluomas_1_ordered_dithering(
            cell, palette, order=8)
        yield dith

blur_filter = ImageFilter.BoxBlur(radius = 1)

def image_diff(orig_lab, new):
    new_lab = image_to_Lab(new.convert('RGB').filter(blur_filter))
    delta_E = colour.delta_E(cell_lab, new_lab)
    scalar_diff = (delta_E ** 2).sum(0)
    return scalar_diff

CELL_W = 8
CELL_H = 8

palettes = tuple(cell_palettes(CGA_PALETTE))

in_fnam, out_fnam = sys.argv[1:]

img = Image.open(in_fnam)
out = img.copy()

for y in range(0, img.height, CELL_H):
    for x in range(0, img.width, CELL_W):
        cell = img.crop((x, y, x + CELL_W, y + CELL_H))
        cell_lab = image_to_Lab(cell)
        best_dith = min(dithers(palettes, cell),
                key=lambda dith: image_diff(cell_lab, dith))
        out.paste(best_dith, (x, y))
        print(x, y)
    out.show()

out.save(out_fnam)
