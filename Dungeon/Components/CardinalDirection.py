import operator

'''
Cardinal directions, indicated by an offset vector
'''
class Direction:
	NORTH = (0, -1)
	SOUTH = (0, 1)
	EAST = (1, 0)
	WEST = (-1, 0)

	# Outputs a vector in the specified direction
	@classmethod
	def get(cls, key):
		if key.lower() == 'north' or key.lower() =='n' or key == 0:
			return Direction.NORTH
		elif key.lower() == 'south' or key.lower() == 's' or key == 1:
			return Direction.SOUTH
		elif key.lower() == 'east' or key.lower() == 'e' or key == 2:
			return Direction.EAST
		elif key.lower() == 'west' or key.lower() == 'w' or key == 3:
			return Direction.WEST
		elif key.lower() == 'northeast' or key.lower() =='ne' or key == 4:
			return tuple(map(operator.add, Direction.NORTH, Direction.EAST))
		elif key.lower() == 'southeast' or key.lower() =='se' or key == 5:
			return tuple(map(operator.add, Direction.SOUTH, Direction.EAST))
		elif key.lower() == 'southwest' or key.lower() =='sw' or key == 6:
			return tuple(map(operator.add, Direction.SOUTH, Direction.WEST))
		elif key.lower() == 'northwest' or key.lower() =='nw' or key == 7:
			return tuple(map(operator.add, Direction.NORTH, Direction.WEST))

	# Outputs a one-character key for the given direction vector
	@classmethod
	def getKey(cls, direction):
		if direction == Direction.NORTH:
			return 'n'
		elif direction == Direction.EAST:
			return 'e'
		elif direction == Direction.SOUTH:
			return 's'
		elif direction == Direction.WEST:
			return 'w'

	# Outputs the resulting coordinate after going one unit forward in the specified direction
	@classmethod
	def moveFrom(cls, start, key):
		if key.lower() == 'north' or key.lower() =='n' or key == 0:
			return tuple(map(operator.add, start, Direction.NORTH))
		elif key.lower() == 'south' or key.lower() == 's' or key == 1:
			return tuple(map(operator.add, start, Direction.SOUTH))
		elif key.lower() == 'east' or key.lower() == 'e' or key == 2:
			return tuple(map(operator.add, start, Direction.EAST))
		elif key.lower() == 'west' or key.lower() == 'w' or key == 3:
			return tuple(map(operator.add, start, Direction.WEST))
		elif key.lower() == 'northeast' or key.lower() =='ne' or key == 4:
			return tuple(map(operator.add, tuple(map(operator.add, start, Direction.NORTH)), Direction.EAST))
		elif key.lower() == 'southeast' or key.lower() =='se' or key == 5:
			return tuple(map(operator.add, tuple(map(operator.add, start, Direction.SOUTH)), Direction.EAST))
		elif key.lower() == 'southwest' or key.lower() =='sw' or key == 6:
			return tuple(map(operator.add, tuple(map(operator.add, start, Direction.SOUTH)), Direction.WEST))
		elif key.lower() == 'northwest' or key.lower() =='nw' or key == 7:
			return tuple(map(operator.add, tuple(map(operator.add, start, Direction.NORTH)), Direction.WEST))

	# New direction after making a 90 degree left turn, assuming that you are going straight in the direction of @key
	@classmethod
	def turnLeftFrom(cls, key):
		if key == 0 or key == Direction.NORTH:
			return Direction.WEST
		elif key == 2 or key == Direction.EAST:
			return Direction.NORTH
		elif key == 1 or key == Direction.SOUTH:
			return Direction.EAST
		elif key == 3 or key == Direction.WEST:
			return Direction.SOUTH
		elif key.lower() == 'north' or key.lower() =='n':
			return Direction.WEST
		elif key.lower() == 'east' or key.lower() == 'e':
			return Direction.NORTH
		elif key.lower() == 'south' or key.lower() == 's':
			return Direction.EAST
		elif key.lower() == 'west' or key.lower() == 'w':
			return Direction.SOUTH

	@classmethod
	def turnLeftAsKey(cls, key):
		if key == 0 or key == Direction.NORTH:
			return 'w'
		elif key == 1 or key == Direction.EAST:
			return 'e'
		elif key == 2 or key == Direction.SOUTH:
			return 'n'
		elif key == 3 or key == Direction.WEST:
			return 's'
		elif key.lower() == 'north' or key.lower() =='n':
			return 'w'
		elif key.lower() == 'south' or key.lower() == 's':
			return 'e'
		elif key.lower() == 'east' or key.lower() == 'e':
			return 'n'
		elif key.lower() == 'west' or key.lower() == 'w':
			return 's'

	# New direction after making a 90 degree right turn, assuming that you are going straight in the direction of @key
	@classmethod
	def turnRightFrom(cls, key):
		if key == 0 or key == Direction.NORTH:
			return Direction.EAST
		elif key == 2 or key == Direction.EAST:
			return Direction.SOUTH
		elif key == 1 or key == Direction.SOUTH:
			return Direction.WEST
		elif key == 3 or key == Direction.WEST:
			return Direction.NORTH
		elif key.lower() == 'north' or key.lower() =='n':
			return Direction.EAST
		elif key.lower() == 'east' or key.lower() == 'e':
			return Direction.SOUTH
		elif key.lower() == 'south' or key.lower() == 's':
			return Direction.WEST
		elif key.lower() == 'west' or key.lower() == 'w':
			return Direction.NORTH

	@classmethod
	def turnRightAsKey(cls, key):
		if key == 0 or key == Direction.NORTH:
			return 'e'
		elif key == 2 or key == Direction.EAST:
			return 's'
		elif key == 1 or key == Direction.SOUTH:
			return 'w'
		elif key == 3 or key == Direction.WEST:
			return 'n'
		elif key.lower() == 'north' or key.lower() =='n':
			return 'e'
		elif key.lower() == 'east' or key.lower() == 'e':
			return 's'
		elif key.lower() == 'south' or key.lower() == 's':
			return 'w'
		elif key.lower() == 'west' or key.lower() == 'w':
			return 'n'