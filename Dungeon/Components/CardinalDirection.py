import operator


'''
Cardinal directions, indicated by a unit vector in that direction
'''
class Direction:
	'''
	Public directional constants
	'''
	NORTH = (0, -1)
	SOUTH = (0, 1)
	EAST = (1, 0)
	WEST = (-1, 0)
	
	
	'''
	Hidden class variables
	'''
	_names = {
		'n': (0, -1),
		'north': (0, -1),
		0: (0, -1),
		'e': (1, 0),
		'east': (1, 0),
		1: (1, 0),
		's': (0, 1),
		'south': (0, 1),
		2: (0, 1),
		'w': (-1, 0),
		'west': (-1, 0),
		3: (-1, 0),
		4: (1, -1),
		5: (1, 1),
		6: (-1, 1),
		7: (-1, -1)
	}
	
	# 90 degree turn (right)
	_rightTurn = [
		[0, -1],
		[1, 0]
	]
	# 180 degree turn (go in the opposite direction)
	_reverse = [
		[-1, 0],
		[0, -1]
	]
	# 270 degree turn (left)
	_leftTurn = [
		[0, 1],
		[-1, 0]
	]
	
	
	'''
	Basic direction retrieval
	'''
	# Outputs a vector in the specified direction
	@classmethod
	def get(cls, key):
		out = (0, 0)
		
		if type(key) is str:
			# String representation of a direction
			if len(key) < 3:
				# Single-character direction index
				for c in key.lower():
					if not c in Direction._names:
						raise ValueError('Unidentified direction indicator')
					
					out = tuple(map(operator.add, out, Direction._names[c]))
				
				return out
			elif len(key) < 6:
				# Index the direction by word
				if not key.lower() in Direction._names:
					raise ValueError('Unidentified direction indicator')
				
				return Direction._names[key.lower()]
			else:
				# Compound directions by word
				ns = key.lower()[:5]
				ew = key.lower()[5:]
				
				if not ns in Direction._names or not ew in Direction._names:
					raise ValueError('Unidentified direction indicator')
				
				return tuple(map(operator.add, Direction._names[ns], Direction._names[ew]))
		elif type(key) is int:
			# Integer representation of a direction
			if not key in Direction._names:
				raise ValueError('Unidentified direction indicator')
			
			return Direction._names[key]
		else:
			raise ValueError('Cannot map input to direction')

	# Outputs the string key (up to 2 characters long) for the given direction vector
	@classmethod
	def getKey(cls, d):
		parts = [tuple(0, d[1]), tuple(d[0], 0)]
		out = ''
		
		for v in parts:
			if v != (0, 0):
				for name, tuple in Direction._names.items():
					if tuple == v and len(name) == 1:
						out += name
						break
		
		if len(out) == 0:
			raise ValueError('Key not found for given direction')
		
		return out
	
	
	'''
	Directional movement
	'''
	# Outputs the resulting coordinate after going one unit forward in the specified direction
	@classmethod
	def moveFrom(cls, start, key):
		return tuple(map(operator.add, start, Direction.get(key)))
	
	# New direction after making a 90 degree right turn, assuming that you are going straight in the direction of @key (where @key is a valid direction)
	@classmethod
	def turnRightFrom(cls, key):
		if type(key) is str or type(key) is int:
			orig = Direction.get(key)
			return tuple(Direction._rotate(orig, Direction._rightTurn))
		elif type(key) is tuple:
			return tuple(Direction._rotate(key, Direction._rightTurn))
		else:
			raise ValueError('Cannot map input to direction')

	@classmethod
	def turnRightAsKey(cls, key):
		return Direction.getKey(Direction.turnRightFrom(key))
	
	# Go in the opposite direction of @key (where @key is a valid direction)
	@classmethod
	def reverseOf(cls, key):
		if type(key) is str or type(key) is int:
			orig = Direction.get(key)
			return tuple(Direction._rotate(orig, Direction._reverse))
		elif type(key) is tuple:
			return tuple(Direction._rotate(key, Direction._reverse))
		else:
			raise ValueError('Cannot map input to direction')
	
	@classmethod
	def reverseOfAsKey(cls, key):
		return Direction.getKey(Direction.reverseOf(key))

	# New direction after making a 90 degree left turn, assuming that you are going straight in the direction of @key (where @key is a valid direction)
	@classmethod
	def turnLeftFrom(cls, key):
		if type(key) is str or type(key) is int:
			orig = Direction.get(key)
			return tuple(Direction._rotate(orig, Direction._leftTurn))
		elif type(key) is tuple:
			return tuple(Direction._rotate(key, Direction._leftTurn))
		else:
			raise ValueError('Cannot map input to direction')

	@classmethod
	def turnLeftAsKey(cls, key):
		return Direction.getKey(Direction.turnLeftFrom(key))
	
	
	'''
	Helper functions
	'''
	# Multiply by rotation vector
	@classmethod
	def _rotate(cls, vector, matrix):
		return [
			matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
			matrix[1][0] * vector[0] + matrix[1][1] * vector[1]
		]