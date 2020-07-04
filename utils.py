from PIL import Image

# Define the beginning and end format tokens.
FORMAT_TOKEN = '$$$$$'

# Reads data from a file and returns it as a string.
def readStringFromFile(filename):
	try:
		with open(filename, 'r') as file:
			return file.read()
	except Exception as exception:
		print(exception)
		return None

# Writes a string into a file.
def writeStringToFile(string, filename):
	try:
		with open(filename, 'w') as file:
			file.write(string)
			return 0
	except Exception as exception:
		print(exception)
		return -1

# Opens an image object from file and returns it.
def openImage(filename):
	try:
		return Image.open(filename)
	except Exception as exception:
		print(exception)
		return None

# Extracts pixels from the provided image.
def extractPixelsFromImage(image):
	try:
		return list(image.getdata())
	except Exception as exception:
		print(exception)
		return None