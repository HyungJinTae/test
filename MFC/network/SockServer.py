
from common.Setting import logger
import threading
import socket
from threading import Lock


class SockServer(threading.Thread):
    def __init__(self, host='localhost', port=12312):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.lock = Lock()
        self.is_run = True

    def run(self):
        self.socket.listen(5)
        conn, address = self.socket.accept()
        logger.debug(f"conn: {conn}, address: {address}")
        while self.is_run:
            try:
                recv_message = conn.recv(1024)
                message = recv_message.decode('cp949').encode('utf-8').decode('utf-8')
                logger.debug(f"{message}")
                send_message = "".encode('cp949')
                logger.debug(f"{send_message}")
            except ConnectionAbortedError:
                logger.warning("ConnectionAbortedError")
                conn.close()
                conn, address = self.socket.accept()
            except ConnectionResetError:
                logger.warning("ConnectionResetError")
                conn.close()
                conn, address = self.socket.accept()
            except Exception as e:
                logger.error(f"e->{e}")
        conn.close()

    def Init(self):
        self.start()
