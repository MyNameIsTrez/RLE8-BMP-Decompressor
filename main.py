import os

from pathlib import Path


import bmp_to_png


def main():
	# Opening an RLE8 BMP with Pillow causes a console error, so instead this code reads the pixels and palette of the RLE8 BMP.
	for input_parent_folder_path, subfolders, subfiles in os.walk("Input"):
		for filename in subfiles:
			if bmp_to_png.is_bmp(filename):
				input_filepath = Path(input_parent_folder_path) / filename
				with open(input_filepath, "rb") as img:
					if bmp_to_png.is_bmp_rle8_compressed(img):
						bmp_to_png.convert_rle8_bmp_to_png(img, input_filepath, "Output")


if __name__ == "__main__":
	main()
