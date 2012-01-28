include                $(MK_SHARE)Core/Main.dirstack.mk
MK_$d               := $/Rules.mk
MK                  += $(MK_$d)
#
#      ------------ -- 

SRC_$d              := $/uriref/__init__.py

TRGT_$d             := \
	$/profiling_urllib-comparison_.py

DEP_$d              :=
DMK_$d              :=

define python-urllib-profile 
	if test ! -e $(BUILD); then mkdir $(BUILD); fi
	python test/py/profile.py -csv | tee $@
endef

#      ------------ -- 
#
TEST_$d             += profile_$d
.PHONY:                profile_$d

profile_$d:: $/doc/stdlib-comparison.png $/doc/stdlib-comparison.svg

$/doc/stdlib-comparison.svg $/doc/stdlib-comparison.png: $Bstdlib-comparison.csv

$Bstdlib-comparison.csv: $(SRC_$d) $/Rules.mk $/Makefile
	@$(call log_line,info,$@,..);\
	$(python-urllib-profile)
	@$(call log_line,ok,$@)

$/doc/%.svg $/doc/%.png: DIR := $/
$/doc/%.svg $/doc/%.png: $B%.csv
	@$(call log_line,info,$@,..);\
	cd $(DIR); python bin/plot-profile.py $< $(@D)/$*
	@$(call log_line,ok,$@)

#      ------------ -- 
#
TEST_$d             += test_$d
.PHONY:                test_$d

test_$d: DIR := $/
test_$d:
	@$(call log_line,info,$@,Starting tests..)
	@\
	cd $(DIR);\
	PYTHONPATH=$$PYTHONPATH:src/py:test/py;\
	TEST_PY=test/py/main.py;TEST_LIB=uriref;\
    $(test-python);
	@\
	cd $(DIR);\
    [ -e htmlcov ] && mv htmlcov doc && rm .coverage;\
    [ -e uriref_testreport.html ] && mv uriref_testreport.html doc;
	@$(call log_line,ok,$@)


#      ------------ -- 
#
# TODO: generate docs
#DOC                 += RST+=' '$/ReadMe.rst
#DOC                 += TXT+=' '$/doc/rfc2396.txt' '$/doc/rfc3986.txt


#      ------------ -- 
#
CLN_$d              := \
	$(shell find $/ -name '*.pyc') \
	$(wildcard .coverage htmlcov dist MANIFEST)


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
