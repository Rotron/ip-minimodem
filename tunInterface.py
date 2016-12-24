#!/usr/bin/env python3
import fcntl
import os
import struct
import subprocess
import select

# Some constants used to ioctl the device file. I got them by a simple C
# program.
TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

class tunInterface():
    def __init__(self, config):
        ifName = config['interfacename']
        ipAddr = config['ipaddress']

        # Open TUN device file.
        self.tun = open('/dev/net/tun', 'r+b', buffering=0)

        # Tell it we want a TUN device named tun0.
        ifr = struct.pack('16sH', bytes(ifName, 'utf-8'), IFF_TUN | IFF_NO_PI)
        fcntl.ioctl(self.tun, TUNSETIFF, ifr)

        # Optionally, we want it be accessed by the normal user.
        fcntl.ioctl(self.tun, TUNSETOWNER, 1000)

        # Bring it up and assign addresses.
        subprocess.check_call('ifconfig ' + ifName + ' '+ipAddr+'/24 up',
shell=True)

    def getPacket():
        return self.tun.read(512)
