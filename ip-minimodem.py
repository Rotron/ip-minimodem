#!/usr/bin/env python3
from minimodem import *
import select
from threading import Thread
import time
import subprocess
import sys
import configparser

from packet import *
from tunInterface import *

pkt = Packetizer()
depkt = Depacketizer()

def testTransmit():
    while True:
        data = b'Hello World'
        packet = pkt.createPacket(data)
        depkt.unpackData(packet)
        mm.send(packet)
        time.sleep(5)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    mm = minimodem_wrapper(speed = 1200, interface=config['radio']['audiodevice'])
    tun = tunInterface(config = config['tun'])

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
