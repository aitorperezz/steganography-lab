import math
from PIL import Image

import utils

# Reads an image from imgFilename and a text from msgFilename and encodes
# the text inside the image using Least Significant Bit Steganography.
# The output image is called 'encoded.png' and stored at the working directory.
def encode(imgFilename, msgFilename):

	# Open the image.
	image = utils.openImage(imgFilename)
	if image == None:
		utils.log('ERROR: could not open the image')
		return -1
	else:
		utils.log('Image opened correctly')

	# TODO: if the image is JPEG, first convert it to PNG, as we need a lossless format
	# for the message information not to be lost.

	# Get the string inside the provided message file.
	stringMessage = utils.readStringFromFile(msgFilename)
	if stringMessage == None:
		utils.log('ERROR: there was a problem reading the message from the provided file')
		utils.log('Provided message file: {}'.format(msgFilename))
		return -1
	else:
		utils.log('Message read from file:')
		utils.log('{}'.format(stringMessage))

	# Transform the secret message to binary format.
	binaryMessage = stringToBinary(stringMessage)
	if binaryMessage == None:
		utils.log('ERROR: could not convert the message to binary format')
		return -1
	else:
		utils.log('Message converted to binary format:')
		utils.log('{}'.format(binaryMessage))
	
	# TODO: get some metadata from the image to check the size of the image is enough
	# to store the secret message.

	# Get all the pixel values in the image.
	pixels = utils.extractPixelsFromImage(image)
	if pixels == None:
		utils.log('ERROR: could not extract pixels from image')
		return -1
	else:
		utils.log('Pixels extracted from image')
	utils.log('First ten pixels in the input image:')
	for i in range(10):
		utils.log('\t{} -> {}'.format(i, pixels[i]))

	# Get a new pixel list where the message is encoded in the least significant bits.
	newPixels = encodeMessageInPixels(pixels, binaryMessage)
	if newPixels == None:
		utils.log('ERROR: there was a problem encoding the message inside the image')
		return -1
	else:
		utils.log('Message encoded correctly inside the image')
		utils.log('First ten pixels of the encoded image:')
		for i in range(10):
			utils.log('\t{} -> {}'.format(i, newPixels[i]))
	
	# Create the new image with the new pixel values and export it.
	encodedImage = Image.new(image.mode, image.size)
	encodedImage.putdata(newPixels)
	encodedImage.save('encoded.png')

	return 0


# Appends the format tokens to the beginning and end of the string, then gets
# the binary representation of the string using utf-8 as the encoder. Returns a string
# of only '0' and '1' characters.
def stringToBinary(string):

	# Add format tokens to the string and transform into a byte array.
	byteList = bytearray(utils.FORMAT_TOKEN + string + utils.FORMAT_TOKEN, encoding='utf-8')

	# Join all those bytes in one big string of only 0 and 1 chars, like '0110101'.
	return ''.join([format(byte, '08b') for byte in byteList])


# Receives the list of pixels, flattened, found in the original image,
# and the string encoded in binary format. It then modifies the least significant
# bit of each value of each pixel to store the message.
def encodeMessageInPixels(pixels, binaryMessage):

	# A list to store the new pixel values.
	newPixels = []

	# Current position inside the binary message, and length of the message.
	currentIndex = 0
	messageLen = len(binaryMessage)

	# Iterate over all the pixels in the original image.
	for pixel in pixels:

		# If the pixel is iterable (a tuple), go through all its values.
		if type(pixel) == tuple:
			newPixel = ()
			for value in pixel:
				newPixel += (newPixelValue(value, binaryMessage, currentIndex, messageLen), )
				currentIndex += 1
		
		# If the pixel is not iterable, get only one new value.
		elif type(pixel) == int:
			newPixel = newPixelValue(pixel, binaryMessage, currentIndex, messageLen)
			currentIndex += 1
		
		# If the pixel is of any other type, return with error.
		else:
			utils.log('ERROR: unexpected pixel type: {}'.format(type(pixel)))
			return None

		# Get the new pixel inside the growing list of pixels.
		newPixels.append(newPixel)
	
	return newPixels


# Receives the current value inside a pixel and a binary message, and tries to
# modify the LSB of the value to store the next bit of the message.
# If the binary message has already been consumed, it just returns the value itself.
def newPixelValue(value, binaryMessage, currentIndex, messageLen):

	if currentIndex < messageLen:
		return math.floor(value / 2) * 2 + int(binaryMessage[currentIndex], 2)
	else:
		return value