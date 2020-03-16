import socket
import sys
import pyautogui
import json
import time

pyautogui.FAILSAFE = False

class Remote():
    def __init__(self, settings):
        self.mode = settings[1]
        if len(settings) == 3:
            self.ip = settings[2]

    # def connect_controller(self):
    #     IP = self.ip
    #     PORT = 14888
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #     print('connecting...')
    #     sock.sendto('ping'.encode('utf-8'), (IP, PORT))
    #     ans = sock.recv(1024).decode('utf-8')
    #     if ans == 'pong':
    #         print('connected to', self.IP)
    #
    # def connect_controlled(self):
    #     IP = ''
    #     PORT = 14888
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     sock.bind((IP, PORT))
    #     mess, addr = sock.recvfrom(1024)
    #     if mess.decode('utf-8') == 'ping':
    #         print('connected with:', addr)
    #         sock.sendto('pong'.encode('utf-8'), addr)
    #     sock.close()

    def start_controller(self):
        IP = self.ip
        PORT = 14888
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        ans = sock.recv(1024).decode('utf-8')
        if ans == 'ok':
            print(f'Успешно подключено к {self.ip}')
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
            sock.send(pos.encode('utf-8'))
            time.sleep(0.033)

    def start_controlled(self):
        IP = ''
        PORT = 14888
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((IP, PORT))
        sock.listen(1)
        print('Ожидаю соединения...')
        conn, addr = sock.accept()
        print(f'Подключено к {addr[0]}')
        conn.send('ok'.encode('utf-8'))
        while True:
            data = conn.recv(1024).decode('utf-8')
            try:
                pos = json.loads(data)
            except:
                continue
            if not data:
                break
            cx, cy = pyautogui.position()
            x = pos['x']
            y = pos['y']
            pyautogui.moveRel(x, -y, pause=0)

    def start(self):
        if self.mode == '-c':
            self.start_controller()
        elif self.mode == '-r':
            self.start_controlled()

test = Remote(sys.argv)
test.start()