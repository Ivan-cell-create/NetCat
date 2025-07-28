import textwrap
import argparse
import sys
from classes.NetCat import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c #командная оболочка
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt
            #загружаем в файл
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd"\"
            #выполняем команду
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135
            #шлут текст на порт сервера 135
            # netcat.py -t 192.168.1.108 -p 5555 #соединяемся с сервером
            '''))
    parser.add_argument('-c', '--comand', action='store_true',
                        help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified commad')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555,
                        help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203',
                        help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
        
    nc = NetCat(args, buffer.encode())
    nc.run()
    