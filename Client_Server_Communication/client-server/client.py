''' This module is client application which interacts with
the users,sends reqests to the server and displays response.
'''
import asyncio

import json
from secrets import choice


async def request(read_token,write_token,body):
    '''This functions sends requests to the server'''
    body = json.dumps(body)
    write_token.write(body.encode())
    await write_token.drain()
    data = await read_token.read(100)
    return json.loads(data)

def print_commands():
    ''' This methods are suitable the format of service commands.'''
    print(" change_folder <name>")
    print(" list")
    print(" read_file <name>")
    print(" write_file <name> <content>")
    print(" create_folder <name>")

async def login_instructions(read_token,write_token):
    '''This function is in responsible of the registration and login processes.
    '''
    while True:
        print("\nLog in to utilize the File Manager.")
        print("Choose any option:")
        print("1.Register")
        print("2.Login")
        choice = input("\n$ ")
        if choice=="1":
            user_name=input("Type your new username:").strip()
            pass_word=input("Type your password:").strip()
            message = {"command":"register","user_name":user_name,"pass_word":pass_word}
            response = await request(read_token,write_token,message)
            if response['status'] == 200:
                print("Registered-successfully!!")
            else:
                print(response['message']+"\n")
        elif choice=="2":
            print("------------Login-page-------------")
            user_name = input("Type your username here :").strip()
            pass_word = input("Type your password here :").strip()
            message = {"command":"login","user_name":user_name,"pass_word":pass_word}
            response = await request(read_token,write_token,message)
            if response['status'] == 200:
                print("Successfully logged in!!\n")
                print("Commands available:\n$ commands\n$ quit")
                break
            print(response['message']+"\n")
        elif choice == 'quit':
            quit()    

async def commands_instructions(read_token,write_token):
    ''' This function handles the services commands
    and sends appropriate requests to the server.
    '''
    while True:
        message = input("\n$ ")
        if message.lower() == "quit":
            print("Bye!!")
            break
        tokens = message.split()
        if not tokens:
            continue
        command = tokens[0]
        try:
            if command=="commands":
                print_commands()
            elif command == 'change_folder':
                message = {'command':'change_folder','name':tokens[1]}
                response = await request(read_token,write_token,message)
                print(response['message'])
            elif command == 'list':
                message = {'command':'list'}
                response = await request(read_token,write_token,message)
                print(response['message'])
            elif command == 'read_file':
                message = {'command':'read_file','name':tokens[1]}
                response = await request(read_token,write_token,message)
                print(response['message'])
            elif command == 'write_file':
                if len(tokens)==2:
                    tokens.append('')
                else:
                    tokens[2] = ' '.join(tokens[2:])
                message = {'command':'write_file','name':tokens[1],'input':tokens[2]}
                response = await request(read_token,write_token,message)
                print(response['message'])
            elif command == 'create_folder':
                message = {'command':'create_folder','name':tokens[1]}
                response = await request(read_token,write_token,message)
                print(response['message'])
            else:
                print("Invalid-Command!") 

        except IndexError:
            print('Invalid format!')


async def main():
    '''The main function that connects to the server and begins the client workflow.
    '''
    read_token, write_token = await asyncio.open_connection('127.0.0.1', 8091)
    print("---------------Client Application------------------")
    await login_instructions(read_token,write_token)
    await commands_instructions(read_token,write_token)
    print('--------Connection closed----------')
    write_token.close()
    await write_token.wait_closed()

try:
    asyncio.run(main())
except KeyboardInterrupt :
    print("\nConnection closed!!!")
except ConnectionRefusedError:
    print("The server cannot be reached.!!")
