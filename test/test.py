# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test_project(dut):

    dut._log.info("Start 8-bit counter test")

    # 10 us period
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Initial values
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

   # 1. reset case

    dut._log.info("Testing: reset")

    dut.rst_n.value = 0

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.uo_out.value == 0

    dut.rst_n.value = 1

    # 2. allow normal counting from 0-2

    dut._log.info("Testing: counting")

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.uo_out.value == 1

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.uo_out.value == 2

    # 3. test synchronous load (12) and count up 

    dut._log.info("Testing: synchronous load")

    dut.uio_in.value = 12

    # enable load
    dut.ui_in.value = 0b00000001

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.uo_out.value == 12

    # 4. count upwards from load value

    dut._log.info("Testing: count after load")

    dut.ui_in.value = 0

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.uo_out.value == 13

    # 5. test tri state for output enable = 0 (hi Z)

    dut._log.info("Testing: output enable")

    # for oe = 0, uio pins should not be driven (only uo)
    assert dut.uio_oe.value == 0x00

    # set oe
    dut.ui_in.value = 0b00000010

    await Timer(1, unit="ns")

    assert dut.uio_oe.value == 0xFF
    assert dut.uio_out.value == 13

    # oe off again
    dut.ui_in.value = 0

    await Timer(1, unit="ns")

    assert dut.uio_oe.value == 0x00
