import threading
import socket
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
                    chunk = data.decode()
                    response += chunk
                    print(chunk, end='') 
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
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()
     
    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'[+] Файл сохранён: {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    while b'\n' not in cmd_buffer:
                        cmd_buffer += client_socket.recv(4096)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'[!] Сервер завершил работу: {e}')
                    client_socket.close()
                    break