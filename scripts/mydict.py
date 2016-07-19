
def chainitem(pepe, list_key):
	"""
	pepe is a dictionary with lots of keys.
	"""

	sub_dict = pepe[list_key[0]]
	for key in list_key[1:]:
		sub_dict = sub_dict[key]
	return sub_dict