#!/usr/bin/python
__author__ = 'deevarvar'

import sys
import socket
import threading
import os
import select
import errno
import json
import thread

#copied from http://code.activestate.com/recipes/408859/
def recv_basic(the_socket):
    total_data=[]
    while True:
        data = the_socket.recv(8192)
        print 'data in function is '+data
        if not data: break
        total_data.append(data)
    return ''.join(total_data)



uds = '/tmp/entry.sock'


#two threads: one thread read input from socket, the other write cmd to socket

thread_list = []

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    sock.connect(uds)
except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)

write_exit = False
read_exit = False

def write_cmd():
    print 'write thread ident is ', threading.current_thread()
    while write_exit is False:
        cmd = raw_input('enter command:')
        print 'cmd is ' + cmd
        sock.sendall(cmd)


def read_cmd():
    fds = [sock]
    print 'read thread ident is ', threading.current_thread()
    global read_exit
    while read_exit is False:

        reads, _, _ = select.select(fds, [], [], 0)
        if 0 < len(reads):

            try:
                data = os.read(reads[0].fileno(), 512)
                if data:
                    print "from server data is ", data
                    #try parse data
                    try:
                        jata = json.loads(data)
                        print 'path is ', jata['path']
                        print 'exit is ',jata['exit']
                        if jata['exit'] == "True":
                            read_exit = True

                    except ValueError,e:
                        print 'error is ', e
            except OSError as err:
                if err.errno != errno.EAGAIN and err.errno != errno.EWOULDBLOCK:
                    raise  # something else has happened -- better reraise
    print 'exit thread loop'

read_thread = threading.Thread(target=read_cmd)
write_thread = threading.Thread(target=write_cmd)

thread_list.append(read_thread)
thread_list.append(write_thread)

for thread in thread_list:
    thread.daemon = True
    thread.start()


for thread in thread_list:
    thread.join()