import sys, yaml
from config import settings


from Dungeon import Dungeon

from tests.generate_dungeon import run


def run_tests(tests):
	run()


if __name__ == '__main__':
	if settings['env'] == 'DEV':
		run_tests(settings['tests'])
	elif settings['env'] = 'PROD':
		pass