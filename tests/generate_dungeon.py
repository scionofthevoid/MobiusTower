from Dungeon import Dungeon

def run():
	m = Dungeon(119, 47)
	m.setNumTries(500)
	m.createRooms(0.0)
	m.createMaze(1)
	print(m)