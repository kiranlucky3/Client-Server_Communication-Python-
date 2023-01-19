''' This module reads and writes json file informations.
'''
import json

class JSONFILE:
    '''JSONFILE class reads and writes json files methods: read, write
    '''
    def __init__(self,file_name):
        self.file_name = file_name

    def read(self):
        ''' This function reads a JSON file and returns it as a Dictionary object.
        '''
        try:
            with open(self.file_name,'r',encoding='utf-8') as file_name:
                information = file_name.read()
                information = json.loads(information)
                return information

        except IOError:
            print('could not read file'+self.file_name)

        except json.JSONDecodeError:
            print('need to store the file in json format')

    def write(self,information):

        '''
        This function takes a Dictionary object and exports it to a JSON file.
        '''
        
        try:
            with open(self.file_name,'w',encoding='utf-8') as file_name:
                file_name.write(json.dumps(information))

        except IOError:
            print('The file could not be opened. '+self.file_name)

        except json.JSONDecodeError:
            print("The file cannot be written to! JSON format is invalid.")

users_data = JSONFILE('users_information.json')
