# Makefile
# See https://docs.cocotb.org/en/stable/quickstart.html for more info

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog
EMILIAN_TEMPLATE_ROOT = ../../sc-rv-tt03/hw/gen

EMILIAN_LOCAL_DEV ?= no
EMILIAN_SV2V_FLAGS ?= -DEMILIAN_ADD_BUFS=y

# normal simulation
ifneq ($(GATES),yes)

# this is the only part you should need to modify:
VERILOG_SOURCES += $(PWD)/tb.v $(PWD)/rv_block1.v 

else

# gate level simulation requires some extra setup, you shouldn't need to touch this
COMPILE_ARGS    += -DGL_TEST
COMPILE_ARGS    += -DFUNCTIONAL
COMPILE_ARGS    += -DUSE_POWER_PINS
COMPILE_ARGS    += -DSIM
COMPILE_ARGS    += -DUNIT_DELAY=#1
VERILOG_SOURCES += $(PDK_ROOT)/sky130B/libs.ref/sky130_fd_sc_hd/verilog/primitives.v
VERILOG_SOURCES += $(PDK_ROOT)/sky130B/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v

# this gets copied in by the GDS action workflow
VERILOG_SOURCES += $(PWD)/tb.v $(PWD)/gate_level_netlist.v
endif

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = tb

# MODULE is the basename of the Python test file
MODULE = test

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

ifeq ($(EMILIAN_LOCAL_DEV),yes)

# Regenerate plain Verilog from SystemVerilog on local development.
# This also gets submitted to Github.
gen: $(EMILIAN_TEMPLATE_ROOT)/ScrivCpu.v $(EMILIAN_TEMPLATE_ROOT)/ScrivBlackbox.v
	sv2v $(EMILIAN_SV2V_FLAGS) $(EMILIAN_TEMPLATE_ROOT)/ScrivCpu.v \
			$(EMILIAN_TEMPLATE_ROOT)/ScrivBlackbox.v > $(PWD)/rv_block1.v
	sed -i "s/module ScrivCpu/module diferential_rvb1/" rv_block1.v
	sed -i "s/module Scriv/module Scriv1/" rv_block1.v
	sed -i "s/ScrivMailbox/Scriv1Mailbox/" rv_block1.v
	sed -i "s/ScrivBB_/Scriv1BB_/" rv_block1.v

endif
