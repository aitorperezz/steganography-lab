import utils


# Opens the image provided at imgFilename and looks for a hidden message inside
# the Least Significant Bits of each pixel value. If a properly formatted secret message 
# is found, it is written to msgFilename.
def decode(imgFilename, msgFilename):

	# Open the image.
	image = utils.openImage(imgFilename)
	if image == None:
		print('ERROR: could not open the image')
		return -1
	else:
		print('Image opened correctly')

	# Extract the pixels inside the image.
	pixels = utils.extractPixelsFromImage(image)
	if pixels == None:
		print('ERROR: could not extract pixels from image')
		return -1
	else:
		print('Pixels extracted from image')
	
	# Extract the binary data in the LSB of the provided pixels.
	binaryString = extractBinaryMessageFromPixels(pixels)

	# Get the string of the secret message, if there is one.
	secretMessage = extractSecretMessage(binaryString)
	if secretMessage == None:
		print('ERROR: no secret message was found inside the image')
		return -1
	else:
		print('Secret message found inside the image:')
		print('{}'.format(secretMessage))
	
	# Finally, store the secret message inside the requested file.
	if utils.writeStringToFile(secretMessage, msgFilename) != 0:
		print('ERROR: could not write secret message to file {}'.format(msgFilename))
		return -1
	else:
		print('Secret message written to file')
	
	return 0


# Receives the list of pixels inside the suspected image and extracts the binary values
# of the least significant bits of each value of each pixel, into a string.
def extractBinaryMessageFromPixels(pixels):

	# Create an empty string to store the zeros and ones that we find inside the image.
	binaryData = ''

	# Loop through all pixels and values inside the pixels.
	for pixel in pixels:
		binaryData += ''.join(['0' if value % 2 == 0 else '1' for value in pixel])
	
	return binaryData


# Looks for the format tokens at the beginning and end of a suspected message. If found, returns the string
# representing the message itself.
def extractSecretMessage(binaryString):

	# First convert the binary string into a byte array.
	byteArray = bytes(int(binaryString[i : i + 8], 2) for i in range(0, len(binaryString), 8))

	# Create the binary representation of the format tokens.
	binaryToken = utils.FORMAT_TOKEN.encode('utf-8')

	# Try to find the format token at the beginning of the byte array.
	if not byteArray[0:len(binaryToken)] == binaryToken:
		print('ERROR: the binary stream does not start with the expected "$$$$$" token')
		return None
	
	# Discard the beginning.
	byteArray = byteArray[len(binaryToken):]

	# Try to find again the same sequence that marks the end of the message.
	if not binaryToken in byteArray:
		print('ERROR: the binary stream does not end with the expected "$$$$$" token')
		return None
	
	# Discard the token at the end.
	byteArray = byteArray[0:byteArray.find(binaryToken)]
	
	# Finally, try to decode the byte array into a string using utf-8 as the encoder.
	try:
		return byteArray.decode('utf-8')
	except Exception as exception:
		print(exception)
		print('ERROR: could not decode the byte stream of the secret message')
		return None
