#!/usr/bin/env python
# coding: UTF-8

from killer import *

l = Local('ls')
res = l.recvall()
print(res)

l2 = Local(['sed', '-l', 's/a/x/g'])
l2.sendline('sample')
res2 = l2.recvline()
print(res2)
