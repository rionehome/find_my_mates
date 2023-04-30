import socket

#UDP通信の受信側の準備
def UDP_recv(state, sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):

    if state == "始まり":
        HOST_NAME = ''   
        PORT = 8080
        #ipv4を使うので、AF_INET
        #udp通信を使いたいので、SOCK_DGRAM
        #ブロードキャストするときは255.255.255.255と指定せずに空文字
        sock.bind((HOST_NAME, PORT))

        return sock

    elif state == "繰り返し":
         #データを待ち受け
        rcv_data, addr = sock.recvfrom(1024)
        #print("receive data : [{}]  from {}".format(rcv_data.decode('utf-8'),addr))

        return rcv_data.decode('utf-8')

    elif state == "終了":
        sock.close()

        return state


#UDP通信の送信側の準備
def UDP_send(state, sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM), send_data = ''):

    HOST_NAME = ''
    PORT = 8080

    if state == "始まり":
        #ipv4を使うので、AF_INET
        #udp通信を使いたいので、SOCK_DGRAM
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #ブロードキャストを行うので、設定
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        return sock

    elif state == "繰り返し":
        sock.sendto(send_data.encode('utf-8'), (HOST_NAME, PORT))
        return state


    elif state == "終了":
        sock.close()

        return state




#試験的にUDP通信を受信する
def UDP_recv_test():

    sock = UDP_recv("始まり")

    while (True):
        rcv_data = UDP_recv("繰り返し", sock=sock)

    UDP_recv("終了", sock=sock)

#試験的にUDP通信を受信する
def UDP_send_test():

    sock = UDP_send("始まり")

    while (True):
        UDP_send("繰り返し", sock=sock, send_data="めがね")

    UDP_recv("終了", sock=sock)

