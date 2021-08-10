# RLE8-BMP-Decompressor

## What is this?

This is a Python program that convert RLE8 compressed BMPs to paletted PNGs.

## How to use this program

Use `py main.py` to convert RLE8 BMPs that are in the `Input` folder to paletted PNGs that will be put in the `Output` folder.
Any files that aren't RLE8 BMPs will be skipped, so if your BMP isn't being converted then it isn't RLE8 compressed.

In the `Tests` folder you'll find BMPs that can be moved to the `Input` folder to verify whether the program still works on a bunch of edge cases.

## Limitations

* If there are offset "Delta" bytes in the RLE8 BMP, this program is currently hardcoded to fill the empty space with palette index 0 values.

* This program won't work for BMPs with palettes that don't have an alpha layer, or that don't have exactly 256 palette colors.

* This program won't decompress RLE4 BMPs, but it should be pretty easy to add this feature. I'd be happy to merge any pull request for it!

I recommend reading [the MS Documentation on bitmaps](https://docs.microsoft.com/en-us/windows/win32/gdi/bitmap-compression) to learn how RLE8 (and RLE4) compression exactly works.