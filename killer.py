#!/usr/bin/env python
# coding: UTF-8

import socket
import struct


class Remote(object):
    def __init__(self, ip_addr, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2.0)
        self.sock.connect((ip_addr, port))

    def __del__(self):
        self.sock.shutdown(socket.SHUT_WR)

    def send(self, req):
        self.sock.sendall(req)

    def sendline(self, req):
        self.sock.sendall(req + '\n')

    def recvuntil(self, word):
        res = ''
        while not res.endswith(word):
            res += self.sock.recv(1)
        return res

    def recvline(self):
        return self.recvuntil('\n')


def p32(number):
    return struct.pack('<I', number & 0xffffffff)


def p64(number):
    return struct.pack('<Q', number & 0xffffffffffffffff)


def u32(number):
    return struct.unpack('<I', number)[0]


def u64(number):
    return struct.unpack('<Q', number)[0]
