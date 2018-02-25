#!/usr/bin/env python3

from unicorn import *
from unicorn.arm_const import *
import struct, math

firmware = open("mcu2.bin", 'rb').read()
app_image = 0x8004000
ram = 0x20000000
ram_size = 64*1024

u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
u.mem_map(app_image, len(firmware))
u.mem_write(app_image, firmware)
u.mem_map(ram, ram_size)
u.reg_write(UC_ARM_REG_SP, ram + ram_size - 4)

def try_call_site(addr, r0, r1=0, r2=0, r3=0):
	u.reg_write(UC_ARM_REG_R0, r0)
	u.reg_write(UC_ARM_REG_R1, r1)
	u.reg_write(UC_ARM_REG_R2, r2)
	u.reg_write(UC_ARM_REG_R3, r3)
	u.emu_start(addr|1, addr+4)
	return u.reg_read(UC_ARM_REG_R0), u.reg_read(UC_ARM_REG_R1)

def unpack_float64(r0, r1):
	return struct.unpack("d", struct.pack("<II", r0, r1))[0]

def pack_float64(f):
	return struct.unpack("<II", struct.pack("d", f))

def unpack_float32(r0, r1=0):
	return struct.unpack("f", struct.pack("<I", r0))[0]

def pack_float32(f):
	return struct.unpack("<I", struct.pack("f", f))


for i in range(50):
	print()
	print(i)
	a = 1
	b = 1 + i*0.1
	result = unpack_float32(*try_call_site(0x800a4ee, *(pack_float32(a) + pack_float32(b))))
	print(a, b, result)
