from typing import Tuple


class TrieNode(object):
	"""
	Our trie node implementation. Very basic. but does the job
	"""

	def __init__(self, char: str):
		self.char = char
		self.children = []
		# Is it the last character of the word.`
		self.word_finished = False
		# How many times this character appeared in the addition process
		self.counter = 0


def add(root, word: str):
	"""
	Adding a word in the trie structure
	"""
	node = root
	word = word.strip()
	for char in word:
		found_in_child = False
		# Search for the character in the children of the present `node`
		for child in node.children:
			if child.char == char:
				# We found it, increase the counter by 1 to keep track that another
				# word has it as well
				if (child.word_finished and child.counter<1):
					child.counter += 1
				# And point the node to the child that contains this char
				node = child
				found_in_child = True
				break
		# We did not find it so add a new chlid
		if not found_in_child:
			new_node = TrieNode(char)
			node.children.append(new_node)
			# And then point node to the new child
			node = new_node
	# Everything finished. Mark it as the end of a word.
	node.word_finished = True


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


def sum_level(root, level):
	if (level == 0):
		return 0

	node = root
	sum = 0
	if (level -1 == 0):
		for child in node.children:
			sum += child.counter
		return sum
	else:
		for child in node.children:
			sum += sum_level(child, level - 1)
		return sum


if __name__ == "__main__":
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


	# with open("C:/fib 201906/save2.txt") as fp:
	# 	for line in fp:
	# 		add(root,line)

	for pr in prelist:
		add(root, pr)

	print(find_prefix(root, '00000001000000001'))
	print(find_prefix(root, '000000010000000011110'))
	print(find_prefix(root, '000000010000000011111'))
	print(find_prefix(root, '0000000100000001010'))
	print(find_prefix(root, '1101111111111111010'))
	print(find_prefix(root, '11011111111111111100'))
	print(find_prefix(root, '110111111111110100110'))
	print(sum_level(root, 21))
	print(sum_level(root, 17))
	print(sum_level(root, 19))
	print(sum_level(root, 8))
	print(sum_level(root, 3))
