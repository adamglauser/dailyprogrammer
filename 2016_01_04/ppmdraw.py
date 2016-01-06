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
		self.drawBySlope(canvas, None, self.origin)

	def drawBySlope(self, canvas, slope, startPoint):
		canvas.setPoint(startPoint, self.colour)
		slope = Line.getSlope(self.origin, self.end)
		if (startPoint == self.end):
			canvas.setPoint(startPoint, self.colour)
			return

		# if the startPoint is adjacent to the end point, we can just
		#  fill it in then draw a line on the end point
		if (Canvas.areAdjacent(startPoint, self.end)):
			self.drawBySlope(canvas, slope, self.end)
			return

		# horizontal and vertical lines are easy
		if (slope == 0):
			direction = 1 if startPoint.x <= self.end.x else -1
			nextPoint = Coordinate(startPoint.x + direction, startPoint.y)
			self.drawBySlope(canvas, slope, nextPoint)
			return
		if (slope == None):
			yDirection = 1 if startPoint.y <= self.end.y else -1
			nextPoint = Coordinate(startPoint.x, startPoint.y + yDirection) 
			self.drawBySlope(canvas, slope, nextPoint)
			return


		# depending on the quadrant the line is in, only three possible points could be next on the line
		# figure out which three depending on line direction, then choose the one that will result in a line
		# with the slope closest to the final line
		xDirection = 1 if startPoint.x <= self.end.x else -1
		yDirection = 1 if startPoint.y <= self.end.y else -1
		candidate = (Coordinate(startPoint.x, startPoint.y + yDirection),Coordinate(startPoint.x + xDirection, startPoint.y),Coordinate(startPoint.x + xDirection, startPoint.y + yDirection))

		closestSlope = None
		closestCandidateIndex = None
		newSlope = [0, 0, 0] 
		for i in range(len(candidate)):
			newSlope[i] = Line.getSlope(self.origin, candidate[i])
			if (closestSlope is None or abs(newSlope[i] - slope) < abs(closestSlope - slope)):
				closestSlope = newSlope[i]
				closestCandidateIndex = i

		# in case my algorithm doesn't work well, to avoid infinite loop
		if ((xDirection > 0 and candidate[closestCandidateIndex].x > self.end.x) 
				or (xDirection < 0 and candidate[closestCandidateIndex].x < self.end.x) 
				or (yDirection > 0 and candidate[closestCandidateIndex].y > self.end.y) 
				or (yDirection < 0 and candidate[closestCandidateIndex].y < self.end.y)
				):
			self.drawBySlope(canvas, slope, self.end)
		else:
			self.drawBySlope(canvas, slope, candidate[closestCandidateIndex])
		
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
