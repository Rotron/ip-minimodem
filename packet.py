#!/usr/bin/env python3

from PyCRC.CRC16 import CRC16
from cobs import cobs
from reedsolo import RSCodec

class Packetizer():
    def __init__(self, callsign):
        self.sequenceId = 0
        callsignLen = 6 if len(callsign) > 6 else len(callsign)
        self.callsign = bytes(callsign[:callsignLen].upper() + ' '*(6-len(callsign)), 'utf-8')
        self.rs = RSCodec(16)

    def createPacket(self, data=b''):
        packet = bytearray()

        # Header (1 byte - added after padding)
        # Callsign (6 bytes)
        packet += self.callsign

        # Length (2 bytes)
        dataLen = len(data)
        packet += bytes([(dataLen & 0xFF00) >> 8, dataLen & 0xFF])

        # Sequence ID (2 bytes)
        packet += bytes([(self.sequenceId & 0xFF00) >> 8, self.sequenceId & 0xFF])
        self.sequenceId = (self.sequenceId + 1) & 0xFFFF

        # payload (unknown length)
        packet += data

        # CRC and footer (CRC MSB, CRC LSB) (2 bytes)
        crcCalculator = CRC16()
        crc = crcCalculator.calculate(bytes(packet))
        packet += bytes([(crc & 0xFF00) >> 8, crc & 0xFF])

        cobs_packet = cobs.encode(packet)
        encoded_packet = self.rs.encode(cobs_packet)
        return bytes([0]) + encoded_packet + bytes([0])
