import argparse
import sys
import textwrap
from Classes.NetCat import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Примеры:
  netcat.py -t 192.168.1.108 -p 5555 -l -c              # Командная оболочка
  netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt   # Загрузка файла
  netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd"  # Выполнить команду
  echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135      # Отправить данные на порт
  netcat.py -t 192.168.1.108 -p 5555                    # Подключение к серверу
'''))
    parser.add_argument('-c', '--command', action='store_true', help='Командная оболочка')
    parser.add_argument('-e', '--execute', help='Выполнить команду')
    parser.add_argument('-l', '--listen', action='store_true', help='Слушать входящие подключения')
    parser.add_argument('-p', '--port', type=int, default=5555, help='Порт подключения')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='IP-адрес назначения') 
    parser.add_argument('-u', '--upload', help='Сохранить полученные данные в файл')

    args = parser.parse_args()

    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()
