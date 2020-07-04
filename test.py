import unittest
from filecmp import cmp

from encode import encode
from decode import decode
import utils


# Test everything related to PNG images.
class TestPNGImages(unittest.TestCase):

	# Test RGB and RGBA images, PNG format.
	def testRGBImages(self):
		utils.silent = True
		decode('test_files/png16rgba.png', 'test_files/message1.txt')
		decode('encoded.png', 'secret.txt')
		self.assertTrue(cmp('test_files/message1.txt', 'secret.txt'))
		decode('test_files/png16rgb.png', 'test_files/message1.txt')
		decode('encoded.png', 'secret.txt')
		self.assertTrue(cmp('test_files/message1.txt', 'secret.txt'))
		decode('test_files/png8rgb.png', 'test_files/message1.txt')
		decode('encoded.png', 'secret.txt')
		self.assertTrue(cmp('test_files/message1.txt', 'secret.txt'))
		decode('test_files/pngHDrgba.png', 'test_files/message1.txt')
		decode('encoded.png', 'secret.txt')
		self.assertTrue(cmp('test_files/message1.txt', 'secret.txt'))

	# Test Black and White images, PNG format.
	def testBWImages(self):
		utils.silent = True
		decode('test_files/png8l.png', 'test_files/message1.txt')
		decode('encoded.png', 'secret.txt')
		self.assertTrue(cmp('test_files/message1.txt', 'secret.txt'))
	
	# TODO: test really big message files on small and big images.

	# TODO: test messages with strange characters.

# Test all of the above, but with JPEG images.

if __name__ == '__main__':
	unittest.main()