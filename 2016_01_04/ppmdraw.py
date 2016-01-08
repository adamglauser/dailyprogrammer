# /r/dailyprogrammer easy challenge 2016-01-04

# The task is to read a file with instructions for creating various shapes
# on a canvas. The output should be a .ppm image file containing those shapes
# on a black background.
import pdb

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
		print('{0:3d} {1:3d} {2:3d}'.format(self.r, self.g, self.b), end="")

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
		# drawing "backward" to simplify determination of next point to draw
		if (self.origin.y <= self.end.y):
			self.drawBySlope(canvas, None, self.origin, self.end)
		else:
			self.drawBySlope(canvas, None, self.end, self.origin)

	# A line drawing algorithm of my own design
        # For simplicity, assumes that startPoint.y <= endPoint.y
        #   Lines for which this is not true can simply be drawn in reverse
        # Start by drawing the start point of the line
        #   Unless we are at or adjacent to the end point, pick the next
        #   point by minimizing the difference between the slope of what we've drawn so far
        #   and the slope of the desired line
	def drawBySlope(self, canvas, slope, startPoint, endPoint):
		canvas.setPoint(startPoint, self.colour)
		if (startPoint == endPoint):
			return

		# if the startPoint is adjacent to the end point, we can just
		#  fill in the end point and be done
		if (Canvas.areAdjacent(startPoint, endPoint)):
			canvas.setPoint(endPoint, self.colour)
			return

		# horizontal and vertical lines are easy
		slope = Line.getSlope(self.origin, self.end)
		xDirection = 1 if startPoint.x <= self.end.x else -1
		if (slope == 0):
			nextPoint = Coordinate(startPoint.x + xDirection, startPoint.y)
			self.drawBySlope(canvas, slope, nextPoint, endPoint)
			return
		if (slope == None):
			nextPoint = Coordinate(startPoint.x, startPoint.y + 1) 
			self.drawBySlope(canvas, slope, nextPoint, endPoint)
			return

		# in case we don't quite hit the end point, abort if line goes 
                #  past end point to avoid infinite loop
		if ((xDirection > 0 and startPoint.x > endPoint.x) 
				or (xDirection < 0 and startPoint.x < endPoint.x) 
				or (startPoint.y > endPoint.y) 
				):
			self.drawBySlope(canvas, slope, endPoint, endPoint)
			return

		# depending on the quadrant the line is in, only three possible points could be next on the line
		# figure out which three depending on line direction, then choose the one that will result in a line
		# with the slope closest to the final line
		candidate = (
			Coordinate(startPoint.x, startPoint.y + 1),
			Coordinate(startPoint.x + xDirection, startPoint.y),
			Coordinate(startPoint.x + xDirection, startPoint.y + 1))

		closestSlope = None
		closestCandidateIndex = None
		newSlope = [0, 0, 0] 
		for i in range(len(candidate)):
			newSlope[i] = Line.getSlope(self.origin, candidate[i])
			if (closestSlope is None or abs(newSlope[i] - slope) < abs(closestSlope - slope)):
				closestSlope = newSlope[i]
				closestCandidateIndex = i
		else:
			self.drawBySlope(canvas, slope, candidate[closestCandidateIndex], endPoint)
		
	@staticmethod
	def getSlope(p1, p2):
		if not(isinstance(p1, Coordinate)) or not(isinstance(p2, Coordinate)):
			#error
			return None

		if (p2.x == p1.x):
			slope = None 
		else:
			slope = (p2.y - p1.y) / (p2.x - p1.x)

		return slope

class Rectangle(Shape):
	def __init__(self, origin, height, width, colour):
		super(Rectangle, self).__init__(origin, colour)
		self.height = height
		self.width = width

	def draw(self, canvas):
		for i in range(self.height):
			Line(Coordinate(self.origin.x + i, self.origin.y), Coordinate(self.origin.x + i, self.origin.y + self.width - 1), self.colour).draw(canvas)

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

	def writePPM(self, eol, colPad):
		print('P3 ', end=eol)
		print('{0:d} {1:d}'.format(len(self.grid[0]), len(self.grid)), end=eol)
		for row in self.grid:
			for col in row:
				col.show()
				print(' ' * colPad, end='')
			if (not (eol == '')):
				print ('', end=eol)

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
	print('')
	print('')

	canvas = Canvas(7, 7)
	testLine = (Line(Coordinate(1,1),Coordinate(1,6),Colour(0,255,0)),Line(Coordinate(0,2),Coordinate(6,2),Colour(0,0,255)),Line(Coordinate(5,4),Coordinate(1,4),Colour(255,0,0)),Line(Coordinate(5,6),Coordinate(5,1),Colour(255,255,0)))
	testLine[0].draw(canvas)
	canvas.show()
	print('')
	print('')

	testLine[1].draw(canvas)
	canvas.show()
	print('')
	print('')

	testLine[2].draw(canvas)
	canvas.show()
	print('')
	print('')

	#pdb.set_trace()
	testLine[3].draw(canvas)
	canvas.show()
	print('')
	print('')

	print('Test diagonal lines')
	canvas = Canvas(20, 20)
	testLine = (
		Line(Coordinate(0,0),Coordinate(19,19),Colour(0,255,0)),
		Line(Coordinate(1,0),Coordinate(17,2),Colour(0,0,255)),
		Line(Coordinate(15,14),Coordinate(3,4),Colour(255,0,0)),
		Line(Coordinate(5,6),Coordinate(0,1),Colour(255,255,0)))
	#pdb.set_trace()
	testLine[0].draw(canvas)
	canvas.show()
	print('')
	print('')

	testLine[1].draw(canvas)
	canvas.show()
	print('')
	print('')

	testLine[2].draw(canvas)
	canvas.show()
	print('')
	print('')

	testLine[3].draw(canvas)
	canvas.show()
	print('')
	print('')

	print('Test rectangles')
	canvas = Canvas(8, 7)
	testLine = (
		Rectangle(Coordinate(0, 0), 2, 2,Colour(0, 255, 0)),
		Rectangle(Coordinate(3, 0), 3, 4, Colour(0, 0, 255)))
	#pdb.set_trace()
	testLine[0].draw(canvas)
	canvas.show()
	print('')
	print('')

	testLine[1].draw(canvas)
	canvas.writePPM('\n', 1)
	canvas.writePPM('', 1)
