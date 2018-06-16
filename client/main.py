#!/usr/bin/env python

import socket
import time
import sys

BUFFER_SIZE = 1024

def parse_ep(s):
    ip,port = s.split(':')
    return (ip, int(port))

def discover(key):
  UDP_IP = "192.168.0.255"
  UDP_PORT = 3210
  MESSAGE = "discover"
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  sock.bind(("0.0.0.0", 0))
  def calculate_delay(i):
      if i < 30:  return 0.02
      if i < 50:  return 0.1
      if i < 100: return 0.5
      if i < 200: return 1
      return 2
  i = 0
  while True:
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    sock.settimeout(calculate_delay(i))
    data = []
    addr = []
    try:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        s = data.split(':', 1)

        if (len(s) >= 1 and s[0] == key):
            if (len(s) == 2):
                return s[1]
            else:
                return []
    except socket.timeout:
        sys.stdout.write('.')
        sys.stdout.flush()
        pass

    i += 1

if __name__ == '__main__':
    ep_str = discover('esppir')
    ep = parse_ep(ep_str)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting")
    s.connect(ep)

    print("Connected")

    while True:
        data = s.recv(BUFFER_SIZE)
        print("Received: " + data)

    s.close()

