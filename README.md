# RLE8-BMP-Decompressor

A Python program that convert RLE8 compressed BMPs to paletted PNGs.

Note that if there are offset "Delta" bytes in the RLE8 BMP this program will fill these pixels with palette index 0 values.