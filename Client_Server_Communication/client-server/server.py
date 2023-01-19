'''
This module manages the connections established from each client.
'''
import asyncio
import json
from request_info import request_info


def get_client_id(client):

    '''This method accepts a client tuple('127:0.0.1',54645),
        unites its components, and returns client id('127:0.0.1:54645').
    '''
    return ':'.join([str(i) for i in client])

async def submit_response(write_token,data):
    '''This function communicates the server's response to the user.
    '''
    data = json.dumps(data)
    write_token.write(data.encode())
    await write_token.drain()

async def server_files(read_token, write_token):
    '''This method is invoked for each client connection to the server.

    '''
    client = write_token.get_extra_info('peername')
    client = get_client_id(client)
    print('Connected from '+client)
    while True:
        data = await read_token.read(100)
        if not data:
            break
        data = json.loads(data)
        response = request_info.handle_request(data,client)
        await submit_response(write_token,response)
    write_token.close()

async def main(host, port):
    '''This function runs the server at the specified host and port.
    '''
    print(f'Server started at {host}: port {port}')
    server = await asyncio.start_server(server_files, host, port)
    await server.serve_forever()

try:
    asyncio.run(main('127.0.0.1', 8091))
except KeyboardInterrupt:
    print('\nServer terminated!!!')
except Exception as e:
    print("Something went wrong"+str(e))
