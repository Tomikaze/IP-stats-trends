from typing import Tuple


class TrieNode(object):
	"""
	Our trie node implementation. Very basic. but does the job
	"""

	def __init__(self, char: str, *nexthop: str):

		self.char = char
		self.children = []
		# Is it the last character of the word.`$
		self.word_finished = False
		# How many times this character appeared in the addition process
		self.counter = 0
		self.nexthop = str(nexthop).strip("(,)'")
		self.depth=0
		self.word= ''

	def display(self):
		lines, *_ = self._display_aux()
		for line in lines:
			print(line)

	def _display_aux(self):
		"""Returns list of strings, width, height, and horizontal coordinate of the root."""
		# No child.

		if len(self.children) == 0:
			if self.word_finished:
				line = '%s' % "|" + self.word + "|"
			else:
				line = '%s' % self.char
			width = len(line)
			height = 1
			middle = width // 2
			return [line], width, height, middle

		# Only left child.
		if len(self.children) == 1:
			lines, n, p, x = self.children[0]._display_aux()
			if self.word_finished:
				s = '%s' % "|" + self.word + "|"
			else:
				s = '%s' % self.char
			u = len(s)
			first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
			second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
			shifted_lines = [line + u * ' ' for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

		# Only right child.
		# if self.left is None:
		# 	lines, n, p, x = self.right._display_aux()
		# 	s = '%s' % self.key
		# 	u = len(s)
		# 	first_line = s + x * '_' + (n - x) * ' '
		# 	second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
		# 	shifted_lines = [u * ' ' + line for line in lines]
		# 	return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

		# Two children.

		left, n, p, x = self.children[0]._display_aux()
		right, m, q, y = self.children[1]._display_aux()
		if self.word_finished:
			s = '%s' % "|" + self.word + "|"
		else:
			s = '%s' % self.char
		u = len(s)
		first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
		second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
		if p < q:
			left += [n * ' '] * (q - p)
		elif q < p:
			right += [m * ' '] * (p - q)
		zipped_lines = zip(left, right)
		lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
		return lines, n + m + u, max(p, q) + 2, n + u // 2


def leafpush(root):
	node = root
	char = ''
	if not root.children:
		return False
	if root:
		# First print the data of node
		if node.word_finished and len(node.children) == 1:
			if node.children[0].char == '0':
				char = '1'
			else:
				char = '0'
			new_node = TrieNode(char)
			new_node.word_finished = True
			new_node.nexthop=node.nexthop
			new_node.word=node.word+new_node.char
			new_node.depth=node.depth+1
			node.children.append(new_node)
			node.word_finished = False

		if node.word_finished and len(node.children) == 2:
			node.word_finished = False

		for child in node.children:
			leafpush(child)


def printPreorder(root):
	if root:
		if root.word_finished:
			print(root.word)

		for child in root.children:
			printPreorder(child)


def maxDepth(root):
	D=0
	Depth = 0
	if root is None:
		return Depth;

	else:
		for child in root.children:
			D = maxDepth(child)
			if D>Depth:
				Depth=D
		return Depth +1


def make_pushed_list(root,list):
	if root:
		if root.word_finished:
			# print(root.word+":"+str(root.depth))
			range=str(2**(32-root.depth))
			list_element=[root.word,range,root.nexthop]
			list.append(list_element)

		for child in root.children:
			make_pushed_list(child,list)



def add(root, word: str, *nexthop):
	"""
	Adding a word in the trie structure
	"""
	depth=0
	node = root
	word = word.strip()
	for char in word:
		found_in_child = False
		depth=depth+1
		# Search for the character in the children of the present `node`
		for child in node.children:
			if child.char == char:
				# We found it, increase the counter by 1 to keep track that another
				# word has it as well
				if (child.word_finished and child.counter < 1):
					child.counter += 1
				# And point the node to the child that contains this char
				node = child
				found_in_child = True
				break
		# We did not find it so add a new chlid
		if not found_in_child:
			str = ''.join(nexthop).strip("(,)'")
			new_node = TrieNode(char, str)
			new_node.depth=depth
			node.children.append(new_node)
			# And then point node to the new child
			node = new_node
	# Everything finished. Mark it as the end of a word.
	node.word_finished = True
	node.word=word


def find_prefix(root, prefix: str) -> Tuple[bool, int]:
	"""
	Check and return
	  1. If the prefix exsists in any of the words we added so far
	  2. If yes then how may words actually have the prefix
	"""
	node = root
	# If the root node has no children, then return False.
	# Because it means we are trying to search in an empty trie
	if not root.children:
		return False, 0
	for char in prefix:
		char_not_found = True
		# Search through all the children of the present `node`
		for child in node.children:
			if child.char == char:
				# We found the char existing in the child.
				char_not_found = False
				# Assign node as the child containing the char and break
				node = child
				break
		# Return False anyway when we did not find a char.
		if char_not_found:
			return False, 0
	# Well, we are here means we have found the prefix. Return true to indicate that
	# And also the counter of the last node. This indicates how many words have this
	# prefix
	return True, node.counter


def count_first_letter(root, level, branch):
	node = root

	if node.word_finished:
		branch[level - 1] += 1
	# print("branch "+str(level)+": "+str(branch[level]))
	else:
		for child in node.children:
			count_first_letter(child, level + 1, branch)


def sum_level(root, level):
	if (level == 0):
		return 0

	node = root
	sum = 0
	if (level - 1 == 0):
		for child in node.children:
			sum += child.counter
		return sum
	else:
		for child in node.children:
			sum += sum_level(child, level - 1)
		return sum


if __name__ == "__main__":
	count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	root = TrieNode('*')
	prelist = [
		"00",
		"10",
		"000",
		"010",
		"011",
		"100",
		"101",
		"110",
		"111",
		"0010",
		"0011",
		"0100",
		"0101",
		"0110",
		"0111",
		"1010",
		"1011",
		"1101",
		"1110",
		"1111",
		"00100",
		"00101",
		"00110",
		"00111",
		"01000",
		"01001",
		"11000",
		"11001",
		"11110",
		"11111",
		"001010",
		"001011",
		"110000",
		"110001",
		"110010",
		"110011",
		"0010111",
		"00101100",
		"00101101",
		"001011000",
		"001011001",
		"001011010",
		"001011011"]

	with open("C:/teszt/act.txt") as fp:
		for line in fp:
			add(root, line)

	# for pr in prelist:
	# 	add(root, pr)

	print(sum_level(root, 21))
	print(sum_level(root, 17))
	print(sum_level(root, 19))
	print(sum_level(root, 8))
	print(sum_level(root, 3))
	print('------------')
	count_first_letter(root, 0, count)
	cnt = 0
	for i in count:
		cnt += 1
		print(str(cnt) + ': ' + str(i))
	print('------------')
	per8 = 0
	for i in range(0, 32):
		per8 += count[i] * (1 / (2 ** (i - 7)))
		print("per8 " + str(i + 1) + ": " + str(count[i]))
		print("per8 normalized " + str(i + 1) + ": " + str(count[i] * (1 / (2 ** (i - 7)))))

	print('per8 Sum: ' + str(per8))
