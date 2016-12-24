#!/usr/bin/env python3

from PyCRC.CRC16 import CRC16

class ReceivePacket():
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

        # Get packet length
        packetLen = packet[7] << 8 | packet[8]

        # Origin callsign
        originCallsign = packet[1:7].decode('utf-8').strip()

        # Check for missing packets
        if packetValid:
            expectedSequenceId = (self.sequenceId + 1) & 0xFFFF
            packetSequenceId = packet[9] << 8 | packet[10]
            if expectedSequenceId != packetSequenceId:
                self.packetLost += 1
            self.sequenceId = packetSequenceId
            payload = packet[12:-3]
            return (originCallsign, packetLen, packetSequenceId, payload)

        return None
