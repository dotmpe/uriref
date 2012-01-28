# Non-recursive makefile
# Example of mkdoc usage, see git://github.org/dotmpe/mkdoc

DOMAIN              := mpe

BUILD               := .build/
DIR                 := .

SRC_PATH            := /src/
PROJ_PATH           := /srv/project-$(DOMAIN)/
MK_ROOT             := $(PROJ_PATH)mkdoc/
MK_SHARE            := $(MK_ROOT)usr/share/mkdoc/

ifneq ($(VERBOSE), )
$(info mkdocs:DIR=$(DIR))
$(info mkdocs:BUILD=$(BUILD))

$(info mkdocs:MK_ROOT=$(MK_ROOT))
$(info mkdocs:MK_SHARE=$(MK_SHARE))
endif

#      ------------ -- 

include                $(MK_SHARE)Core/Main.mk
ifneq ($(VERBOSE), )
$(info $(shell $(ll) header "mkdoc" "Core script loaded, reading shares" ))
endif

#include                \
                       $(MK_SHARE)<package_name>/Main.mk \

#      ------------ -- 

MK                  += $(DIR)/Makefile

ifneq ($(VERBOSE), )
$(info $(shell $(ll) header "mkdoc" "Reading shared default rules" ))
endif

#include                \
                       $(MK_SHARE)<package_name>/Rules.default.mk \

#      ------------ -- 

ifneq ($(VERBOSE), )
$(info $(shell $(ll) header "mkdoc" "Reading local rules" ))
endif

# Include specific rules and set SRC, DEP, TRGT and CLN variables.
#
include                $(call rules,$(DIR)/) 

# Now at last set standard targets and prerequisites
#
include                $(MK_SHARE)Core/Rules.default.mk

#      ------------ -- 

$(info $(shell $(ll) OK "mkdoc" "starting 'make $(MAKECMDGOALS)'.." ))

# vim:ft=make:
