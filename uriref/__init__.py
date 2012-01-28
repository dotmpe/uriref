"""
uriref - extensible URI parser based on Regular Expressions.

This code provides regular expressions to validate and parse Universal Resource
Identifiers as defined by (the BNF in) RFC 2396.

Each BNF term is translated to Python Regular Expression. The resulting set of
partial expressions are merged using string formatting and compiled into regex
object to match absolute, relative references, and other parts of URIs
(URLs and URNs). This method does not provide the most optimized expressions,
but is very precise and easy to work with.

The project started as an exercise and out of curiosity to the exact patterns 
and validation of URI references.
This implementation runs up to twice as fast as Python's standard implementation
for URI parsing (`urlparse`).

The current naming of groups or URI parts needs some work but I have not come
around to that yet.

Uniform Resource Indicator parts
--------------------------------
This diagram breaks a reference up into its parts, using the names from the BNF
terms in RFC 2396. Only the terms relevant are shown.

::

	( domainlabel "." ) toplabel [ "." ]
	------------------------------------
			  |
		   hostname | IPv4address
		   ----------------------		 *pchar *( ";" param )
					 |					---------------------
				   host [ ":" port ]			   |
				   -----------------		*--------------*
						 |				  |			  |
   [ [ userinfo "@" ] hostport ]		 segment *( "/" segment )
   -----------------------------		 ------------------------
			   |							  |
			 server | reg_name		"/"  path_segments
			 -----------------		------------------
					   |						|
					   |			   *--------*----------------------*
					   |			   |		|					  |
				"//" authority [ abs_path ]	 |	rel_segment [  abs_path ]
				---------------------------	 |	-------------------------
							  |				 |			   |
			*-----------------*				 |			   |
			|		  *------|------------*----*			   |
			|		  |	  |			|					*---*
			|		  |	  |			|						|
			|		  |   ( net_path | abs_path | opaque_part | rel_path ) [ "?" query ]
			|		  |   --------------------------------------------------------------
			|		  |						|
	   ( net_path | abs_path ) [ "?" query]	 |
	   ------------------------------------	 |
						|					   |
		scheme ":" ( hier_part | opaque_part )  |
		--------------------------------------  |
								 |			  |
						   [ absoluteURI | relativeURI ] [ "#" fragment ]
						   ----------------------------------------------
											   |
											   |
										 URI-reference

The only deviation between the RFC's BNF terms and the regular expressions groups
is that the `net_path` *match group* is the `abs_path` of the `net_path` *BNF term*.
Otherwise these terms give difficulties with regex nesting (as group id's
should be unique).

There are three types of path found in URIs:

- net_path; abs_path in uri with authority given.
- abs_path; absolute, rooted paths but no authority (any other abs_path).
- rel_path; relative paths (unrooted paths).

`rel_path` only appears in relative URIs, `net_path` and `abs_path` in both
relative and absolute URIs.


Usage of this module
--------------------
Most importantly, this module provides the compiled expressions `relativeURI`
and `absoluteURI` to match the respective reference notations. Function `match`
takes any reference and uses the compiled expression `scheme` to determine
if the string represents a relative or absolute reference.
New RegEx objects (to match other identifer(s)-parts) my be created using string 
formatting. All partial expressions (mostly translated BNF terms) reside in 
`partial_expressions`, while `grouped_partial_expressions` adds Id's for some
groups. `merge_strings` is a function to merge the partial expressions into a
complete RegEx string.

The function `parseuri` uses the RegEx match object return by `match` and
returns a six-part tuple, such as Python's stdlib urlparse returns.

In addition, each part is available as attribute on instances of `URIRef`.

>>> from cllct.uri import URIRef
>>> URIRef('file://home/test').path
'/test'
>>> URIRef('file://home/test').path
>>> URIRef('file://home/test').scheme
'file'

`query`, `path` and `port` are special attributes which will return the expected
part and in the proper type.

Extending to match specific URIs
--------------------------------
Patterns are named after their BNF terms and kept in dictionaries.

- `partial_expressions` contains the translated BNF terms from RFC 2396,
  which is merged into `expressions`.
- `grouped_partial_expressions` adds some match group id's to the partial
  expressions, `grouped_expressions` contains the merged form of these.

The parts in these dictionaries can used to build your own custom regex's
for URI matching. For example, to match `mysql://` style links one could
create an regex object as follows::

  grouped_partial_expressions['mysq_db_ref'] = \
	  r"^mysql: // %(authority)s / (?P<db> %(pchar)s*)$"
  mysql_link_expr = merge_strings(grouped_partial_expressions)['mysq_db_ref']
  mysql_link_re = re.compile(mysql_link_expr, re.VERBOSE)

See above diagram or the RFC for the part names. Because the dictionary with
match-group IDs is used (and one is added, 'db'), this results in a match
object with the following nicely named groups::

  __________<mysql://user:withpass@dbhost:3306/database>
  userinfo :		 user:withpass
  host	 :					   dbhost
  port	 :							  3306
  db	   :								   database

Examples of references
----------------------
::

  _____________<http://user@sub.domain.org:80/path/to/leaf.php?query=arg&q=foo#fragment>
  scheme	  : http
  authority   :		user@sub.domain.org:80
  userinfo	:		user
  host		:			 sub.domain.org
  port		:							80
  net_path	:							  /path/to/leaf.php
  query	   :												query=arg&q=foo
  fragment	:																fragment

::

  _____________<ftp://usr:pwd@example.org:4321/pub/>
  scheme	  : ftp
  authority   :	   usr:pwd@example.org:4321
  userinfo	:	   usr:pwd
  host		:			   example.org
  port		:						   4321
  net_path	:							   /pub/

::

  _____________<mid:some-message@example.org>
  scheme	  : mid
  opaque_part :	 some-message@example.org

::

  _____________<service?query=foo>
  rel_path	: service
  query	   :		 query=foo


See bin/parseuri for interactive parsing and tabular parts rendering.

Misc.
-----
- TODO: better parsing of paths, parameters, testing.
- XXX: stdlib 'urlparse' only allows parameters on the last path segment.
- TODO: update to RFC 3986
   

References
----------
.. [RFC_2396] `Uniform Resource Identifiers (URI): Generic Syntax`,
			  T. Berners-Lee et al., 1998 <http://tools.ietf.org/html/rfc2396>
.. [RFC_3986] `Uniform Resource Identifiers (URI): Generic Syntax`,
			  T. Berners-Lee et al., 2005 <http://tools.ietf.org/html/rfc3986>

"""
import re
import urlparse as stdlib_urlparse



# Expressions
"""
A dictionary of Regular Expressions as transcribed from RFC 2396 BNF,
parts are referenced using Python's string formatting notation.
"""
partial_expressions = {
	# RFC 2396 1.6.
	'alpha': r"%(lowalpha)s%(upalpha)s",
	'lowalpha': r"a-z",
	'upalpha': r"A-Z",
	'digit': r"0-9",
	'alphanum': r"%(alpha)s%(digit)s",
	# RFC 2396 2.
	'uric': r"[%(unreserved)s%(reserved)s%(escaped)s]",
	# RFC 2396 2.3.
	'unreserved': r"%(mark)s%(alphanum)s",
	# RFC 2396 2.2.
	'reserved': r"; / ? : @ & = + $ ,",
	# RFC 2396 2.4.2.
	'escaped': r"%%a-zA-Z0-9",
	# RFC 2396 3.
	'net_path': r"// %(authority)s %(abs_path)s",
	'hier_part': r"( (%(net_path)s) | (%(abs_path)s) ) (\? %(query)s )?",
	'opaque_part': r"%(uric_no_slash)s %(uric)s*",
	# RFC 2396 3.1.
	'scheme': r"[%(alpha)s] [- + \. %(alpha)s %(digit)s]*",
	# RFC 2396 3.2.
	'authority': r"%(server)s | %(reg_name)s",
	# RFC 2396 3.2.1.
	'reg_name': r"[%(unreserved)s %(escaped)s $ , ; : & = +]*",
	# RFC 2396 3.2.2.
	'server': r"(%(userinfo)s @)? %(hostport)s",
	'userinfo': r"[%(unreserved)s %(escaped)s $ , ; : & = +]*",
	'hostport': r"%(host)s ( : %(port)s )?",
	'host': r"( %(hostname)s | %(IPv4address)s )",
	'hostname': r"(%(domainlabel)s \.)* %(toplabel)s (\.)? ", # RFC 2396 says there can be a trailing "." for local domains
	'domainlabel': r"([%(alphanum)s] | ([%(alphanum)s][-%(alphanum)s]*[%(alphanum)s]))",
	'toplabel': r"([%(alpha)s] | ([%(alpha)s] [-%(alphanum)s]* [%(alphanum)s]))",
	'IPv4address': r"([0-9]+ \. [0-9]+ \. [0-9]+ \. [0-9]+)",
	'port': r"[0-9]+",
	# RFC 2396 3.3. Path Component
	# XXX: difference here
	#'path': r"( %(abs_path)s | %(opaque_part)s )",
	'pchar': r"[%(unreserved)s%(escaped)s:@&=+$,]",
	'segment': r"(%(pchar)s* (; %(param)s)*)",
	'path_segments': r"(%(segment)s) (/ %(segment)s)*",
	'abs_path': r"/ %(path_segments)s",
	'param': r"%(pchar)s*",
	# RFC 2396 3.4. Query Component
	'query': r"%(uric)s*",
	# RFC 2396 4., RFC 2396 5.
	'relativeURI': r"((%(net_path)s) | (%(abs_path)s) | (%(rel_path)s) | (%(opaque_part)s)) (\? %(query)s)?",
	'absoluteURI': r"%(scheme)s : (%(hier_part)s) | (%(opaque_part)s)",
	'URI_reference': r"((%(absoluteURI)s | %(relativeURI)s) (\# %(fragment)s)?)",
	# RFC 2396 4.1.
	'fragment': r"%(uric)s*",
	# Other
	'mark': r"- _ \. ! ~ * ' ( )",
	'rel_segment': r"[ %(unreserved)s %(escaped)s ; @ & = + $ ,]{1}",
	'rel_path': r"%(rel_segment)s (%(abs_path)s)?",
	'uric_no_slash': r"[%(unreserved)s %(escaped)s ; ? : @ & = + $ ,]",
}

def merge_strings(strings):
	"""
	Format every string in dictionary `strings` using the same dictionary until
	every string has been formatted (merged). Returns a dictionary with all
	string formatting references replaced.

	Important! More than one non-existing formatting reference will cause an infinite loop.
	"""

	results = {}

	names = strings.keys()
	while names:
		# cycle through the list until all strings are resolved
		name = names.pop(0)
		try:
			results[name] = (strings[name] % results)
		except Exception, e:
			names.append(name)
			# one unformatted string left while every other string is merged:
			assert name != names[0], 'Cannot resolve %s' % name

	return results

# Merge unformatted strings
expressions = merge_strings(partial_expressions)


# Give some regex groups an ID
grouped_partial_expressions = {
	'userinfo': r"(?P<userinfo> [%(unreserved)s %(escaped)s ; : & = + $ ,]*)",
	'port': r"(?P<port> [0-9]*)",
	'host': r"(?P<host> %(hostname)s | %(IPv4address)s)",
	'query': r"(?P<query> %(uric)s*)",
	'abs_path': r"/ %(path_segments)s",
	'authority': r"(?P<authority> (%(server)s) | %(reg_name)s)",
	'net_path': r"// %(authority)s (?P<net_path> %(abs_path)s)",
	'hier_part': r"((%(net_path)s) | (?P<abs_path> %(abs_path)s)) (\? %(query)s)?",
	'opaque_part': r"(?P<opaque_part> %(uric_no_slash)s %(uric)s*)",
	'scheme': r"(?P<scheme> %s)" % partial_expressions['scheme'],
	'relativeURI': r"((%(net_path)s) | (?P<abs_path> %(abs_path)s) | (?P<rel_path> %(rel_path)s) | (%(opaque_part)s)) (\? %(query)s)?",
	'absoluteURI': r"%(scheme)s : (%(hier_part)s | %(opaque_part)s)",
}
for k, e in partial_expressions.items():
	grouped_partial_expressions.setdefault(k, e)

# Merge unformatted strings
grouped_expressions = merge_strings(grouped_partial_expressions)


### Regex objects for matching relative and absolute URIRef notations

relativeURI = re.compile(r"^%(relativeURI)s(\# (?P<fragment> %(fragment)s))?$" % grouped_expressions, re.VERBOSE)
"a URI with no scheme-part and optional fragment part"

absoluteURI = re.compile(r"^%(absoluteURI)s(\# (?P<fragment> %(fragment)s))?$" % grouped_expressions, re.VERBOSE)
"a URI with scheme-part and optional fragment part"


### Regex objects of URIRef strings

abs_path = re.compile(r"^%(abs_path)s$" % grouped_expressions, re.VERBOSE)
"matches an absolute path"

net_path = re.compile(r"^%(net_path)s$" % grouped_expressions, re.VERBOSE)
"matches a full net_path, ie. //host/path "

scheme = re.compile(r"^%(scheme)s:" % grouped_expressions, re.VERBOSE)
"matches the scheme part"

net_scheme = re.compile(r"^%(scheme)s:(\/\/)?" % grouped_expressions, re.VERBOSE)
"matches the scheme part and tests for a net_path"


### Functions to validate and parse URIRef strings

def match(uriref):
	"""
	Match given `uriref` string using a Regular Expression.

	If the passed in string starts with a valid scheme sequence it is treated as
	an absolute-URI, otherwise a relative one.

	Returns the match object or None.
	"""

	if scheme.match(uriref):
		return absoluteURI.match(uriref)
	else:
		return relativeURI.match(uriref)


def urlparse(uriref, md=None):
	"""
	Comparible with Python's stdlib urlparse, parse a URL into 6 components:

		<scheme>://<netloc>/<path>;<params>?<query>#<fragment>

	and no further split of the components. Returns tuple.
	"""

	if not md:
		md = match(uriref).groupdict()

	if 'scheme' not in md:
		md['scheme'] = None

	auth = ''
	if 'hostname' in md:
		auth = md['hostname']
		if 'userinfo' in md:
			auth = "%s@%s" % (md['userinfo'], auth)
		if 'port' in md:
			auth += ':%i' % md['port']

	path = ''
	if 'abs_path' in md:
		path = md['abs_path']
	elif 'net_path' in md:
		path = md['net_path']

	params = ''

	return stdlib_urlparse.ParseResult(
	        md['scheme'] or '',
	        auth, path, params, 
	        md['query'] or '',
	        md['fragment'] or ''
        )

#URIREF_RE = r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?$'
#URIREF_GROUPED_RE = r'^((?P<scheme>[^:/?#]+):)?(//(?P<authority>[^/?#]*))?(?P<path>[^?#]*)(\?(?P<query>[^#]*))?(#(?P<fragment>.*))?'
#"Break-down well-formed URI reference into its components [RFC 3986]"


# TODO: compare regex results against urlparse.urlsplit

### URI parsing based on urlparse

def isfragment(url, location=None):

	"""Return true if URL links to a fragment.
	"""

	urlparts = stdlib_urlparse.urlsplit(url)
	if not location and not urlparts[4] is None:
		return False

	elif location and urlparts[4]:
		locparts = stdlib_urlparse.urlsplit(location)
		# scheme
		if urlparts[0] and not urlparts[0] is locparts[0]:
			return False
		# domain
		elif not onsamedomain(url, location):
			return False
		# path
		elif urlparts[2] and not urlparts[2] is locparts[2]:
			return False
		# query
		elif urlparts[3] and not urlparts[3] is locparts[3]:
			return False
		return True

	elif urlparts[4]:
		return True

	return False

def get_hostname(url):

	"""Return the hostname of the given `url`.
	"""

	hostname = stdlib_urlparse.urlsplit(url)[1]
	if ':' in hostname:
		hostname = hostname.split(':').pop(0)
	return hostname

def onsamedomain(url1, url2):

	"""Examine the URLs and return true if they are on the same
	domain (but perhaps in a different subdomain).
	"""

	url1parts = stdlib_urlparse.urlsplit(url1)
	url2parts = stdlib_urlparse.urlsplit(url2)
	host1, host2 = url1parts[1], url2parts[1]
	host1, host2 = host1.split('.'), host2.split('.')

	# TLD
	if len(host1) > 0 and len(host2) > 0:
		part1, part2 = host1.pop(), host2.pop()
		if not part1 == part2:
			return False
	# domain
	if len(host1) > 0 and len(host2) > 0:
		part1, part2 = host1.pop(), host2.pop()
		if not part1 == part2:
			return False
		else:
			return True
	return False



class URIRef(str):

	"""
	Convenience class with regular expression parsing of URI's and
	formatting back to string representation again.
	"""

	def __new__(type, *args, **kwds):
		return str.__new__(type, *args)

	def __init__(self, uri, opaque_targets=[]):
		"Construct instance with match object and parts dictionary."
		"`opaque_targets` indicates partnames which may 'default' to opaque_part."

		str.__init__(uri)
		self.__match__ = match(uri)
		self.__groups__ = self.__match__.groupdict()

		self.opaque_targets = opaque_targets
		"The partnames that if not set get the value of opaque_part/"

	def __getattr__(self, name):
		"Generic getter access to match groups. "
		part = None
		if name in self.__groups__:
			part = self.__groups__[name]
		if not part and name in self.opaque_targets:
			part = self.__groups__['opaque_part']
		if not part and name == 'path':
			part = self.path
		return part

	# Special 'groups'
	@property
	def port(self, *value):
		port = int(self.__groups__['port'])
		if not port:
			if self.scheme in ('http', 'https'):
				return 80
			elif self.scheme in ('file',):
				return 21
			else:
				assert False, self.href # not implemented
		return port

	@property
	def query(self, *value):
		return self.__groups__['query']

	@property
	def path(self, *value):
		for path in 'abs_path', 'rel_path', 'net_path':
			if path in self.__groups__ and self.__groups__[path]:
				return self.__groups__[path]

	#
	def generate_signature(self):
		sig = []
		if self.scheme:
			sig.extend((self.scheme, ':'))

		if self.host:
			sig.append('//')
			if self.userinfo:
				sig.extend((self.userinfo, '@'))
			sig.append(self.host)
			if self.port:
				sig.extend((':', self.port))

		if self.path:
			sig.append(self.path)
		elif self.opaque_part:
			sig.append(self.opaque_part)
		else:
			sig.append('/')

		if self.query:
			sig.extend(('?', self.query))
		if self.fragment:
			sig.extend(('#', self.fragment))

		return tuple(sig)

	def __repr__(self):
		return "URIRef(%s)" % self

	def __str__(self):
		return "".join(self.generate_signature())


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
	assert gd['net_path'] == '//net', gd

def print_complete_expressions():
	print "**relativeURI**::\n\t", r"^%(relativeURI)s(\# (?P<fragment> %(fragment)s))?$" % expressions
	print
	print "**absoluteURI**::\n\t", r"^%(absoluteURI)s(\# (?P<fragment> %(fragment)s))?$" % expressions
	print
	print "**abs_path**::\n\t", r"%(abs_path)s" % expressions
	print
	print "**net_path**::\n\t", r"%(net_path)s" % expressions
	print
	print "**scheme**::\n\t", r"%(scheme)s:" % expressions
	print
	print "**net_scheme**::\n\t", r"%(scheme)s:(\/\/)?" % expressions
	print


if __name__ == '__main__':
	bug1()
	print_complete_expressions()
