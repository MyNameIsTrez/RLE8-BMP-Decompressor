# RLE8-BMP-Decompressor

## What is this?

A Python program that convert RLE8 compressed BMPs to paletted PNGs.

## Limitations

* If there are offset "Delta" bytes in the RLE8 BMP, this program is currently hardcoded to fill the empty space with palette index 0 values.

* This program won't work for BMPs with palettes that don't have an alpha layer, or that don't have exactly 256 palette colors.

* This program won't decompress RLE4 BMPs, but it should be pretty easy to add this feature. I'd be happy to merge any pull request for it!

I recommend reading [the MS Documentation on bitmaps](https://docs.microsoft.com/en-us/windows/win32/gdi/bitmap-compression) to learn how RLE8 (and RLE4) compression exactly works.