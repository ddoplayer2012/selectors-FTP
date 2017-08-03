import os, json
import selectors, socket

class Ftp_Server(object):
    def __init__(self):
        self.server = socket.socket()
        self.server.bind(('localhost', 9001))
        self.server.listen()
        self.server.setblocking(False)

        self.sel = selectors.DefaultSelector()
        self.sel.register(self.server, selectors.EVENT_READ, self.accept)
        while True:
            event = self.sel.select()
            for key ,mask in event:
                callback = key.data
                callback(key.fileobj, mask)

    def accept(self, sock, mask):
        conn , addr = sock.accept()
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        try:
            cmd = conn.recv(1024).decode()
            self.cmd_list = eval(cmd)
            print(self.cmd_list)
            getattr(self, self.cmd_list[0])(conn, mask)
        except Exception:
            print('客户端已断开')
            self.sel.unregister(conn)

    def get(self, conn ,mask):
        cmd ,filename = self.cmd_list
        print(filename)
        if os.path.isfile(filename):
            conn.setblocking(True)      #此处有什么其他的办法吗？
            f = open(filename, 'rb')
            file_size = os.stat(filename).st_size
            conn.send( str(file_size).encode() )
            conn.recv(1024)
            for line in f:
                conn.send(line)
            f.close()
            conn.setblocking(False)
        else:
            conn.send(b"False")

    def upload(self, conn, mas):
        conn.setblocking(True)
        cmd,filename = self.cmd_list
        print(filename)
        conn.send(b"ready to get file")
        file_total_size = int(conn.recv(1024).decode())
        conn.send(b"get the file size")

        f = open(filename, 'wb')
        received_size = 0
        while received_size <  file_total_size:
            data = conn.recv(1024)
            f.write(data)
            received_size += len(data)
            print(file_total_size, received_size)
        else:
            f.close()
            conn.setblocking(False)

    def ls(self, conn, mask):
        conn.setblocking(True)
        res = str(os.listdir('.'))
        conn.send( str(len(res.encode())).encode() )
        conn.recv(1024)

        conn.send(res.encode())
        conn.setblocking(False)

if __name__ == '__main__':
    Ftp_Server()

