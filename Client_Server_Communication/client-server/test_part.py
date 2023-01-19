'''
This module helps to test all the possible cases. 
'''

from unit_test_cases import unit_tester
import unittest

def test_part():
    test_part = unittest.TestSuite()
    test_part.addTest(unit_tester('testcase_register_user'))
    test_part.addTest(unit_tester('testcase_register_user_already_exist'))
    test_part.addTest(unit_tester('testcase_authenticate_user'))
    test_part.addTest(unit_tester('testcase_authenticate_user_with_invalid_creds'))
    test_part.addTest(unit_tester('testcase_create_folder'))
    test_part.addTest(unit_tester('testcase_create_folder_already_exists'))
    test_part.addTest(unit_tester('testcase_change_folder'))
    test_part.addTest(unit_tester('testcase_change_folder_not_existed'))
    test_part.addTest(unit_tester('testcase_change_folder_unauthorized'))
    test_part.addTest(unit_tester('testcase_write_file'))
    test_part.addTest(unit_tester('testcase_read_file'))
    test_part.addTest(unit_tester('testcase_read_file_not_existed'))
    return test_part


if __name__ == '__main__':

    runner = unittest.TextTestRunner(failfast=True)
    runner.run(test_part())
