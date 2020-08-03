#!/bin/bash

set -eux

# Converts single image into 4 images for examples:
# - image-scaled.png - scaled and aspect-adjusted to 640x200
# - image-scaled-pereview.png - previous image un-aspect-adjusted
# - image-dithered.png - dithered
# - image-scaled-pereview.png - previous image un-aspect-adjusted

basename=${1%.*} # remove extension

convert -scale '100%x41.666%' -resize '640x200' "$1" "$basename"-scaled.png
convert -scale '100%x240%' "$basename"-scaled.png "$basename"-scaled-preview.png
time ../dithersaurus.py "$basename"-scaled.png "$basename"-dithered.png
convert -scale '100%x240%' "$basename"-dithered.png "$basename"-dithered-preview.png
