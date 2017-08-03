import socket,os
client = socket.socket()
client.connect(('localhost', 9001))


class Ftp_client(object):
    def __init__(self):
        while True:
            cmd = input(">>:").strip()
            if not cmd:continue
            self.cmd_list= cmd.split()
            print(self.cmd_list)
            if hasattr(self, self.cmd_list[0]):
                getattr(self, self.cmd_list[0])()
            else:
                print("cmd error")

    def get(self):
        if len(self.cmd_list) == 2:
            client.send(str(self.cmd_list).encode())
            server_reponse = client.recv(1024).decode()
            if server_reponse == "False":
                print("文件不存在")
                return
            print(server_reponse)
            file_total_size = int(server_reponse)
            client.send(b"ready to recv file")

            received_size = 0
            filename = self.cmd_list[1]
            f = open(filename, 'wb')
            while received_size < file_total_size:
                data = client.recv(1024)
                print(data)
                received_size += len(data)
                f.write(data)
                print(file_total_size, received_size)
            else:
                print("file recv done")
                f.close()
        else:
            print("cmd error")


    def upload(self):
        if len(self.cmd_list) == 2:
            filename = self.cmd_list[1]
            if os.path.isfile(filename):
                client.send(str(self.cmd_list).encode())
                client.recv(1024)
                f = open(filename, 'rb')
                file_size = os.stat(filename).st_size
                client.send(str(file_size).encode())
                client.recv(1024)
                for line in f:
                    client.send(line)
                f.close()
                print("file upload over")
            else:
                print("无此文件")
        else:
            print("cmd error")

    def ls(self):
        if self.cmd_list == ["ls"]:
            client.send(str(self.cmd_list).encode())
            server_reponse = client.recv(1024).decode()
            print(server_reponse)
            cmd_res_size = int(server_reponse)
            client.send(b"ready to recv cmd res")

            received_size = 0
            received_data = b''
            while received_size < cmd_res_size:
                data = client.recv(1024)
                received_data += data
                received_size += len(data)  #received_size += 1024
                print(cmd_res_size, received_size)
            else:
                print(received_data.decode())
        else:
            print("cmd error")

    def exit(self):
        if self.cmd_list == ["exit"]:
            exit()
        else:
            print("cmd error")


if __name__ == '__main__':
    Ftp_client()
