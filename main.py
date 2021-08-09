import os
from PIL import Image
from pathlib import Path
import numpy as np


# def get_bmp_bits_per_pixel(img):
# 	img.seek(0x1C)
# 	return int.from_bytes(img.read(2), byteorder="little")


# def is_bmp_indexed(img):
# 	return get_bmp_bits_per_pixel(img) == 8


# print(is_bmp_indexed("input/rgb_image.bmp"))
# print(is_bmp_indexed("input/indexed_image.bmp"))
# print(is_bmp_indexed("input/actual_rgb_image.png"))


def get_bmp_compression_method(img):
	img.seek(0x1E)
	return int.from_bytes(img.read(4), byteorder="little")


def is_bmp_rle8_compressed(img):
	return get_bmp_compression_method(img) == 1


def get_bmp_pixel_index_array_offset(img):
	img.seek(0xA)
	# Start of the rle8.bmp example's pixel array: 08 00 03 F8
	return int.from_bytes(img.read(4), byteorder="little")


def get_bmp_pixel_index_array_byte_size(img):
	img.seek(0x22)
	return int.from_bytes(img.read(4), byteorder="little")


# def is_image(full_filename):
# 	return full_filename.lower().endswith((".bmp", ".png"))


# def is_bmp(full_filename):
# 	return os.path.splitext(full_filename)[1] == ".bmp"


def get_bmp_width(img):
	img.seek(0x12)
	return int.from_bytes(img.read(2), byteorder="little")


def get_bmp_height(img):
	img.seek(0x16)
	return int.from_bytes(img.read(2), byteorder="little")


# See the MS docs for more information on how the BI_RLE8 decoding works:
# https://docs.microsoft.com/en-us/windows/win32/gdi/bitmap-compression
def get_decoded_pixel_index_array(rle_bytes, width, height):
	decompressed = [[] for _ in range(height)]

	byte_index = -1
	y = height - 1

	while True:
		run_even = True

		byte_index += 1
		byte = rle_bytes[byte_index] # Get the first byte.

		if byte == 0:
			byte_index += 1
			special_byte = rle_bytes[byte_index] # Get the second byte.

			if special_byte == 0:
				y -= 1
			elif special_byte == 1:
				return decompressed
			elif special_byte == 2:
				# TODO: Try to make an example RLE8 BMP with delta by saving a PNG in GIMP to it.
				# TODO: Wait on MS pull request feedback on whether delta goes up or down.
				raise "The RLE8 BMP has a delta byte, but I didn't write code for that yet!"
				pass
			else: # Called "absolute mode" in the MS Docs.
				following = special_byte

				for _ in range(following):
					byte_index += 1
					palette_index = rle_bytes[byte_index]
					decompressed[y].append(palette_index)
					run_even = not run_even

			# Adding padding so each run has an even number of bytes.
			if not run_even:
				byte_index += 1

		else: # Called "encoded mode" in the MS Docs.
			repeat = byte

			byte_index += 1
			palette_index = rle_bytes[byte_index]

			for _ in range(repeat):
				decompressed[y].append(palette_index)


def get_pixel_index_array_bytes(img):
	pixel_index_array_offset = get_bmp_pixel_index_array_offset(img)
	pixel_index_array_byte_size = get_bmp_pixel_index_array_byte_size(img)

	img.seek(pixel_index_array_offset)
	return img.read(pixel_index_array_byte_size)


def get_pixel_array(img, width, height, palette):
	pixel_index_array_bytes = get_pixel_index_array_bytes(img)
	decoded_pixel_index_array = get_decoded_pixel_index_array(pixel_index_array_bytes, width, height)
	return np.array(decoded_pixel_index_array, dtype="uint8")


def is_png_paletted(img):
	img.seek(0x19)
	return int.from_bytes(img.read(1), byteorder="big") == 3


# print(is_png_paletted("input/regular_rgb_image.png"))
# print(is_png_paletted("input/paletted_rgb_image.png"))


# print(is_png_paletted("output/indexed_image.png"))
# print(is_png_paletted("output/rgb_image.png"))


def get_palette(img):
	img.seek(0x36)
	# TODO: This won't work for palettes that don't have an alpha layer or that don't have exactly 256 palette colors.
	palette = list(img.read(4 * 256))
	del palette[3::4] # Removes the alpha values.

	# Swaps the R and B values.
	palette[0:-2:3], palette[2::3] = palette[2::3], palette[0:-2:3]

	return palette


if __name__ == "__main__":
	# Opening an RLE8 BMP with Pillow causes a console error, so instead this code reads the pixels and palette of the RLE8 BMP.
	for input_parent_folder_path, subfolders, subfiles in os.walk("input"):
		for filename in subfiles:
			input_filepath = Path(input_parent_folder_path) / filename
			with open(input_filepath, "rb") as img:
				# print(get_bmp_compression_method(img))
				if is_bmp_rle8_compressed(img):
					width = get_bmp_width(img)
					height = get_bmp_height(img)

					palette = get_palette(img)
					# print(palette)
					
					pixel_array = get_pixel_array(img, width, height, palette)
					
					# print(pixel_array)
					
					img = Image.fromarray(pixel_array, mode="P")
					img.putpalette(palette)

					output_filepath = "output" / Path(*input_filepath.parts[1:]).with_suffix(".png")
					img.save(output_filepath)