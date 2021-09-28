from socket import *
from pathlib import Path


def runProxy():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((gethostbyname(gethostname()), 5000))
    server_socket.listen(1)

    while True:
        connection_socket, addr = server_socket.accept()
        request = connection_socket.recv(2048).decode()

        req_split_up = request.split('\n')
        req_top_split = req_split_up[0].split(' ')

        request_body = ''

        #if not cached, the body of the req the proxy makes will be the same besides the first 2 lines
        for x in req_split_up[2:]:
            request_body += x + '\n'

        if req_top_split[0] == 'GET':
            http_version = req_top_split[2].split('\r')[0]
            response = http_version + ' '
            url = req_top_split[1]
            url_split = url.split('/')

            if not url_split[0] == 'http:':
                url = 'http://' + url


            url_split = url.split('/')
            if not url_split[2][0:4] == 'www.':
                url = 'http://www.' + url_split[2]
                for str in url_split[3:]:
                    url += '/' + str

            url_split = url.split('/')
            host = url_split[2]
            path = ''

            for x in url_split[3:]:
                path += '/' + x

            if path == '':
                path = '/'

            file = Path('cachedirectory' + host + path)
            #webpage has already been cached
            if file.is_file():
                print('to be implemented is_file')

            #website has not yet been cached
            else:
                #create a request socket to send a request for this website
                pc_socket = socket(AF_INET, SOCK_STREAM)

                #establish a connection to the website's server
                pc_socket.connect((host, 80))

                #create a proper request for the website
                proxy_request = 'GET ' + path + ' ' + http_version + '\r\nHost: ' + host + '\r\nScheme: https\r\n' + request_body
                #print(proxy_request)
                pc_socket.send(proxy_request.encode())
                try:
                    proxy_response = pc_socket.recv(8192)
                    proxy_response = proxy_response
                   # print(proxy_response)

                    connection_socket.send(proxy_response)
                    connection_socket.close()
                    pc_socket.close()

                    

                except:
                    connection_socket.send(proxy_response)
                    connection_socket.close()
                    pc_socket.close()
