import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

segments = [ 63, 6, 91, 79, 102, 109, 124, 7, 127, 103 ]

async def flop_data(dut, x):
    # flop serial done clear
    dut._log.info("flop serial done clear")
    dut.io_in.value = 8
    await Timer(100, units='ns')
    dut.io_in.value = 9

    # idle clock
    dut._log.info("idle clock")
    dut.io_in.value = 0
    await Timer(100, units='ns')
    dut.io_in.value = 1
    await Timer(100, units='ns')

    dut.io_in.value = 0
    await Timer(500, units='ns')
    dut._log.info("done idle clock")


    dut._log.info("flopping serial value {}".format(x))
    for i in range(28):
        bitVal = 3 if (x & (1 << (28 - i - 1))) else 2;

        # flop a 1
        dut._log.info("flop serial bit{}".format(bitVal))
        dut.io_in.value = bitVal
        await Timer(100, units='ns')
        dut.io_in.value = bitVal + 1
        await Timer(100, units='ns')

    # flop serial done
    dut._log.info("flop serial done")
    dut.io_in.value = 8
    await Timer(100, units='ns')
    dut.io_in.value = 9
    await Timer(100, units='ns')
    dut.io_in.value = 16
    await Timer(100, units='ns')
    dut.io_in.value = 17
    await Timer(100, units='ns')

    # flop serial done clear
    dut._log.info("flop serial done clear")
    dut.io_in.value = 8
    await Timer(100, units='ns')
    dut.io_in.value = 9


@cocotb.test()
async def test_7seg(dut):
    dut._log.info("start")
    # clock = Clock(dut.clk, 10, units="us")
    # cocotb.start_soon(clock.start())

    await Timer(100, units='ns')

    dut._log.info("reset")
    dut.io_in.value = 0xfe
    await Timer(100, units='ns')

    # idle clock
    dut._log.info("idle clock for reset of reset")
    dut.io_in.value = 0
    await Timer(100, units='ns')
    dut.io_in.value = 1
    await Timer(100, units='ns')

    for i in range(20):
        dut.io_in.value = 0xff
        await Timer(100, units='ns')

        dut.io_in.value = 0xfe
        await Timer(100, units='ns')

    # idle clock
    dut._log.info("idle clock")
    dut.io_in.value = 0
    await Timer(100, units='ns')
    dut.io_in.value = 1
    await Timer(100, units='ns')

    for i in range(10):
        await flop_data(dut, i)

    dut._log.info("flop idle")
    for i in range(10):
        # dut._log.info("check segment {}".format(i))
        dut.io_in.value = 0
        await Timer(100, units='ns')
        dut.io_in.value = 1
        await Timer(100, units='ns')
        # assert int(dut.segments.value) == segments[i]
