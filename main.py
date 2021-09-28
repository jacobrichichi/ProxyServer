from proxyservertwo import *
from socket import *

def test_server():
    pc_socket = socket(AF_INET, SOCK_STREAM)
    # establish a connection to the website's server
    pc_socket.connect(('www.google.com', 80))

    print(pc_socket)

    proxy_request = 'GET /?gws_rd=ssl HTTP/1.1\nHost: www.google.com\nScheme: https\n' + '\nConnection: keep-alive' + '\nCache-Control: max-age=0' + '\nUpgrade-Insecure-Requests: 1' +'\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52' +'\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' +'\nAccept-Encoding: gzip, deflate' +'\nAccept-Language: en-US,en;q=0.9'

    print(proxy_request)
    pc_socket.send(proxy_request.encode())
    proxy_response = pc_socket.recv(8192).decode()

    print(proxy_response)

    pc_socket.close()

if __name__ == '__main__':
    runProxy()
    #test_server()
