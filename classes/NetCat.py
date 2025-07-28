import socket
import threading
from execute import *

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        try:
            self.socket.connect((self.args.target, self.args.port))

            if self.buffer:
                self.socket.send(self.buffer)

            while True:
                recv_len = 1
                response = ''

                while recv_len:
                    data = self.socket.recv(4096)
                    if not data:
                        break
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break

                if response:
                    print(response, end='')

                try:
                    buffer = input('> ') + '\n'
                except (EOFError, KeyboardInterrupt):
                    print("\n[!] Выход")
                    break

                self.socket.send(buffer.encode())

        except Exception as e:
            print(f"[!] Ошибка при подключении/отправке: {e}")
        finally:
            self.socket.close()
    
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target = self.handle, args=(client_socket, )
            )
            client_thread.start()
     

    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
