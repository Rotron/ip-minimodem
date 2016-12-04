#!/usr/bin/env python3
from minimodem import *
import select
from threading import Thread
import time

def testTransmit():
    while True:
        data = bytes([0x55, 0])+b'ON4SEB'+bytes([0, 0, 0xAA])
        mm.send(data)
        time.sleep(10)

if __name__ == '__main__':
    mm = minimodem_wrapper(speed = 75)

    transmitThd = Thread(target=testTransmit)
    transmitThd.start()

    while(True):
        readers, writers, _ = select.select([mm.rxHandler.stdout, mm.rxHandler.stderr, mm.txHandler.stderr], [mm.txHandler.stdin], [])
        if mm.rxHandler.stderr in readers:
            mm.processRxPacketTags()

        if mm.txHandler.stderr in readers:
            mm.processEndOfTransmission()

        if mm.rxHandler.stdout in readers:
            mm.processRxPacketData()

        if mm.txHandler.stdin in writers:
            mm.processTxPackets()
