#!/usr/bin/env python
# coding: UTF-8

import socket
import struct
import subprocess
import sys
from telnetlib import Telnet
from shellcraft import *


class Remote(object):

    def __init__(self, ip_addr, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2.0)
        self.sock.connect((ip_addr, port))

    def __del__(self):
        self.sock.shutdown(socket.SHUT_WR)

    def close(self):
        self.__del__()

    def interact(self):
        t = Telnet()
        t.sock = self.sock
        try:
            t.interact()
        finally:
            close(s)

    def recvall(self):
        return self.sock.recv(1024)

    def recvuntil(self, word):
        res = ''
        while not res.endswith(word):
            res += self.sock.recv(1)
        return res

    def recvline(self):
        return self.recvuntil('\n')

    def send(self, req):
        self.sock.sendall(req)

    def sendline(self, req):
        self.send(req + '\n')


class Local(object):

    def __init__(self, program):
        if type(program) == str:
            self.proc = subprocess.Popen([program], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        elif type(program) == list:
            self.proc = subprocess.Popen(program, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def __del__(self):
        if self.proc.poll() is None:
            self.proc.terminate()

    def close(self):
        self.__del__()

    def interact(self):
        import threading
        go = threading.Event()

        def recv_thread():
            while not go.isSet():
                try:
                    cur = self.recv()
                    cur = cur.replace('\r\n', '\n')
                    if cur:
                        sys.stdout.write(cur)
                        sys.stdout.flush()

                except EOFError:
                    self.info('Got EOF while reading in interactive')
                    break

        t = context.Thread(target=recv_thread)
        t.daemon = True
        t.start()

        try:
            while not go.isSet():
                data = sys.stdin.read(1)

                if data:
                    try:
                        self.send(data)
                    except EOFError:
                        go.set()

                else:
                    go.set()

        except KeyboardInterrupt:
            self.info('Interrupted')
            go.set()

        while t.is_alive():
            t.join(timeout=0.1)

    def recvall(self):
        return self.proc.stdout.read()

    def recvuntil(self, word):
        res = ''
        while not res.endswith(word):
            res += self.proc.stdout.read(1)
        return res

    def recvline(self):
        return self.recvuntil('\n')

    def send(self, req):
        self.proc.stdin.write(req)

    def sendline(self, req):
        self.send(req + '\n')


def p32(number):
    return struct.pack('<I', number & 0xffffffff)


def p64(number):
    return struct.pack('<Q', number & 0xffffffffffffffff)


def u32(number):
    return struct.unpack('<I', number)[0]


def u64(number):
    return struct.unpack('<Q', number)[0]


def xor(x, y):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(x, y))
