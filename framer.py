#!/usr/bin/env python3

IDLE, HEADER, DATA ,CRC = range(4)

class Framer():
    def __init__(self):
        self.state = IDLE
        self.fieldLength = 0
        self.packet = bytearray()

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
                print ('packet received : '+str(self.packet))
                if data != bytes([0xAA]):
                    print('Framing error: invalid end of packet')
                self.state = IDLE

        #print (str(self.state) + ' Processing data ' + str(data))
