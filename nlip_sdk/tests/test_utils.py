# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-8b-code-instruct

import unittest 
from nlip_sdk import utils as ut

class TestGetJoinedPath(unittest.TestCase):

    def test_simple_concatenation(self):
        file_path_1 = ut.get_resolved_path('/home/user')
        file_path_2 = 'documents'
        expected_result = ut.get_resolved_path('/home/user/documents')
        actual_result = ut.get_joined_path(file_path_1, file_path_2)
        self.assertEqual(actual_result, expected_result)

    def test_relative_path(self):
        file_path_1 = ut.get_resolved_path('/home/user')
        file_path_2 = '../documents'
        expected_result = ut.get_resolved_path('/home/documents')
        actual_result = ut.get_joined_path(file_path_1, file_path_2)
        self.assertEqual(actual_result, expected_result)

    def test_relative_path_with_dots(self):
        file_path_1 = ut.get_resolved_path('/home/user/blah')
        file_path_2 = '../../documents'
        expected_result = ut.get_resolved_path('/home/documents')
        actual_result = ut.get_joined_path(file_path_1, file_path_2)
        self.assertEqual(actual_result, expected_result)

    def test_relative_path_with_current_directory(self):
        file_path_1 = ut.get_resolved_path('/home/user')
        file_path_2 = './documents'
        expected_result = ut.get_resolved_path('/home/user/documents')
        actual_result = ut.get_joined_path(file_path_1, file_path_2)
        self.assertEqual(actual_result, expected_result)

    def test_relative_path_with_parent_directory(self):
        file_path_1 = ut.get_resolved_path('/home/user/documents')
        file_path_2 = '../images'
        expected_result = ut.get_resolved_path('/home/user/images')
        actual_result = ut.get_joined_path(file_path_1, file_path_2)
        self.assertEqual(actual_result, expected_result)

class TestGetParentLocation(unittest.TestCase):
    def test_get_parent_location(self):
        file_path = ut.get_resolved_path('/home/user/project/file.txt')
        expected_parent_path = ut.get_resolved_path('/home/user/project')
        actual_parent_path = ut.get_parent_location(file_path)
        self.assertEqual(actual_parent_path, expected_parent_path)

    def test_get_parent_location_with_relative_path(self):
        file_path = ut.get_resolved_path('file.txt')
        expected_parent_path = ut.get_resolved_path('.')
        actual_parent_path = ut.get_parent_location(file_path)
        self.assertEqual(actual_parent_path, expected_parent_path)

    def test_get_parent_location_with_multiple_directories(self):
        file_path = ut.get_resolved_path('/home/user/project/subfolder/file.txt')
        expected_parent_path = ut.get_resolved_path('/home/user/project/subfolder')
        actual_parent_path = ut.get_parent_location(file_path)
        self.assertEqual(actual_parent_path, expected_parent_path)

class TestGetFileExtension(unittest.TestCase):
    def test_with_extension(self):
        filename = "example.txt"
        expected_extension = ".txt"
        actual_extension = ut.get_file_extension(filename)
        self.assertEqual(actual_extension, expected_extension)

    def test_without_extension(self):
        filename = "example"
        expected_extension = None
        actual_extension = ut.get_file_extension(filename)
        self.assertEqual(actual_extension, expected_extension)

    def test_with_multiple_extensions(self):
        filename = "example.tar.gz"
        expected_extension = ".gz"
        actual_extension = ut.get_file_extension(filename)
        self.assertEqual(actual_extension, expected_extension)

    def test_with_directory_path(self):
        filename = "/home/users/example.png"
        expected_extension = ".png"
        actual_extension = ut.get_file_extension(filename)
        self.assertEqual(actual_extension, expected_extension)

if __name__ == '__main__':
    unittest.main()