#!/usr/bin/env python3
from minimodem import *
import select
import time
import subprocess
import sys
import configparser

from packet import *
from tunInterface import *

def dispatchIncomingPacketsToTun(minimodem, tun):
    packet = minimodem.getIncomingPackets()
    if packet[0] > 0:
        print('Sending to TUN : '+str(packet[1]))
        tun.writePacket(packet[1][3])

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    
    pkt = Packetizer(callsign=config['radio']['callsign'])

    mm = minimodem_wrapper(speed = 1200, interface=config['radio']['audiodevice'])
    tun = tunInterface(config = config['tun'])

    while(True):
        readers, writers, _ = select.select([mm.rxHandler.stdout, mm.rxHandler.stderr, mm.txHandler.stderr, tun.tun], [], [], 5)
        if mm.rxHandler.stderr in readers:
            mm.processRxPacketTags()

        if mm.txHandler.stderr in readers:
            mm.processEndOfTransmission()

        if mm.rxHandler.stdout in readers:
            mm.processRxPacketData()

        if tun.tun in readers:
            data = tun.getPacket()
            packet = pkt.createPacket(data)
            print ("Sending to Radio: "+str(packet))
            mm.send(packet)

        # Send data on timeout
        mm.processTxPackets()

        # Dispatch incoming packets to tun
        dispatchIncomingPacketsToTun(mm, tun)
