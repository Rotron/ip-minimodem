#!/usr/bin/env python3
from minimodem import *
import select
from threading import Thread
import time
import subprocess
import sys
from PyCRC.CRC16 import CRC16

def testTransmit():
    while True:
        data = bytes([0x55, 0])+bytes('ON4SEB Hello World','utf-8')
        crcCalc = CRC16()
        packetCrc = crcCalc.calculate(data)
        # Append end of packet
        data += bytes([(packetCrc & 0xFF00) >> 8, packetCrc & 0xFF, 0xAA])
        mm.send(data)
        time.sleep(5)

if __name__ == '__main__':
    mm = minimodem_wrapper(speed = 1200, interface=sys.argv[1])

    transmitThd = Thread(target=testTransmit)
    transmitThd.start()

    while(True):
        readers, writers, _ = select.select([mm.rxHandler.stdout, mm.rxHandler.stderr, mm.txHandler.stderr], [], [], 5)
        if mm.rxHandler.stderr in readers:
            mm.processRxPacketTags()

        if mm.txHandler.stderr in readers:
            mm.processEndOfTransmission()

        if mm.rxHandler.stdout in readers:
            mm.processRxPacketData()

        # Send data on timeout
        mm.processTxPackets()
