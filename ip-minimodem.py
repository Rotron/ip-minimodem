#!/usr/bin/env python3
from minimodem import *
import select
from threading import Thread
import time
import subprocess
import sys

from packet import *

pkt = Packetizer()

def testTransmit():
    while True:
        data = b'Hello World'
        packet = pkt.createPacket(data)
        mm.send(packet)
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
