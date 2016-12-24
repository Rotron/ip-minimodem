#!/bin/bash

ip route del table local 192.168.7.2 dev ham1
ip route add 192.168.7.2 via 192.168.7.1
ip route flush cache
 
