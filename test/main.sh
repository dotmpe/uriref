#!/bin/sh

export PYTHONPATH=.:$PYTHONPATH

./bin/uriref-cli.py parseuri -O ptable 'http://example.net/path;param/name?query#fragment'
./bin/uriref-cli.py parseuri -O plain 'http://example.net/path;param/name?query#fragment'


