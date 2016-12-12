#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 13:06:36 2016

@author: arhy
"""

import socket
from bs4 import BeautifulSoup

fload = file('httpclient.conf')
temp = fload.read().strip().split(':')

addr = temp[0]
port = int(temp[1])

fload.close()

#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = (addr, port)
#client_socket.connect(server_address)

while True:
    uri = ''
    try:
        uri = input('Link: ')
        
        txt = '{}:{}'.format(addr, port)
        if not txt in uri:
            print "Error: Can not recognize URI!"
            continue
    except:
        print 'Error: No single or double quote!'
        continue
        
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (addr, port)
    client_socket.connect(server_address)
    
    uri = [i for i in uri.strip().split('/') if len(i) > 1]
    
    if len(uri) == 1:
        uri = '/'
    else:
        uri = '/'+'/'.join(uri[1:])
    
    request_header = 'Get {} HTTP/1.1\r\nHost: {}:{}\r\ncustom'.format(uri,addr,port)
    client_socket.send(request_header)

    response = ''
    while True:
        recv = client_socket.recv(1024)
        if not recv:
            break
        response += recv
    
    #print 'Result: {}'.format('<html>' in response)
    #print response
    
    if 'HTTP/1' in response:
        response = response.split('\r\n\r\n')[1]
    elif 'HTTP/1' not in response.split('\n')[0]:
        try:
            fname = response.split('\n')[0]
        
            fsize = int(response.split('\n')[1])
            fdown = response.split('\n')[2]
            
            frec = file(fname,'wb')
            frec.write('\n'.join(response.split('\n')[2:]))
            frec.close()
            print 'Message: File downloaded!'
            client_socket.close()
            continue
        except:
            print 'Message: Not a file to download!'
    soup = BeautifulSoup(response, 'html.parser')
    print soup.text
    
    client_socket.close()