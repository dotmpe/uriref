Python uriref
==============
:Last-Update: 2011-02-13
:Homepage: https://launchpad.net/uriref
:Description:
  URL and URN parser written in regular expressions. 
  Based on RFC 2396 BNF terms, update to RFC 3986 planned but not started.


.. figure:: profiling-results.svg
   :width: 45em
   :height: 55em

   uriref reference matching, compared to stdlib urlparse

   The regex implementation runs up to twice as fast as the standard
   implementation for URI parsing.


See `uriref <src/py/uriref.py>`__.

.. .. include:: src/py/uriref.py
      :start-line: 1
      :end-line: 181


