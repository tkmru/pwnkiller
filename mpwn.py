#!/usr/bin/env python
# coding: UTF-8

import socket
import struct


def connect(ip_addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_addr, port))
    return s


def p32(number):
    return struct.pack("<I", number & 0xffffffff)


def p64(number):
    return struct.pack("<Q", number & 0xffffffffffffffff)


def u32(number):
    return struct.unpack('<I', number)[0]


def u64(number):
    return struct.unpack("<Q", number)[0]
