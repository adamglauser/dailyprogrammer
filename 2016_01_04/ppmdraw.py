# /r/dailyprogrammer easy challenge 2016-01-04

# The task is to read a file with instructions for creating various shapes
# on a canvas. The output should be a .ppm image file containing those shapes
# on a black background.

class Coordinate(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):
		if type(other) is type(self):
			return other.__dict__ == self.__dict__
		return False

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

class Line(Shape):
	def __init__(self, origin, end, colour):
		super(Line, self).__init__(origin, colour)
		self.end = end

	def draw(self, canvas):
		if (self.end.x == self.origin.x):
			slope = 1
		else:
			slope = (self.end.y - self.origin.y) / (self.end.x - self.origin.x)
		self.drawBySlope(canvas, slope, self.origin)

	def drawBySlope(self, canvas, slope, startPoint):
		if (startPoint == self.end):
			canvas.setPoint(startPoint, self.colour)
			return

		# if the startPoint is adjacent to the end point, we can just
		#  fill it in then draw a line on the end point
		if (Canvas.areAdjacent(startPoint, self.end)):
			canvas.setPoint(startPoint, self.colour)
			self.drawBySlope(canvas, slope, self.end)
			return

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

	@staticmethod
	def areAdjacent(p1, p2):
		if not(isinstance(p1, Coordinate)) or not(isinstance(p2, Coordinate)):
			return False
		if abs(p1.x - p2.x) <= 1 and abs(p1.y - p2.y) <= 1:
			return True
		return False

if __name__ == '__main__':
	canvas = Canvas(3,3)
	testPoint = Point(Coordinate(0,1),Colour(255,0,0))
	testPoint.draw(canvas)
	canvas.show()
	print('')
	print('')

	testLine = (Line(Coordinate(1,1),Coordinate(1,1),Colour(0,255,0)),Line(Coordinate(2,0),Coordinate(2,1),Colour(0,0,255)))
	testLine[0].draw(canvas)
	canvas.show()
	print('')
	print('')

	testLine[1].draw(canvas)
	canvas.show()
