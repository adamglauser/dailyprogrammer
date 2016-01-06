# /r/dailyprogrammer easy challenge 2016-01-04

# The task is to read a file with instructions for creating various shapes
# on a canvas. The output should be a .ppm image file containing those shapes
# on a black background.

class Coordinate(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Colour(object):
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b

class Shape(object):
	def __init__(self, origin, colour):
		self.origin = origin
		self.colour = colour

	def draw(self):
		print("Shape")

class Point(Shape):
	def draw(self):
		print('A {0:d},{1:d},{2:d} point at {3:d},{4:d}.'.format(self.colour.r,self.colour.g,self.colour.b,self.origin.x, self.origin.y))

if __name__ == '__main__':
	testPoint = Point(Coordinate(5,5),Colour(255,0,0))
	testPoint.draw()
