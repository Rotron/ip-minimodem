#!/usr/bin/env python3

from PyCRC.CRC16 import CRC16
from cobs import cobs

class ReceivePacket():
    def __init__(self):
        self.sequenceId = 0
        self.packetLost = 0

    def unpackData(self, inPacket=b''):
        crcCalculator = CRC16()
        packetValid = False

        try:
            packet = cobs.decode(inPacket)

            crc = crcCalculator.calculate(bytes(packet[:-2]))

            # Check CRC validity
            if ((crc & 0xFF00) >> 8) == packet[-2] and (crc & 0xFF) == packet[-1]:
                packetValid = True
            # Get packet length
            packetLen = packet[6] << 8 | packet[7]

            # Origin callsign
            originCallsign = packet[0:6].decode('utf-8').strip()

            # Check for missing packets
            if packetValid:
                expectedSequenceId = (self.sequenceId + 1) & 0xFFFF
                packetSequenceId = packet[8] << 8 | packet[9]
                if expectedSequenceId != packetSequenceId:
                    self.packetLost += 1
                self.sequenceId = packetSequenceId
                payload = packet[10:-3]
                return (originCallsign, packetLen, packetSequenceId, payload)
        except:
            #print('Decode error '+str(inPacket))
            return None
