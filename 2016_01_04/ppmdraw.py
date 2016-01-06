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

	def show(self):
		print('{0:3d} {1:3d} {2:3d}'.format(self.r, self.b, self.g), end="")

class Shape(object):
	def __init__(self, origin, colour):
		self.origin = origin
		self.colour = colour

	def draw(self):
		print("Shape")

class Point(Shape):
	def draw(self, canvas):
		canvas.setPoint(self.origin, self.colour)

class Canvas(object):
	def __init__(self, col, row):
		self.grid = [[Colour(0,0,0) for x in range(col)] for x in range(row)]

	def setPoint(self, point, colour):
		self.grid[point.x][point.y] = colour

	def show(self):
		for row in self.grid:
			for col in row:
				col.show()
				print('   ', end="")
			print('')

if __name__ == '__main__':
	canvas = Canvas(2,2)
	testPoint = Point(Coordinate(0,1),Colour(255,0,0))
	testPoint.draw(canvas)
	canvas.show()
