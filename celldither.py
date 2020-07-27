#!/usr/local/bin/python3

from PIL import Image
import hitherdither
import numpy

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

img = Image.open('kodim23.png')

# img_dithered = hitherdither.ordered.bayer.bayer_dithering(
#     img, palette, 0, order=8)
cell = img.crop((0,0,8,8))
cell_srgb = numpy.array(cell).reshape(-1, 3)
print(cell_srgb)
# TODO: convert to lab

palettes = tuple(cell_palettes(CGA_PALETTE))
for i, palette in enumerate(palettes):
    img_dithered = hitherdither.ordered.yliluoma.yliluomas_1_ordered_dithering(
        cell, palette, order=8)
    # TODO: convert to array
    # TODO: convert to lab
    # TODO: get delta_E with cell_lab
    # TODO: compute sum of squares
    # TODO: pick best dither by sum of squares of delta_E
    # TODO: assemble each best dither into output image




