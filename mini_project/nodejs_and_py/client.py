#!/usr/bin/python
__author__ = 'deevarvar'

import sys
import socket

#copied from http://code.activestate.com/recipes/408859/
def recv_basic(the_socket):
    total_data=[]
    while True:
        data = the_socket.recv(8192)
        print 'data in function is '+data
        if not data: break
        total_data.append(data)
    return ''.join(total_data)



uds = '/tmp/test.sock'
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    sock.connect(uds)
except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)


while 1:
    cmd = raw_input('enter command:')
    print 'cmd is ' + cmd
    sock.sendall(cmd)

    server_data = sock.recv(8192)
    print 'data from server is '+ server_data
    if cmd == 'close':
        print 'close the socket'
        sock.close()
        sys.exit(1)