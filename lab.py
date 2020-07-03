import sys

from encode import encode
from decode import decode


# The main function basically checks the command line arguments
# and decides to call either the encode or the decode routines.
def main():

	# Check that the necessary command line arguments were provided.
	if len(sys.argv) != 4:
		print('ERROR: incorrect syntax')
		printUsage()
		return -1

	# Store command line arguments for later.
	imgFilename = sys.argv[2]
	msgFilename = sys.argv[3]

	# Decide if we have to encode or decode:
	if sys.argv[1] == '-e':
		print('Encoding...')
		if encode(imgFilename, msgFilename) != 0:
			print('ERROR: there was a problem encoding the message')
			return -1
		else:
			print('Encoding executed correctly')
			return 0
	elif sys.argv[1] == '-d':
		print('Decoding...')
		if decode(imgFilename, msgFilename) != 0:
			print('ERROR: there was a problem decoding the message')
			return -1
		else:
			print('Decoding executed correctly')
			return 0
	else:
		print('ERROR: option "{}" not recognized'.format(sys.argv[1]))
		printUsage()
		return -1


# Prints the correct usage of the application to the screen.
def printUsage():
	print('\nUsage:')
	print('\tpython3 lab.py -[e/d] <img_filename> <msg_filename>\n')

if __name__ == '__main__':
	main()