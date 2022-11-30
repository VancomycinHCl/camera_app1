import os
import logging
import socket_init
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def Server_start() -> None:

    # To start an FTP server.

    ftpUserMap = DummyAuthorizer()
    ftpUserMap.add_user(username = "test",
                        password = "password",
                        homedir  = "../output",
                        perm = 'elr')


    ftpHandler = FTPHandler
    ftpHandler.authorizer = ftpUserMap
    ftpHandler.banner = "Hello! Test Word Only."
    logging.basicConfig(filename="../log/test_ftp.log",level=logging.INFO)
    local_ip = socket_init.getIpAddress()
    address = (local_ip,2121)

    sever = FTPServer(address,ftpHandler)

    sever.max_cons = 128
    sever.max_cons_per_ip = 5
    sever.serve_forever()

    return

if __name__ == '__main__':
    Server_start()