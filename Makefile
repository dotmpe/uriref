.PHONY: help all test profile

help:
	@echo 'nothing to do'

all:

test::
	PYTHONPATH=src/py python test/py/main.py

profile:: profiling-results.png profiling-results.svg

profiling-results.svg profiling-results.png: tmp/profile-results.csv
	cd bin; python plot-profile.py 
	mv bin/profiling-results.* ./

tmp/profile-results.csv:
	if test ! -e tmp; then mkdir tmp; fi
	cd bin;\
		PYTHONPATH=../src/py \
		python ../test/py/profile.py -csv | tee ../tmp/profile-results.csv
	

