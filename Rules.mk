include                $(MK_SHARE)Core/Main.dirstack.mk
MK_$d               := $/Rules.mk
MK                  += $(MK_$d)
#
#      ------------ -- 

SRC_$d              := $/src/py/uriref.py

TRGT_$d             := \
	$/profiling_urllib-comparison_.py

DEP_$d              :=
DMK_$d              :=

define python-urllib-profile 
	if test ! -e $(BUILD); then mkdir $(BUILD); fi
	cd bin;\
	PYTHONPATH=../src/py \
	python ../test/py/profile.py -csv | tee ../$(BUILD)/profile-results.csv
endef

#      ------------ -- 
#
TEST_$d             += profile_$d
.PHONY:                profile_$d

profile_$d:: profiling-results.png profiling-results.svg

$Bprofile-results.csv::
	$(python-urllib-profile)

profiling-results.svg profiling-results.png: $Bprofile-results.csv
	cd bin; python plot-profile.py 
	mv bin/profiling-results.* ./

#      ------------ -- 
#
TEST_$d             += test_$d
.PHONY:                test_$d

test_$d:
	@$(call log_line,info,$@,Starting tests..)
	@\
	PYTHONPATH=$$PYTHONPATH:src/py:test/py;\
	TEST_PY=test/py/main.py;TEST_LIB=uriref;\
    $(test-python)


#      ------------ -- 
#
# TODO: generate docs
#DOC                 += RST+=' '$/ReadMe.rst
#DOC                 += TXT+=' '$/doc/rfc2396.txt' '$/doc/rfc3986.txt


#      ------------ -- 
#
CLN_$d              := \
	$(shell find $/ -name '.coverage') \
	$(shell find $/ -name '*.pyc') \
	$(shell find $/htmlcov -type f)


#      ------------ -- 

# 'make dep' prerequisites
SRC                 += $(SRC_$d)
DEP                 += $(DEP_$d)
# 'make stat'
DMK                 += $(DMK_$d)
# 'make build'
TRGT                += $(TRGT_$d)
# 'make test'
TEST                += $(TEST_$d)
# 'make clean'
CLN                 += $(CLN_$d)

#      ------------ -- 

#DIR                 := $/mydir
#include                $(call rules,$(DIR)/)

#      ------------ -- 
#
include                $(MK_SHARE)Core/Main.dirstack-pop.mk
# vim:noet:
