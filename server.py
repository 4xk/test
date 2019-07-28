#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import struct
import json
import requests
import time
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def unpack_varint(s):
    d = 0
    for i in range(5):
        b = ord(s.recv(1))
        d |= (b & 0x7F) << 7 * i
        if not b & 0x80:
            break
    return d


def pack_varint(d):
    o = ''
    while True:
        b = d & 0x7F
        d >>= 7
        o += struct.pack('B', b | ((0x80 if d > 0 else 0)))
        if d == 0:
            break
    return o


def pack_data(d):
    return pack_varint(len(d)) + d


def pack_port(i):
    return struct.pack('>H', i)


def get_info(host='localhost', port=25565):

    # Connect

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Send handshake + status request

    s.send(pack_data('\x00\x00' + pack_data(host.encode('utf8'))
           + pack_port(port) + '\x01'))
    s.send(pack_data('\x00'))

    # Read response

    unpack_varint(s)  # Packet length
    unpack_varint(s)  # Packet ID
    l = unpack_varint(s)  # String length

    d = ''
    while len(d) < l:
        d += s.recv(1024)

    # Close our socket

    s.close()

    # Load json and return

    return json.loads(d.decode('utf8'))


pings = []
previous_players = []
avg = lambda a: sum(a) / len(a)
def sendMessage(channel,message):
  pass
while True:
    try:
        status = get_info('mc.fakezane.net')
        print status
        playing = 'Noone :('

        try:
            playing = ', '.join(player['name'] for player in
                                status['players']['sample'])
        except Exception:
          # print 'key error'
          pass
        with open('status.logs', 'w+') as f:
          f.write(str(status) + "\n\n\n")
          os.system('git add .;git commit -m "Updated logs"; git push')
          print 'updated logs'
        content = '''
  **Status** {}
  **Version** 1.14 - 1.14.4
  **Players** {}/{}
  **Playing now** {}
      '''.format("Starting" if status['version']['protocol'] == -1 else "Online",
          # status['version'
                # ]['name'], status['version']['protocol'],
                status['players']['online'], status['players']['max'],
                playing)

        # "\xe2 (slower)" if status['ping'] > avg(pings) else "\xe3 (faster)"

        x = {'color': 0x00FF00,
             'timestamp': datetime.datetime.now().isoformat(),
             'description': content,
             'title': '**Neverland - 1.14.x Vanilla survival Whitelisted**',
             'footer':{
               'text': 'Last updated '
             }
            }
        r = requests.request('PATCH',
                             'https://discordapp.com/api/v6/channels/602741527965597698/messages/602747665293508608'
                             ,
                             json={'content': 'Some stats for the server, updated every 2 seconds!'
                             , 'embed': x},
                             headers={'Content-Type': 'application/json'
                             ,
                             'Authorization': 'Bot ' + os.getenv('TOKEN')
                             })
    except Exception as e:
      print e
      playing = 'Noone :('
      content ='''
**Neverland**
**Status** Offline - If there is not a message below, the server crashed and will be relaunched soon.
    '''
      x = {'color': 0xFF0000,
           'timestamp': datetime.datetime.now().isoformat(),
           'description': content}
      r = requests.request('PATCH',
                           'https://discordapp.com/api/v6/channels/602741527965597698/messages/602747665293508608'
                           ,
                           json={'content': 'Some stats for the server, updated every 2 seconds!'
                           , 'embed': x},
                           headers={'Content-Type': 'application/json'
                           ,
                           'Authorization': 'Bot ' + os.getenv('TOKEN')
                           })
    time.sleep(2)

			