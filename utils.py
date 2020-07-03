# Reads data from a file and returns it as a string.
def readStringFromFile(filename):
	try:
		with open(filename, 'r') as file:
			return file.read()
	except Exception as exception:
		print('ERROR: there was a problem opening the file {}'.format(filename))
		print(exception)
		return None
	