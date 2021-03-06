#!/usr/bin/env python3

from receivePacket import *
from collections import deque

class Framer():
    def __init__(self):
        self.packet = bytearray()
        self.packetFifo = deque()
        self.depack = ReceivePacket()

    def clearBuffers(self):
        self.packet = bytearray()

    def processInput(self, data):
        if data != b'\x00':
            self.packet += data
        else:
            extractedPacket = self.depack.unpackData(self.packet)
            if extractedPacket != None:
                #print('Packet OK '+str(extractedPacket))
                self.packetFifo.append(extractedPacket)
            self.packet = bytearray()

    def incomingPackets(self):
        if len(self.packetFifo) > 0:
            return self.packetFifo.popleft()
        else:
            return None

    def incomingPacketsCount(self):
        return len(self.packetFifo)
