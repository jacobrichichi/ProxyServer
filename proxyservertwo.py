from socket import *
from pathlib import Path
import os


def runProxy():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((gethostbyname(gethostname()), 5000))
    server_socket.listen(1)
    try:
        while True:
            connection_socket, addr = server_socket.accept()

            while True:
                request = connection_socket.recv(2048).decode()
                print(request)
                if request == '':
                    connection_socket.close()
                    break

                req_split_up = request.split('\n')
                req_top_split = req_split_up[0].split(' ')
                req_type = req_top_split[0]
                url = req_top_split[1]

                #parsing out http from the front of the requested url, it's unnecessary
                if url[0] == '/':
                    url = url[1:]

                if url[0:7] == 'http://':
                    url = url[7:]

                if url[0:8] == 'https://':
                    url = url[8:]

               # if url[0:4] == 'www.':
                #    url = url[4:]
               # if url[len(url)-1] == '/':
             #       url = url[0: len(url)-1]


                url_split = url.split('/')
                request_body = ''
                proxy_request = ''
                path = ''
                file_path = ''

                for x in req_split_up[2:]:
                    if not x == '':
                        request_body += x + '\n'

                if(req_split_up[1].split(':')[1][1:]==gethostbyname(gethostname())):
                    host = url_split[0]
                    for x in url_split[1:]:
                        path += '/' + x
                    if (not path == '') and (path[0] == '/'):
                        path = path[1:]

                    if path == '':
                        path = '/'
                    proxy_request = 'GET /' + path + ' HTTP/1.1\r\nHost: ' + host + '\r\n' + request_body

                else:
                    url_split = url.split('/')

                    host = url_split[0]
                    proxy_request = request
                    for x in url_split[3:]:
                        path += '/' + x

                    if path == '':
                        path = '/'

                if(req_type== 'GET'):

                    if(path=='/'):
                        file_path = 'cachedirectory/' + url + '/base'
                    else:
                        file_path = 'cachedirectory/' + url
                        if file_path[len(file_path)-1] == '/':
                            file_path = file_path[0:len(file_path)-1]

                    file_path = file_path.replace('?', '')
                    file = Path(file_path + '.txt')
                    if file.is_file():
                        r = open(file_path + '.txt', 'rb')
                        proxy_response = r.read()
                        connection_socket.send(proxy_response)
                        connection_socket.close()
                        r.close()

                    else:


                        pc_socket = socket(AF_INET, SOCK_STREAM)
                        pc_socket.connect((host, 80))

                        pc_socket.send(proxy_request.encode())

                        while True:
                            proxy_response = pc_socket.recv(8192)
                            print(proxy_response)
                            if len(proxy_response)<5:
                                pc_socket.close()
                                break
                            connection_socket.send(proxy_response)

                            path_finder = 'cachedirectory/'

                            path_split = file_path.split('/')[1:]

                            for dir in path_split[0:len(path_split)-1]:
                                path_finder += '/' + dir

                            if not os.path.isdir(path_finder):
                                os.makedirs(path_finder)

                            file = open(file_path + '.txt', 'wb')
                            file.write(proxy_response)

                            file.close()
    except Exception as e:
        print(e)