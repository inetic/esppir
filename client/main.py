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

    def delay_generator():
        i = 0
        while True:
          if   i < 30:  yield 0.02
          elif i < 50:  yield 0.1
          elif i < 100: yield 0.5
          elif i < 150: yield 1
          elif i < 200: yield 2
          else:         yield 5
          i += 1

    delay = delay_generator();

    while True:
      sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
      sock.settimeout(delay.next())
      data = []
      addr = []
      try:
          data, addr = sock.recvfrom(BUFFER_SIZE)
          s = data.split(':', 1)

          if (len(s) >= 1 and s[0] == key):
              print(" found")
              if (len(s) == 2): return s[1]
              else: return []

      except socket.timeout:
          sys.stdout.write('.')
          sys.stdout.flush()
          pass


def extract(key, src):
    entries = src.split(' ')
    for e in entries:
        kv = e.split(':', 1)
        if (len(kv) == 2 and kv[0] == key): return kv[1]



if __name__ == '__main__':
    try:
        while True:
            print("Searching for esppir")
            ep_str = discover('esppir')
            ep = parse_ep(ep_str)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Connecting")
            s.connect(ep)

            s.settimeout(5) # 5 seconds
            print("Connected")

            while True:
                try:
                    data = s.recv(BUFFER_SIZE)
                    print("Received: " + extract('pir-value', data))
                except socket.timeout:
                    break

            print("Closing");
            s.close()
    except KeyboardInterrupt:
        pass


