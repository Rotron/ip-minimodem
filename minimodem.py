#!/usr/bin/env python3
import subprocess
import select
from collections import deque
import time

class minimodem_wrapper:
    def __receiveProcess(self):
        return subprocess.Popen('/home/seb/devel/minimodem/src/minimodem -r ' +
        str(self.speed),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    def __transmitProcess(self):
        return subprocess.Popen('/home/seb/devel/minimodem/src/minimodem -t ' +
             str(self.speed),
            shell=True,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def processRxPacketTags(self):
        line = self.rxHandler.stderr.readline()
        if line.startswith(b'### CARRIER '):
            self.inPacket = True
            self.packet = bytearray()
            print('Beginning of incoming packet')
        elif line.startswith(b'### NOCARRIER '):
            self.inPacket = False
            print('End of incoming packet '+str(self.packet))

    def processRxPacketData(self):
        data = self.rxHandler.stdout.read(1)
        self.packet += data

    def processTxPackets(self):
        if len(self.txPackets) > 0 and not self.inPacket:
            time.sleep(0.1)
            self.transmit = True
            self.txHandler.stdin.write(self.txPackets[0])
            self.txHandler.stdin.flush()
            self.txPackets.popleft()

    def processEndOfTransmission(self):
        line = self.txHandler.stderr.readline()
        if line.startswith(b'### EOM'):
            print('End of transmission')
            self.transmit = False

    def send(self, txData):
        if len(self.txPackets) < 10:
            self.txPackets.append(txData)

    def __init__(self, speed = 200):
        self.speed = speed
        self.packet = bytearray()
        self.txPackets = deque()
        self.inPacket = False
        self.transmit = False

        self.txHandler = self.__transmitProcess()
        self.rxHandler = self.__receiveProcess()
