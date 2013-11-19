import collections
import sys

_BACK = 'a'
_UP   = 'w'
_DOWN = 's'
_FWD  = 'd'
_ENT  = 'f'

_TREE = 't'

class ExitMenu(Exception):
	pass

class Menu(object):

	@staticmethod
	def exit():
		raise ExitMenu()

	def __init__(self, name, items):
		self._name   = name
		self._items  = items
		self._length = len(items)
		self._ptr    = 0

	def print_tree(self, indent=0):
		for txt, cmd in self._items:
			print('%s%s' % (
				'\t' * indent,
				txt
			))
			if isinstance(cmd, Menu):
				cmd.print_tree(indent=indent+1)

	def __call__(self, prmpt=''):
		ipt = None
		while ipt != _BACK:
			txt = self._items[self._ptr][0]
			cmd = self._items[self._ptr][1]
			print(txt)
			ipt = raw_input('%s> ' % (prmpt+self._name))
			if ipt == _UP:
				self._ptr = (self._ptr - 1) % self._length
			elif ipt == _DOWN:
				self._ptr = (self._ptr + 1) % self._length
			elif ipt in (_FWD, _ENT) and isinstance(cmd, collections.Callable):
				try:
					if isinstance(cmd, Menu):
						cmd(prmpt=prmpt+self._name+'/')
					else:
						cmd()
				except ExitMenu:
					break
			elif ipt == _TREE:
				self.print_tree()

class SubMenuB(Menu):
	def __init__(self):
		super(SubMenuB, self).__init__('Subclass', [
			('Method A', self.method_a),
			('Method B', self.method_b),
		])

	def method_a(self):
		print('SubMenuB.method_a')

	def method_b(self):
		print('SubMenuB.method_b')

def print_foo():
	print('foo')

subA = Menu('Sub A', [
	('Sub A', print_foo),
	('Sub B', SubMenuB()),
	('Exit', Menu.exit)
])

mnu = Menu('Main', [
	('Item 1', print_foo),
	('Sub Menu', subA)
])

if __name__ == '__main__':
	mnu()
