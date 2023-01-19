''' This module manages all requests '''
import os
from pathlib import Path
from JSON_FILE import users_data
event_session ={}

class Request_Info:
    '''RequestHandler class for handling client method requests:change folder,list,read file,write file,create folder,handle request,register user,authenticate user
    '''
    def __init__(self):
        if not os.path.isdir('users'):
            os.mkdir('users')
        self.root_dir = os.path.join('users')

    def register_user(self,user_name,pass_word):
        '''This function registers a new user and
            creates a new folder in the users folder for the user.
        '''
        try:
            users = users_data.read()
            if user_name in users:
                return {'status':403,'message':'username already exists !'}
            users[user_name]=pass_word
            new_path = os.path.join(self.root_dir,user_name)
            os.mkdir(new_path)
            users_data.write(users)
            return {'message':'Successfully registered!', 'status':200}

        except Exception as error:
            print('Registration failed :'+str(error))
            return {'message':'Server-error', 'status':500,}

    def authenticate_user(self,user_name,pass_word,client):
        '''This function allows users to connect by validating the provided user_name
            and pass_word and adding the user to the event_session dictionary.
        '''
        try:
            users = users_data.read()
            if user_name in users:
                if users[user_name]==pass_word:
                    user_dir = os.path.join(self.root_dir,user_name)
                    event_session[client] = {'user_name':user_name,'curr_wor_dir':user_dir}
                    return {'message':'Successfully Authenticated!', 'status':200}
                return {'message':'Credentials are Invalid!', 'status':401}
            return {'message':"username doesn't exist !", 'status':401}
        except IOError :
            print("Failed")
            return {'message':'Server-error!', 'status':500}

    def change_folder(self,data,client):
        '''This function moves the current working directory to another folder specified by the user
            without allowing the user to leave his user folder.
        '''

        change_folder_path = os.path.join(event_session[client]['curr_wor_dir'],data['name'])
        if not os.path.isdir(change_folder_path):
            return {'status':404,'message':'No such Directory'}
        os.chdir(change_folder_path)
        change_folder_path = os.getcurr_wor_dir()
        if Path(self.root_dir) in Path(change_folder_path).parents:
            event_session[client]['curr_wor_dir']=change_folder_path
            return {'message':'Folder-changed', 'status':200}
        return {'message':'Access-Denied!', 'status':401}

    def list(self,client):
        '''This function produces a list of all files and
        folders in the current working directory of the user.
        '''
        curr_wor_dir = event_session[client]['curr_wor_dir']
        files = os.listdir(curr_wor_dir)
        output = '\n'.join(files)
        return {'message':output, 'status':200}

    def read_file(self,data,client):
        '''This function reads the file specified by the user
            and returns the contents of the file if the file exists.
        '''
        curr_wor_dir = event_session[client]['curr_wor_dir']
        file_path = os.path.join(curr_wor_dir,data['name'])
        if not os.path.isfile(file_path):
            return {'message':'No File Found', 'status':404}
        with open(file_path,'r',encoding='utf-8') as file:
            return {'message':file.read(), 'status':200}

    def write_file(self,data,client):
        '''This function concatenates the user's input to the requested file and clears the contents of the file
            if no input is provided.If the supplied file does not exist, it creates one and writes to it.
        '''
        curr_wor_dir = event_session[client]['curr_wor_dir']
        new_file_path = os.path.join(curr_wor_dir,data['name'])
        if os.path.isdir(new_file_path):
            return {'message':"A folder with that name already exists", 'status':403,}
        if not data['input']:
            with open(new_file_path,'w',encoding='utf-8') as file:
                file.write('')
        else:
            with open(new_file_path,'a',encoding='utf-8') as file:
                file.write(data['input']+'\n')
        return {'message':"Written to file", 'status':200}

    def create_folder(self,data,client):

        '''If the folder with the specified name does not exist,
           this method creates a new one.
        '''
        curr_wor_dir = event_session[client]['curr_wor_dir']
        new_path = os.path.join(curr_wor_dir,data['name'])
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
            return {'message':'Created new Directory', 'status':200}
        return {'message':'Directory Already Exists', 'status':403}

    def handle_request(self,data,client):
        '''This function handle requests to the server
        '''
        if(client not in event_session and data['command'] not in ['login','register']):
            return {'message':" Authenticated error ! Please Login", 'status':401}
        if data['command']=="register":
            return self.register_user(data['user_name'],data['pass_word'])
        elif data['command']=="login":
            return self.authenticate_user(data['user_name'],data['pass_word'],client)
        elif data['command']=='change_folder':
            return self.change_folder(data,client)
        elif data['command']=='list':
            return self.list(client)
        elif data['command']=='read_file':
            return self.read_file(data,client)
        elif data['command']=='write_file':
            return self.write_file(data,client)
        elif data['command']=='create_folder':
            return self.create_folder(data,client)
        else:
            return {'status':500,'message':'Invalid command'}

request_info = Request_Info()
