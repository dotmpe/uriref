from . import *


### Testing

def bug1():
	"http://host"
	m = absoluteURI.match("my://host/path")
	gd = m.groupdict()
	# problem 1, what should the net path be?
	assert gd['net_path'] == '/path'
	# my guess:
	#assert gd['net_path'] == '//host/path', gd

	# problem 2, this be a hostname:
	m = absoluteURI.match("my://net")
	gd = m.groupdict()
	#assert gd['host'] == 'net', gd
	# and possibly related:
	#assert gd['net_path'] == '//net', gd
	assert URIRef('my://net/path').net_path == '/path'
	assert URIRef('my://net/path').netpath == '//net/path'

def print_complete_expressions():
	print("**relativeURI**::\n\t", r"^%(relativeURI)s(\# (?P<fragment> %(fragment)s))?$" % expressions)
	print()
	print("**absoluteURI**::\n\t", r"^%(absoluteURI)s(\# (?P<fragment> %(fragment)s))?$" % expressions)
	print()
	print("**abs_path**::\n\t", r"%(abs_path)s" % expressions)
	print()
	print("**net_path**::\n\t", r"%(net_path)s" % expressions)
	print()
	print("**scheme**::\n\t", r"%(scheme)s:" % expressions)
	print()
	print("**net_scheme**::\n\t", r"%(scheme)s:(\/\/)?" % expressions)
	print()


if __name__ == '__main__':
	bug1()
	print_complete_expressions()
