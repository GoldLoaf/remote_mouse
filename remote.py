import socket
import sys
import pyautogui
import json
import time
class Remote():
    def __init__(self, settings):
        self.mode = settings[1]
        if len(settings) == 3:
            self.ip = settings[2]

    def connect_controller(self):
        IP = self.ip
        PORT = 14888
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print('connecting...')
        sock.sendto('ping'.encode('utf-8'), (IP, PORT))
        ans = sock.recv(1024).decode('utf-8')
        if ans == 'pong':
            print('connected')
            return 'ok'

    def connect_controlled(self):
        IP = ''
        PORT = 14888
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((IP, PORT))
        mess, addr = sock.recvfrom(1024)
        if mess.decode('utf-8') == 'ping':
            print('connected with:', addr)
            sock.sendto('pong'.encode('utf-8'), addr)
        sock.close()

    def start_controller(self):
        IP = self.ip
        PORT = 14888
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        xr, yr = pyautogui.position()
        while True:
            xn, yn = pyautogui.position()
            x = xn - xr
            y = yr - yn
            xr, yr = xn, yn
            pos = {
                'x' : x,
                'y' : y
            }
            pos = json.dumps(pos)
            sock.sendto(pos.encode('utf-8'), (IP, PORT))
            time.sleep(0.033)

    def start_controlled(self):
        IP = ''
        PORT = 14888
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((IP, PORT))
        while True:
            data = sock.recv(1024).decode('utf-8')
            pos = json.loads(data)
            x = pos['x']
            y = pos['y']
            pyautogui.moveRel(x, y, 0.033)

    def start(self):
        if self.mode == '-c':
            self.start_controller()
        elif self.mode == '-r':
            self.start_controlled()

test = Remote(sys.argv)
test.start()