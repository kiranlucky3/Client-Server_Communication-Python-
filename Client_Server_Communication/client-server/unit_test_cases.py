'''
This module checks the server's operations.

'''
import unittest
from request_info import request_info

class unit_test_cases(unittest.TestCase):
    '''
    unit-tester class for testing server-provided services

    '''
    def testcase_register_user(self):

        '''manages to create a test user with the
            username 'test' and the password 'test'
            and sees if it gives a confirmation message as success or not.
        '''
        response = request_info.register_user('test','test')
        final_output = {'message': 'Successfully registered!', 'status': 200}
        self.assertEqual(response,final_output)
    def testcase_register_user_already_exist(self):

        ''' manages to create a test user with the same login details
            and sees if it produces a failed message or not
        '''
        response = request_info.register_user('test','test')
        final_output = {'message':'A Username already exists!', 'status':403}
        self.assertEqual(response,final_output)
    def testcase_authenticate_user(self):

        '''Attempts to login using an already login and password
            and decides whether or not such a success message is returned.
        '''
        response = request_info.authenticate_user('test','test','127.0.0.1:65430')
        final_output = {'message':'Successfully Authenticated!', 'status':200}
        self.assertEqual(response,final_output)
    def testcase_authenticate_user_with_invalid_creds(self):

        '''attempts to login using wrong credentials
            and sees whether it returns a failed message
        '''
        response = response = request_info.authenticate_user('test','wrong_password','127.0.0.1:65430')
        final_output = {'message':'Credentials are Invalid!', 'status':401}
        self.assertEqual(response,final_output)
    def testcase_create_folder(self):

        '''manages to start a new folder and sees
           whether it gives a confirmation message
        '''
        data = {'command':'create_folder','name':'test_folder'}
        response = request_info.create_folder(data,'127.0.0.1:65430')
        final_output = {'message': 'Created new Directory', 'status': 200}
        self.assertEqual(response,final_output)
    def testcase_create_folder_already_exists(self):

        '''attempts to create folder with the same name
            as above and sees if it produces a failed warning or not
        '''
        data = {'command':'create_folder','name':'test_folder'}
        response = request_info.create_folder(data,'127.0.0.1:65430')
        final_output = {'message':'Already Directory Exists', 'status':403}
        self.assertEqual(response,final_output)
    def testcase_list(self):

        '''executes the list command and checks to see if it
           lists successfully created folders.
        '''
        response = request_info.list('127.0.0.1:65430')
        final_output = {'message':'test_folder', 'status':200}
        self.assertEqual(response,final_output)
    def testcase_change_folder(self):

        ''' Attempts to move the current working directory to a previously established folder
            and decides whether or not a success message is produced.
        '''
        data = {'command':'change_folder','name':'test_folder'}
        response = request_info.change_folder(data,'127.0.0.1:65430')
        final_output = {'message':'Folder-changed', 'status':200}
        self.assertEqual(response,final_output)
    def testcase_change_folder_not_existed(self):

        '''Attempts to move the present working directory to a folder that does not exist
            and determines whether or not a failure message is produced.
        '''
        data = {'command':'change_folder','name':'not_existed_folder'}
        response = request_info.change_folder(data,'127.0.0.1:65430')
        final_output = {'message':'No such Directory', 'status':404}
        self.assertEqual(response,final_output)
    def testcase_change_folder_unauthorized(self):

        '''tries to go out of the user's home folder
            and sees if it produces a failure notice or not
        '''
        data = {'command':'change_folder','name':'../../../'}
        response = request_info.change_folder(data,'127.0.0.1:65430')
        final_output = {'message':'Access-Denied!', 'status':401}
        self.assertEqual(response,final_output)
    def testcase_write_file(self):

        '''manages to write information to a file and checks
            whether something returns a success message
        '''
        data = {'command':'write_file','name':'test_file.txt','input':'this is test file'}
        response = request_info.write_file(data,'127.0.0.1:65430')
        final_output = {'message':"Written to file", 'status':200}
        self.assertEqual(response,final_output)
    def testcase_read_file(self):
        '''Attempts to read from such a file prepared in a previous test and determines
            whether or not a success message is returned.
        '''
        data = {'command':'read_file','name':'test_file.txt'}
        response = request_info.read_file(data,'127.0.0.1:65430')
        final_output = {'message':"this is test file\n", 'status':200}
        self.assertEqual(response,final_output)
    def testcase_read_file_not_existed(self):

        '''Attempts to read a file that does not exist and determines
            whether or not a failure message is returned.
        '''
        data = {'command':'read_file','name':'not_existed.txt'}
        response = request_info.read_file(data,'127.0.0.1:65430')
        final_output = {'message':'File error', 'status':404}
        self.assertEqual(response,final_output)

unit_tester=unit_test_cases()
