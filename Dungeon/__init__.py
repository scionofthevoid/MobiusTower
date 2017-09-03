import math, random
import operator


from Dungeon.Components.Sets.CoordinateSet import CoordinateSet
from Dungeon.Components.Sets.CoordinateSubset import CoordinateSubset

from Dungeon.Components.CardinalDirection import Direction


# Define maze property constants
DEFAULT = ' '
WALL = 'W'
ROOM = 'R'
DOOR = 'D'
LOCKED = 'L'
ITEM = '?'
DEAD_ZONE = 'X'
DOWN_STAIRS = 'v'
UP_STAIRS = '^'
PATH = '█'


'''
The Dungeon
'''
class Dungeon(object):
	def __init__(self, x_dim, y_dim):
		self._xDim = x_dim
		self._yDim = y_dim
		
		'''
		Used for building the dungeon
		'''
		self.__assets = {
			'available': CoordinateSet()
		}

		# Generate a default dungeon (no assets)
		self._dungeon = [DEFAULT] * x_dim
		for x in range(0, x_dim):
			self._dungeon[x] = [DEFAULT] * y_dim

			for y in range(0, y_dim):
				self.__assets['available'].add([x, y])
		
		'''
		Dungeon defaults
		'''
		# Room placement tries
		self._tryPlaceRoom = 50
		self._maxRoomAmount = 20
		
		# Room size
		self._roomMinX = 2
		self._roomMaxX = 8
		self._roomMinY = 2
		self._roomMaxY = 8
	
	@classmethod
	def fromMap(cls, mapfile):
		f, lines = open(mapfile, 'r'), f.readlines()
		
		x_dim, y_dim = len(lines[0]), len(lines)
		dungeon = cls(x_dim, y_dim)
		
		for x in range(0, x_dim):
			for y in range(0, y_dim):
				dungeon._dungeon[x][y] = lines[y][x]

				if lines[y][x] == DEFAULT:
					dungeon.__assets['available'].add([x, y])
		
		f.close()
	
	
	'''
	Set generator parameters
	'''
	def setRoomSize(self, **kwargs):
		for key, value in kwargs.items():
			if key == 'minX':
				self._roomMinX = value if value > 0 and value < self._xDim else self._roomMinX
			elif key == 'maxX':
				self._roomMaxX = value if value > 0 and value < self._xDim else self._roomMaxX
			elif key == 'minY':
				self._roomMinY = value if value > 0 and value < self._yDim else self._roomMinY
			elif key == 'maxY':
				self._roomMaxY = value if value > 0 and value < self._yDim else self._roomMaxY
	
	def setNumTries(self, num_tries):
		if num_tries > 0:
			self._tryPlaceRoom = num_tries

	def setRoomAmount(self, room_amount):
		if room_amount > 0:
			self._maxRoomAmount = room_amount
	
	
	'''
	Generate a dungeon
	'''
	# Add rooms to the dungeon
	# Chance to randomly place rooms right next to other rooms to "extend" them with probability @bias
	def createRooms(self, bias = 0.5):
		tries, numRooms = 0, 0
		
		while tries < self._tryPlaceRoom and numRooms < self._maxRoomAmount:
			x, y = random.randrange(1, self._xDim), random.randrange(1, self._yDim)
			
			# Continue if the coordinate is in bounds
			if x + self._roomMinX < self._xDim - 1 and y + self._roomMinY < self._yDim - 1:
				try:
					roomX = random.randrange(self._roomMinX, min(self._roomMaxX, self._xDim - 1 - x))
					roomY = random.randrange(self._roomMinY, min(self._roomMaxY, self._yDim - 1 - y))
					
					# Check for overlap
					overlap = False
					for xCoord in range(x - (0 if random.random() < bias else 1), x + roomX + 1 + (0 if random.random() < bias else 1)):
						for yCoord in range(y - (0 if random.random() < bias else 1), y + roomY + 1 + (0 if random.random() < bias else 1)):
							overlap = overlap or self._isOccupied(tuple([xCoord, yCoord]))
							
							if overlap:
								break
						
						if overlap:
							break
					
					# Create the room
					if not overlap:
						for xCoord in range(x, x + roomX + 1):
							for yCoord in range(y, y + roomY + 1):
								self._dungeon[xCoord][yCoord] = ROOM
						numRooms += 1
				except ValueError:
					# Not enough space to add a room
					pass
				finally:
					# End of current attempt
					tries += 1
	
	# Add a corridor maze using a "growing tree" algorithm
	# param@bias indicates whether the algorithm will look like a recursive backtracker (> 0.5) or Prim's algorithm (< 0.5)
	def createMaze(self, bias = 1.0):
		# Enqueue cells to check
		cells = [self._getStart()]

		while len(cells) > 0:
			# Select the next index, randomly deciding between first or last
			useCell = int(len(cells) * random.uniform(bias, 1.0)) if bias < 1.0 else len(cells) - 1

			# Find all valid directions
			nextCells = []
			srcCell = cells[useCell]

			self._addToWorkingSet(nextCells, srcCell, 'n')
			self._addToWorkingSet(nextCells, srcCell, 'e')
			self._addToWorkingSet(nextCells, srcCell, 's')
			self._addToWorkingSet(nextCells, srcCell, 'w')

			# Randomly pick a direction
			while len(nextCells) > 0:
				destCell = nextCells.pop(random.randrange(0, len(nextCells)))
				direction = Direction.getKey(tuple(map(operator.sub, destCell, srcCell)))

				# Place a WALL instead of a PATH if the cell is surrounded
				if self._isSurrounded(destCell, direction):
					self._dungeon[destCell[0]][destCell[1]] = WALL
				else:
					self._dungeon[destCell[0]][destCell[1]] = PATH

					# Go backwards and set the left and right WALLs (if possible) for the previous cell
					srcLeft = Direction.moveFrom(srcCell, Direction.turnLeftAsKey(direction))
					if self._isInBounds(srcLeft) and not self._isOccupied(srcLeft):
						self._dungeon[srcLeft[0]][srcLeft[1]] = WALL

					srcRight = Direction.moveFrom(srcCell, Direction.turnRightAsKey(direction))
					if self._isInBounds(srcRight) and not self._isOccupied(srcRight):
						self._dungeon[srcRight[0]][srcRight[1]] = WALL

					# Enqueue the cell and exit the loop
					cells.append(destCell)
					break

			if len(nextCells) == 0:
				cells.pop(useCell)


	'''
	Maze generator utilities
	'''
	# Randomly select a starting point, ensuring that the location selected is DEFAULT
	def _getStart(self):
		start = None
		valid = (not start == None)

		while not valid:
			start = [random.randrange(0, self._xDim), random.randrange(0, self._yDim)]

			valid = (not start == None) and not self._isOccupied(start) \
					and not self._isOccupied(Direction.moveFrom(start, 'n')) \
					and not self._isOccupied(Direction.moveFrom(start, 'e')) \
					and not self._isOccupied(Direction.moveFrom(start, 's')) \
					and not self._isOccupied(Direction.moveFrom(start, 'w'))

		self._dungeon[start[0]][start[1]] = PATH
		return tuple(start)

	# Construct the set of valid directions
	def _addToWorkingSet(self, working_set, coord, direction):
		test = Direction.moveFrom(coord, direction)
		if self._isInBounds(test) and not self._isOccupied(test):
			working_set.append(test)

	# Check if a cell is in bounds
	def _isInBounds(self, coord):
		return coord[0] > -1 and coord[0] < self._xDim and coord[1] > -1 and coord[1] < self._yDim

	# Check if a cell is occupied (not DEFAULT or out of bounds)
	def _isOccupied(self, coord):
		try:
			return self._dungeon[coord[0]][coord[1]] != DEFAULT
		except IndexError:
			return True

	# Check if a cell comes into contact with an existing feature (forward, left, and right are not a WALL, DEFAULT, or out of bounds)
	def _isSurrounded(self, coord, direction):
		forward = Direction.moveFrom(coord, direction)
		if self._isInBounds(forward) and self._dungeon[forward[0]][forward[1]] != DEFAULT and self._dungeon[forward[0]][forward[1]] != WALL:
			return True

		left = Direction.moveFrom(coord, Direction.turnLeftAsKey(direction))
		if self._isInBounds(left) and self._dungeon[left[0]][left[1]] != DEFAULT and self._dungeon[left[0]][left[1]] != WALL:
			return True

		right = Direction.moveFrom(coord, Direction.turnRightAsKey(direction))
		if self._isInBounds(right) and self._dungeon[right[0]][right[1]] != DEFAULT and self._dungeon[right[0]][right[1]] != WALL:
			return True

		return False


	'''
	Representation of dungeon in ASCII
	'''
	def __str__(self):
		out = ""
		
		for y in range(0, self._yDim):
			for x in range(0, self._xDim):
				out += self._dungeon[x][y]
				
			out += '\n'
		
		return out


if __name__ == '__main__':
	pass