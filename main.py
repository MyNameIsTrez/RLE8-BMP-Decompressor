import os
from PIL import Image
from pathlib import Path


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


def get_bmp_pixel_array_offset(img):
	img.seek(0xA)
	# Start of the rle8.bmp example's pixel array: 08 00 03 F8
	return int.from_bytes(img.read(4), byteorder="little")


def get_bmp_pixel_array_byte_size(img):
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
def get_decoded_rle_bmp_pixel_array(rle_bytes):
	width = get_bmp_width(img)
	height = get_bmp_height(img)

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
				decompressed[y].append(0)

		else: # Called "encoded mode" in the MS Docs.
			repeat = byte

			byte_index += 1
			palette_index = rle_bytes[byte_index]

			for _ in range(repeat):
				decompressed[y].append(palette_index)


def get_pixel_array_bytes(img):
	pixel_array_offset = get_bmp_pixel_array_offset(img)
	pixel_array_byte_size = get_bmp_pixel_array_byte_size(img)
	img.seek(pixel_array_offset)
	return img.read(pixel_array_byte_size)


def get_rle_bmp_pixel_array(img):
	pixel_array_bytes = get_pixel_array_bytes(img)
	return get_decoded_rle_bmp_pixel_array(pixel_array_bytes)


def is_png_paletted(img):
	img.seek(0x19)
	return int.from_bytes(img.read(1), byteorder="big") == 3


# print(is_png_paletted("input/regular_rgb_image.png"))
# print(is_png_paletted("input/paletted_rgb_image.png"))


# print(is_png_paletted("output/indexed_image.png"))
# print(is_png_paletted("output/rgb_image.png"))


if __name__ == "__main__":
	for input_parent_folder_path, subfolders, subfiles in os.walk("input"):
		for filename in subfiles:
			input_filepath = Path(input_parent_folder_path) / filename
			with open(input_filepath, "rb") as img:
				# print(get_bmp_compression_method(img))
				if is_bmp_rle8_compressed(img):
					print(input_filepath, get_rle_bmp_pixel_array(img), "\n")
					# get_rle_bmp_pixel_array(img)
					# output_filepath = "output" / Path(*input_filepath.parts[1:]).with_suffix(".png")

					# print(output_filepath, output_filepath.with_suffix(".png"))
					# if is_bmp_indexed(input_filepath):
						# print(filename)

					# Image.open(input_filepath).save(output_filepath)
					# print(output_filepath, is_png_paletted(output_filepath))