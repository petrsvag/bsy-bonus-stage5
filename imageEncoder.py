import cv2
import base64
import numpy as np
from io import BytesIO

class ImageEncoder():
	markdown_image_start = "data:image/png;base64,"
	message_stop_indicator = "====="
	@staticmethod
	def to_bin( data):
		"""Convert `data` to binary format as string"""
		if isinstance(data, str):
			return ''.join([ format(ord(i), "08b") for i in data ])
		elif isinstance(data, bytes):
			return ''.join([ format(i, "08b") for i in data ])
		elif isinstance(data, np.ndarray):
			return [ format(i, "08b") for i in data ]
		elif isinstance(data, int) or isinstance(data, np.uint8):
			return format(data, "08b")
		else:
			raise TypeError("Type not supported.")


	@staticmethod
	def encode(image_name, secret_data):
		# read the image
		image = cv2.imread(image_name)
		# maximum bytes to encode
		n_bytes = image.shape[0] * image.shape[1] * 3 // 8
		print("[*] Maximum bytes to encode:", n_bytes)
		if len(secret_data) > n_bytes:
			raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
		print("[*] Encoding data...")
		# add stopping criteria
		secret_data += ImageEncoder.message_stop_indicator
		data_index = 0
		# convert data to binary
		binary_secret_data = ImageEncoder.to_bin(secret_data)
		# size of data to hide
		data_len = len(binary_secret_data)
		for row in image:
			for pixel in row:
				# convert RGB values to binary format
				r, g, b = ImageEncoder.to_bin(pixel)
				# modify the least significant bit only if there is still data to store
				if data_index < data_len:
					# least significant red pixel bit
					pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
					data_index += 1
				if data_index < data_len:
					# least significant green pixel bit
					pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
					data_index += 1
				if data_index < data_len:
					# least significant blue pixel bit
					pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
					data_index += 1
				# if data is encoded, just break out of the loop
				if data_index >= data_len:
					break
		return image

	@staticmethod
	def decode(image_name):
		print("[+] Decoding...")
		# read the image
		image = cv2.imread(image_name)
		if not image:
			raise ValueError("[!] Wrong path to file.")
		binary_data = ""
		for row in image:
			for pixel in row:
				r, g, b = ImageEncoder.to_bin(pixel)
				binary_data += r[-1]
				binary_data += g[-1]
				binary_data += b[-1]
		# split by 8-bits
		all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
		# convert from bits to characters
		decoded_data = ""
		for byte in all_bytes:
			decoded_data += chr(int(byte, 2))
			if decoded_data[-5:] == ImageEncoder.message_stop_indicator:
				break
		return decoded_data[:-5]

	@staticmethod
	def decodeFromBase64(image):
		# read the image
		img_decoded = base64.b64decode(image)
		nparr = np.fromstring(img_decoded, np.uint8)
		image = cv2.imdecode(nparr, cv2.IMREAD_COLOR )
		binary_data = ""
		for row in image:
			for pixel in row:
				r, g, b = ImageEncoder.to_bin(pixel)
				binary_data += r[-1]
				binary_data += g[-1]
				binary_data += b[-1]
		# split by 8-bits
		all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
		# convert from bits to characters
		decoded_data = ""
		for byte in all_bytes:
			decoded_data += chr(int(byte, 2))
			if decoded_data[-5:] == ImageEncoder.message_stop_indicator:
				break
		return decoded_data[:-5]

	@staticmethod
	def imageToBase64(image):
		_, buffer = cv2.imencode('.png', image)
		jpg_as_text = base64.b64encode(buffer)
		return jpg_as_text.decode()




if __name__ == "__main__":
	import os
	os.getlogin()

	input_image = ".\\images\\pen_lightbulb.png"
	output_image = "encoded_image.PNG"
	secret_data = "This is a top secret message."
	# encode the data into the image
	encoded_image = ImageEncoder.encode(image_name=input_image, secret_data=secret_data)
	# save the output image (encoded image)
	base64_txt = ImageEncoder.imageToBase64(encoded_image)
	res = ImageEncoder.decodeFromBase64(base64_txt)


	# cv2.imwrite(output_image, encoded_image)
	# decode the secret data from the image
	decoded_data = ImageEncoder.decode(output_image)
	print("[+] Decoded data:", decoded_data)