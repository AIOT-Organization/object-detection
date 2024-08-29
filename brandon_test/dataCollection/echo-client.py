import socket


def client_program():
    host = "134.71.68.251"  # The server's hostname or IP address
    port = 42322  # The port used by the server
    

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = str(input(" -> "))  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()