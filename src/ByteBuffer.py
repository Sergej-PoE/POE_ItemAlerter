#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

'''
sku wrote this program. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.
'''


def makeDword(data, endian):
    if endian == ByteBuffer.LITTLE_ENDIAN:
        return data[0] | data[1] << 8 | data[2] << 16 | data[3] << 24
    else:
        return data[3] | data[2] << 8 | data[1] << 16 | data[0] << 24

class ByteBuffer(object):

    LITTLE_ENDIAN = 1
    BIG_ENDIAN = 2

    def __init__(self, data):
        self.data = data
        self.position = 0
        self.length = len(data)
        self.endian = ByteBuffer.LITTLE_ENDIAN

    def setEndian(self, endian):
        self.endian = endian

    def getRemainingBytes(self):
        return self.length - self.position

    def nextByte(self):
        assert self.getRemainingBytes() >= 1
        byte = self.data[self.position]
        self.position += 1
        return byte

    def nextDword(self, endian=None):
        assert self.getRemainingBytes() >= 4
        dword = self.data[self.position:self.position+4]
        self.position += 4
        return makeDword(dword, self.endian if not endian else endian)