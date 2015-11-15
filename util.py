# Check if string represents an int
# http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
def isInt(str):
	try:
		int(str)
		return True
	except:
		return False

# Add an item to the given dictionary
# d is a dict of (item => number of item) pairs
def addItemToDict(d, item):
    if item in d:
        d[item] += 1
    else:
        d[item] = 1

# Add an item to the given dictionary
# d is a dict of (item => number of item) pairs
# It is an error if d does not contain item
def deleteItemFromDict(d, item):
    assert (item in d), 'Dictionary does not contain the item(' + str(item) + ') to be deleted.'
    if d[item] > 1:
        d[item] -= 1
    else:
        del d[item]
