import threading
import socket
import time
from execute import *

"""
Класс NetCat, который реализует основную логику утилиты 
"""
class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    """
    Метод run, принимающий в себя текущий экземпляр класса (self)
    
    Логика реализации флага -l: если True, то будет работать как сервер,
    если False, то как клиент
    """
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    """
    Реализация простого TCP-клиента
    """
    def send(self):
        try:
            self.socket.connect((self.args.target, self.args.port))

            if self.buffer:
                self.socket.send(self.buffer) #При уже подготовленных данных - отправляет их

            while True:
                recv_len = 1
                response = '' # Строка для накопления получаемых данных

                while recv_len:
                    data = self.socket.recv(4096) #4096 байт
                    if not data:
                        break
                    recv_len = len(data)
                    chunk = data.decode()
                    response += chunk
                    print(chunk, end='') 
                    if recv_len < 4096:
                        break

                #if response:
                #   print(response, end='')
                
                buffer = input('') 
                self.socket.send((buffer + '\n').encode())
                
        except Exception as e:
            print(f"[!] Ошибка при подключении/отправке: {e}")
        finally:
            self.socket.close()
    
    """
    Реализация многопоточного TCP-сервера
    """
    def listen(self):
        bind_ip = self.args.target if self.args.target else '0.0.0.0' #Если не получилось, то подключение с любого IP
        self.socket.bind((bind_ip, self.args.port))
        self.socket.listen(5) #Максимальная длина очереди ожидания соединения 
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()
     
    """
     Обработка подлючения в зависимости от аргумента 
    """
    def handle(self, client_socket):
        if self.args.execute:
            start_time = time.time() 
            output = execute(self.args.execute)
            client_socket.send(output.encode())
            elapsed_time = time.time() - start_time
            print(f"[*] Выполнение команды завершено за {elapsed_time:.2f} секунд")

        elif self.args.upload:
            start_time = time.time()  
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                file_buffer += data
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'[+] Файл сохранён: {self.args.upload}'
            client_socket.send(message.encode())
            elapsed_time = time.time() - start_time
            print(f"[*] Загрузка файла завершена за {elapsed_time:.2f} секунд")

        elif self.args.command:
            start_time = time.time()
            cmd_buffer = b''
            client_socket.settimeout(5.0) 
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    while b'\n' not in cmd_buffer:
                        chunk = client_socket.recv(4096)
                        if not chunk:
                            return  
                        cmd_buffer += chunk
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except socket.timeout:
                    print("[!] Тайм-аут при получении данных")
                    client_socket.close()
                    return
                except Exception as e:
                    print(f'[!] Сервер завершил работу: {e}')
                    client_socket.close()
                    break
            elapsed_time = time.time() - start_time
            print(f"[*] Сессия командной оболочки завершена за {elapsed_time:.2f} секунд")