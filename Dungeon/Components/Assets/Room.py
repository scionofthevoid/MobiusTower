from Dungeon.Components.CardinalDirection import Direction


'''
A Room in the dungeon

Hidden properties define the room's structure
	@_upperLeft marks the leftmost x-coordinate and the top y-coordinate in that column
	@_lowerRight marks the rightmost x-coordinate and the bottom y-coordinate in that column
'''
class Room():
	symbol = 'R'


	'''
	Constructors
	'''
	def init():
		"""
		Create a room with no coordinates in it
		"""
		self._members = {}
		self._upperLeft = None
		self._lowerRight = None

	@classmethod
	def createRect(cls, upperLeft, lowerRight):
		"""
		Create a rectangular room
		"""
		r = Room()

		r._upperLeft = upperLeft
		r._lowerRight = lowerRight

		for x in range(upperLeft[0], lowerRight[0] + 1):
			# Map x coordinates to a dictionary of y coordinates
			r._members[x] = {}

			# Map y coordinates to number of cells inside the room
			for y in range(upperLeft[1], lowerRight[0] + 1):
				r._members[x][y] = lowerRight[1] - upperLeft[1] + 1

		return r

	@classmethod
	def fromFile(cls, filename):
		"""
		Create a room from a file containing the room representation
		"""
		r = Room()

		with open(filename) as f:
			lineCount = 0
			charCount = 0

			for line in f.readLine():
				for l in line:
					if l == Room.symbol:
						r.insert((charCount, lineCount))
					charCount += 1

				lineCount += 1
				charCount = 0

			f.close()

		return r


	'''
	Operations on rooms
	'''
	def exists(self, **kwargs):
		"""
		Check if a coordinate exists in the room

		On True, return dictionary location as tuple
		On False, return None
		"""
		if 'x' in kwargs:
			x = kwargs['x']

		if 'y' in kwargs:
			y = kwargs['y']

		if 'coord' in kwargs:
			x, y = kwargs['coord']

		if x in self._members:
			for key, value in self._members[x]:
				if y in range(key, key + value + 1):
					return (x, key)
		
		return None

	def isContiguous(self):
		"""
		Starting from _upperLeft, check to see if the room is contiguous
		"""
		# Blank rooms are vacuously contiguous
		if self._upperLeft == None:
			return True

		# Test if segment AB overlaps with segment CD
		def overlap(a, b, c, d):
			return b - c >= 0 and d - a >= 0

		# The current segment is contiguous if it overlaps with something to the right
		# Reaching the next column to operate on means that every segment to the left is already known to be contiguous
		islands = []
		for x in range(self._upperLeft[0], self._lowerRight[0]):
			for y in self._members[x]:
				coord = tuple([x, y])
				island = set([])

				# Check for overlap
				# There is no need to check the last column because there will be nothing to the right
				for y2 in self._members[x + 1]:
					if overlap(y, y + self._members[x][y], y2, y2 + self._members[x + 1][y2]):
						island.add(tuple([x + 1, y2]))
						break

				# Merge the island into an existing one if there is overlap
				for i in islands:
					# There are common elements if the intersection is less than the sum
					if len(island | i) < len(island) + len(i):
						i |= island
						island = None
						break

				# The island remains and island if it wasn't merged
				if not island == None:
					islands.append(island)

		# For the last column, verify that everything exists in the 0th island
		for y in self._members[self._lowerRight[0]]:
			if not tuple([self._lowerRight[0], y]) in islands[0]:
				return False

		# If there is only 1 island, there is at least 1 path between every segment
		return len(islands) == 1

	def insert(self, coord):
		"""
		Insert an x, y coordinate, returning True on success
		
		Fails to insert if the coordinate is already in the room
		Fails to insert if the room becomes non-contiguous
		"""
		# Already in the room
		if not self.exists({'coord': coord}) == None:
			return False

		# Find any existing segments to the north, east, south, and west
		north = self.exists({'coord': Direction.moveFrom(coord, 'n')})
		east = self.exists({'coord': Direction.moveFrom(coord, 'e')})
		south = self.exists({'coord': Direction.moveFrom(coord, 's')})
		west = self.exists({'coord': Direction.moveFrom(coord, 'w')})

		# An insert causes a non-contiguous room if the new @coord is not adjacent to anything in already in the room
		if north == None and east == None and south == None and west == None:
			return False

		# Perform the insertion and merge if possible
		if not coord[0] in self._members:
			self._members[coord[0]][coord[1]] = 1
		elif not north == None:
			# Add to segment to the north
			self._members[north[0]][north[1]] += 1

			# Merge north and south segments if they now touch
			if not south == None:
				self._members[north[0]][north[1]] += self._members[south[0]][south[1]]
				del self._members[south[0]][south[1]]
		elif not south == None:
			# Add to segment to the south
			self._members[coord[0]][coord[1]] = self._members[south[0]][south[1]] + 1
			del self._members[south[0]][south[1]]
		else:
			# Add as its own segment
			self._members[coord[0]][coord[1]] = 1

		# Update _upperLeft or _lowerRight if necessary
		if (coord[0] == self._upperLeft[0] and coord[1] < self._upperLeft[1]) or coord[0] < self._upperLeft[0]:
			self.upperLeft = coord
		elif (coord[0] == self._lowerRight[0] and coord[1] > self._lowerRight[1]) or coord[0] > self._lowerRight[0]:
			self._lowerRight = coord

		return True

	def delete(self, coord):
		"""
		Remove an x, y coordinate, returning True on success
		
		Fails to remove if the coordinate dosn't exist
		Fails to remove if the removal causes the room to become non-contiguous
		"""
		try:
			x, y = self.exists({'coord': coord})

			# Remove the coordinate
			if y == coord[1]:
				# Start the segment after @coord
				if self._members[x][y] > 0:
					self._members[x][y + 1] = self._members[x][y] - 1

				del self._members[x][y]
			elif coord[1] < y + self._members[x][y]:
				# Split the segment in two
				self._members[coord[0]][coord[1] + 1] = y + self._members[x][y] - coord[1]
				self._members[x][y] = coord[1] - y
			else:
				# Reduce the segment length by 1
				self._members[x][y] -= 1

			if len(self._members[x]) = 0:
				del self._members[x]

			# Put the coordinate back if the room becomes non-contiguous
			if self.isContiguous():
				return True
			else:
				return not self.insert(coord)
		except TypeError:
			# Not in the room
			return False


	'''
	Representations
	'''
	def render(self, dungeon):
		"""
		Draw the room on a target dungeon grid
		"""
		pass

	def __str__(self):
		"""
		Draw the room in ASCII as if there were nothing else around it
		"""
		out = []

		glMin, glMax = None, None
		locMin, locMax = None, None

		for x in range(self._upperLeft[0], self._lowerRight[0] + 1):
			col = ''
			for y in self._members[x]:
				if not locMin:
					locMin = y
					col += Room.symbol * self._members[x][y]
					locMax = y + self._members[x][y]
				elif y < locMin:
					col = Room.symbol * self._members[x][y] + ' ' * (locMin - self._members[x][y] - 1) + col
					locMin = y
				else:
					col += ' ' * (y - locMax - 1) + Room.symbol * self._members[x][y]
					locMax += (y - locMax - 1) + self._members[x][y]
			
			if not glMin:
				glMin = locMin
			elif glMin > locMin:
				out = [' ' * len(out[0]) for i in range(0, glMin - locMin + 1)].extend(out)
				glMin = locMin
			
			if not glMax:
				glMax = locMax
			elif glMax < locMax:
				out.extend([' ' * len(out[0]) for i in range(0, locMax - glMax + 1)])
				glMax = locMax
			
			if len(out) == 0:
				out = [c for c in col]
			else:
				for c in range(0, len(col)):
					out[c] += col[c]
			
			locMin, locMax = None, None

		return out