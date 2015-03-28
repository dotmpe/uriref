Python uriref
==============
:Last-Update: 2011-02-13
:Homepage: https://launchpad.net/uriref
:Description:
  URL and URN parser written in regular expressions. 
  Based on RFC 2396 BNF terms, update to RFC 3986 planned but not started.
:License: FreeBSD

This is an experimental library. Do not use it in production unless you are
prepared to put in time for testing that it does what you need.

.. figure:: blob/master/doc/stdlib-comparison.svg
   :width: 45em
   :height: 55em
   :class: diagram

   uriref reference matching, compared to stdlib urlparse for several
   iteration-counts. The implementations are not tested for identical
   operation.

   The diagram shows constant times for each iteration count.
   The regex implementation outperforms stdlib's urlparse module
   by almost 100%. The latter runs at slighty above 6e-4 seconds,
   with the former at ~3.5e-4 seconds (at my machine).

   Memory profiling remains to be done, I guess regex is taking a lot
   more.

There are almost 100 tests, a good bunch of which need to be reviewed (33
failures). The modules has 34% test coverage.

`Coverage report <doc/htmlcov/index.html>`_ 
and `test results <doc/uriref_testreport.html>`_ are available in html.

See `uriref <src/py/uriref.py>`__.

.. dont work on github
.. .. include:: src/py/uriref.py
      :start-line: 1
      :end-line: 189

.. vim:ft=rst:
