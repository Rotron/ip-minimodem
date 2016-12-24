#!/usr/bin/env python3

from PyCRC.CRC16 import CRC16

class Packetizer():
    def __init__(self):
        self.sequenceId = 0

    def createPacket(self, data=b''):
        packet = bytearray()

        # Header (1 byte)
        packet += bytes([0x7E])

        # Callsign (6 bytes)
        packet += b'ON4SEB'

        # Length (2 bytes)
        dataLen = len(data)
        packet += bytes([(dataLen & 0xFF00) >> 8, dataLen & 0xFF])

        # Sequence ID (2 bytes)
        packet += bytes([(self.sequenceId & 0xFF00) >> 8, self.sequenceId & 0xFF])
        self.sequenceId = (self.sequenceId + 1) & 0xFFFF

        # Add end of header (1 byte)
        packet += bytes([0x55])

        # payload (unknown length)
        packet += data

        # CRC and footer (CRC MSB, CRC LSB, end of packet) (3 bytes)
        crcCalculator = CRC16()
        crc = crcCalculator.calculate(bytes(packet))
        packet += bytes([(crc & 0xFF00) >> 8, crc & 0xFF, 0xAA])

        return packet

class Depacketizer():
    def __init__(self):
        self.sequenceId = 0
        self.packetLost = 0

    def unpackData(self, packet=b''):
        crcCalculator = CRC16()
        packetValid = False
        crc = crcCalculator.calculate(bytes(packet[:-3]))

        # Check CRC validity
        if ((crc & 0xFF00) >> 8) == packet[-3] and (crc & 0xFF) == packet[-2]:
            packetValid = True

        # Check for missing packets
        if packetValid:
            expectedSequenceId = (self.sequenceId + 1) & 0xFFFF
            packetSequenceId = packet[7] << 8 | packet[8]
            if expectedSequenceId != packetSequenceId:
                self.packetLost += 1
            self.sequenceId = packetSequenceId

        return packetValid
