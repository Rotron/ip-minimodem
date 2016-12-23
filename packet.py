#!/usr/bin/env python3

from PyCRC.CRC16 import CRC16

class Packetizer():
    def __init__(self):
        self.sequenceId = 0

    def createPacket(self, data=b''):
        packet = bytearray()

        # Header (1 byte)
        packet += bytes([0x55])

        # Callsign (6 bytes)
        packet += b'ON4SEB'

        # Sequence ID (2 bytes)
        packet += bytes([(self.sequenceId & 0xFF00) >> 8, self.sequenceId & 0xFF])
        self.sequenceId = (self.sequenceId + 1) & 0xFFFF

        # payload (unknown length)
        packet += data

        # CRC and footer (CRC MSB, CRC LSB, end of packet) (3 bytes)
        crcCalculator = CRC16()
        crc = crcCalculator.calculate(bytes(packet))
        packet += bytes([(crc & 0xFF00) >> 8, crc & 0xFF, 0xAA])

        return packet
