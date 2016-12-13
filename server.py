#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 13:33:29 2016

@author: arhy
"""

# This program was created by Anwar Hidayat.
# This program was intended to fulfill an assignment of a subject I took.
# Basically this program is a server for the client specified and created on a different folder.
# I hope I don't forget its mechanism in the future.

import socket
import select
import sys
import os
from os import listdir

# Specifying the necessary data for the server to run.

fload = file('httpserver.conf')
temp = fload.read().strip().split(':')

addr = temp[0]
port = int(temp[1])

fload.close()

server_address = (addr, port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(10)

fileNames = [f for f in listdir('dataset')]
             
def SendCustom(fileName):
    f = open(fileName, 'rb')
    file_name = f.name.split('/')[len(f.name.split('/'))-1]

    temp = '{}\n{}\n'.format(file_name, str(os.fstat(f.fileno()).st_size))
    output = temp + f.read()
    
    return output

def SendData(fileName):
    fmt = fileName.split('.')[-1]
    tmp = ''
    if fmt == 'mp3':
        tmp = 'audio/mpeg'
    elif fmt == 'html':
        tmp = 'text/html'
    elif fmt == 'png':
        tmp = 'image/png'
    elif fmt == 'ogv':
        tmp = 'video/ogg'
    f = file(fileName, 'rb')
    output = 'HTTP/1.1 200 OK\r\n'
    output = output+'Content-Type: {}\r\n'.format(tmp)
    output = output+'\r\n'
    output = output+f.read()
    f.close()
    
    return output

def DirSend():
    output = 'HTTP/1.1 200 OK\r\n'
    output = output+'Content-Type: text/html\r\n'
    output = output+'\r\n'
    
    output = '<html>\n<head>\n<title>Dataset /</title>\n<h1>Dataset /</h1>\n'
    output = output + '</head>\n\n<body>\n'
    
    for name in fileNames:
        tname = name.split(' ')
        tname = '%20'.join(tname)
        output = output+'<a href="dataset/{0}" download = "dataset/{0}">{1}</a><br>\n'.format(tname, name)
        
    output = output + '</body>\n</html>'
    return output

def StringSend(data):
    output = 'HTTP/1.1 200 OK\r\n'
    output = output+'Content-Type: text/html\r\n'
    output = output+'\r\n'
    output = output + data
    
    return output

input_socket = [server_socket]
# I can change it into any number I wish, well I forgot the maximum number.
buffer = 1024

try:
    print '\nServer is online ...\n'
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        # Reading socket found in select funcation.
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                
            else:
                data = sock.recv(buffer)
                
                print '<data>'
                print data
                print '</data>\n'
                
                if data.split('\n')[0].split(' ')[0].lower() == 'get':
                    command = data.split('\n')[0].split(' ')
                    
                    if command[1] == '/' or command[1] == '/index.html':
                        f = file('index.html','rb')
                        sock.send(StringSend(f.read()))
                        
                        f.close()
                        sock.close()
                        input_socket.remove(sock)
                    elif '/dataset' in command[1]:
                        com = command[1].split('%20')
                        com = ' '.join(com)
                        
                        status = False
                        fName = 'dataset/'
                        
                        for f in fileNames:
                            if f in com:
                                fName = fName + f
                                status = True
                                break
                        
                        if status == True:
                            f = ''
                            
                            if data.split('\n')[2].lower() == 'custom':
                                f = SendCustom(fName)
                            else:
                                f = SendData(fName)
                                
                            sock.send(f)
                            
                            sock.close()
                            input_socket.remove(sock)
                        else:
                            sock.send(DirSend())
                            sock.close()
                            input_socket.remove(sock)
                    else:
                        f = file('404.html','rb')
                        sock.send(StringSend(f.read()))
                        
                        f.close()
                        sock.close()
                        input_socket.remove(sock)
                    
                if not data:
                    sock.close()
                    input_socket.remove(sock)
                    
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)