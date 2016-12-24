#!/usr/bin/env python3

from receivePacket import *
from collections import deque

IDLE, HEADER, DATA ,CRC = range(4)

depack = ReceivePacket()

class Framer():
    def __init__(self):
        self.state = IDLE
        self.fieldLength = 0
        self.packet = bytearray()
        self.packetFifo = deque()

    def clearBuffers(self):
        self.packet = bytearray()

    def processInput(self, data):
        if self.state == IDLE:
            if data == bytes([0x7E]):
                self.clearBuffers()
                self.packet += data
                self.state = HEADER
                self.fieldLength = 11
        elif self.state == HEADER:
            self.packet += data
            self.fieldLength -= 1
            if self.fieldLength == 0:
                if data == bytes([0x55]):
                    self.fieldLength = (self.packet[7] << 8) + self.packet[8]
                    self.state = DATA
                else:
                    self.state = IDLE
        elif self.state == DATA:
            self.packet += data
            self.fieldLength -= 1
            if self.fieldLength == 0:
                self.state = CRC
                self.fieldLength = 3
        elif self.state == CRC:
            self.packet += data
            self.fieldLength -= 1
            if self.fieldLength == 0:
                unpackedData = depack.unpackData(self.packet)
                if unpackedData:
                    self.packetFifo.append(unpackedData)
                if data != bytes([0xAA]):
                    print('Framing error: invalid end of packet')
                self.state = IDLE

    def incomingPackets(self):
        if len(self.packetFifo) > 0:
            return self.packetFifo.popleft()
        else:
            return None

    def incomingPacketsCount(self):
        return len(self.packetFifo)
