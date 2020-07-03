import sys
import math
from PIL import Image

def main():
	# Check that the necessary command line arguments were provided.
	if len(sys.argv) != 3:
		print('ERROR: please use the following syntax:')
		print('> python3 lab.py <filename> <message_string>')
		return -1

	# Store command line arguments for later.
	filename = sys.argv[1]
	messageString = sys.argv[2]

	# Try to open the image.
	try:
		image = Image.open(filename)
	except Exception as exception:
		print('ERROR: the image could not be opened')
		print(exception)
		return -1
	print('Image opened correctly')

	# TODO: if the image is JPEG, first convert it to PNG, as we need a lossless format
	# for the message information not to be lost.

	# Transform the secret message to binary format.
	binaryMessage = stringToBinary(messageString)
	if binaryMessage == None:
		print('ERROR: could not convert the message to binary format')
		return -1
	else:
		print('Message string in binary format: {}'.format(binaryMessage))
	
	# TODO: get some metadata from the image to check the size of the image is enough
	# to store the secret message.
	
	# Get all the pixel values in the image.
	try:
		pixels = list(image.getdata())
	except Exception as exception:
		print('ERROR: could not extract the pixels from the image')
		print(exception)
		return -1
	print('First ten pixels in the input image:')
	for i in range(10):
		print('\t{}'.format(pixels[i]))

	# Modify the pixel list including the message in the least significant bits.
	newPixels = encodeMessageInPixels(pixels, binaryMessage)
	if newPixels == None:
		print('ERROR: there was a problem encoding the message inside the image')
		return -1
	else:
		print('Message encoded correctly inside the image')
		print('First ten pixels of the encoded image:')
		for i in range(10):
			print('\t{}'.format(newPixels[i]))
	
	# Create the new image with the new values and export it.
	encodedImage = Image.new(image.mode, image.size)
	encodedImage.putdata(newPixels)
	encodedImage.save('encoded.png')

	return 0


# Append the indicators of beginning and end of string for decoding, then transform
# into a list where each value is the binary representation of a byte in the original
# string, using utf-8 as the encoder.
def stringToBinary(string):

	# Add the delimiters of the string.
	finalString = '$$$$$' + string + '$$$$$'
	
	# Get a list of bytes encoding the string in utf-8.
	byteString = bytearray(finalString, encoding='utf-8')

	# Join all those bytes in one big string of only zeros and ones.
	return ''.join([format(byte, '08b') for byte in byteString])


# Receives the list of pixels, flattened, found in the original image,
# and the string encoded in binary format. It then modifies the least significant
# bit of each value of each pixel to store the message.
def encodeMessageInPixels(pixels, binaryMessage):

	# Variable to store the new pixel values.
	newPixels = []

	# Index for the current 0 or 1 in the binary message and length of the message.
	currentIndex = 0
	messageLen = len(binaryMessage)

	# Iterate over all the pixels in the original image (flattened).
	for pixel in pixels:

		# Declare a new pixel.
		newPixel = ()

		# A pixel can have several values, 1 value in Black and White format,
		# three values in RGB format. For us, this is not important, we iterate over
		# all possible values inside the pixel.
		for value in pixel:

			if currentIndex < messageLen:
				newPixel += (math.floor(value / 2) * 2 + int(binaryMessage[currentIndex], 2), )
				currentIndex += 1
			else:
				newPixel += (value, )
		
		newPixels.append(newPixel)
	
	return newPixels

if __name__ == '__main__':
	main()
