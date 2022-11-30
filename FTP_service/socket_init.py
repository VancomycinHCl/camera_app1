import socket


# from socket import *

def getIpAddress() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        print(s.getsockname())
        s.close()
        return ip
    except Exception as E:
        print(E)
        return ''


if __name__ == '__main__':
    getIpAddress()
