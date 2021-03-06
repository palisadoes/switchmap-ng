#!/usr/bin/env python3
"""Test the general module."""

import getpass
import unittest
import random
import os
import sys
import string
import tempfile
import yaml
import shutil

# Try to create a working PYTHONPATH
TEST_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
SWITCHMAP_DIRECTORY = os.path.abspath(os.path.join(TEST_DIRECTORY, os.pardir))
ROOT_DIRECTORY = os.path.abspath(os.path.join(SWITCHMAP_DIRECTORY, os.pardir))
if TEST_DIRECTORY.endswith('/switchmap-ng/switchmap/test') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "switchmap-ng/bin" directory. '
        'Please fix.')
    sys.exit(2)

from switchmap.utils import general
from switchmap import switchmap


class KnownValues(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    random_string = ''.join([random.choice(
        string.ascii_letters + string.digits) for n in range(9)])

    def test_cli_help(self):
        """Testing method / function cli_help."""
        pass

    def test_systemd_daemon(self):
        """Testing function systemd_daemon."""
        pass

    def test_systemd_exists(self):
        """Testing function systemd_exists."""
        # Get result for unknown service
        agent_name = self.random_string
        result = general.systemd_exists(agent_name)
        self.assertEqual(result, False)

    def test_check_sudo(self):
        """Testing function check_sudo."""
        # Test with sudo variable set
        result = 'SUDO_UID' in os.environ
        self.assertEqual(result, False)

        # Test with sudo variable set
        os.environ['SUDO_UID'] = getpass.getuser()
        with self.assertRaises(SystemExit):
            general.check_sudo()

    def test_check_user(self):
        """Testing function check_user."""
        pass

    def test_root_directory(self):
        """Testing method / function root_directory."""
        # Initializing key variables
        # Determine root directory for switchmap
        switchmap_dir = switchmap.__path__[0]
        components = switchmap_dir.split(os.sep)
        # Determine root directory 2 levels above
        root_dir = os.sep.join(components[0:-2])
        result = general.root_directory()
        self.assertEqual(result, root_dir)

    def test_get_hosts(self):
        """Testing method / function get_hosts."""
        # Initializing key variables
        pass

    def test_read_yaml_file(self):
        """Testing method / function read_yaml_file."""
        # Initializing key variables
        dict_1 = {
            'key1': 1,
            'key2': 2,
            'key3': 3,
            'key4': 4,
        }

        # Create temp file with known data
        directory = tempfile.mkdtemp()
        file_data = [
            (('{}/file_1.yaml').format(directory), dict_1)
        ]
        for item in file_data:
            filename = item[0]
            data_dict = item[1]
            with open(filename, 'w') as filehandle:
                yaml.dump(data_dict, filehandle, default_flow_style=False)

            # Get Results
            result = general.read_yaml_file(filename)

            # Test equivalence
            for key in result.keys():
                self.assertEqual(data_dict[key], result[key])

        # Clean up
        filelist = [
            next_file for next_file in os.listdir(
                directory) if next_file.endswith('.yaml')]
        for delete_file in filelist:
            delete_path = ('{}/{}').format(directory, delete_file)
            os.remove(delete_path)
        os.removedirs(directory)

    def test_read_yaml_files(self):
        """Testing method / function read_yaml_files."""
        # Initializing key variables
        dict_1 = {
            'key1': 1,
            'key2': 2,
            'key3': 3,
            'key4': 4,
        }

        dict_2 = {
            'key6': 6,
            'key7': 7,
        }
        dict_3 = {}

        # Populate a third dictionary with contents of other dictionaries.
        for key, value in dict_1.items():
            dict_3[key] = value

        for key, value in dict_2.items():
            dict_3[key] = value

        # Create temp file with known data
        directory = tempfile.mkdtemp()
        filenames = {
            '{}/file_1.yaml'.format(directory): dict_1,
            '{}/file_2.yaml'.format(directory): dict_2
        }
        for filename, data_dict in filenames.items():
            with open(filename, 'w') as filehandle:
                yaml.dump(data_dict, filehandle, default_flow_style=False)

        # Get Results
        result = general.read_yaml_files([directory])

        # Clean up
        for key in result.keys():
            self.assertEqual(dict_3[key], result[key])
        filelist = [
            next_file for next_file in os.listdir(
                directory) if next_file.endswith('.yaml')]
        for delete_file in filelist:
            delete_path = '{}/{}'.format(directory, delete_file)
            os.remove(delete_path)
        os.removedirs(directory)

    def test_run_script(self):
        """Testing method / function run_script."""
        # Initializing key variables
        pass

    def test_delete_files(self):
        """Testing method / function delete_files."""
        # Testing with a known invalid directory
        directory = self.random_string
        with self.assertRaises(SystemExit):
            general.delete_files(directory)

        # Creating temporary yaml and json files for testing
        directory = tempfile.mkdtemp()
        testfiles = ['test1.yaml', 'test2.yaml', 'test3.json']

        for filename in testfiles:
            filepath = '{}/{}'.format(directory, filename)
            open(filepath, 'a').close()

        # Testing if all yaml files were created
        count = len([name for name in os.listdir(
            directory) if name.endswith('.yaml')])
        self.assertEqual(count, 2)

        # Test if json file was created
        jcount = len([name for name in os.listdir(
            directory) if name.endswith('.json')])
        self.assertEqual(jcount, 1)

        # Deleting all yaml files using function
        general.delete_files(directory)

        # Test if  all yaml files were deleted
        result = len([name for name in os.listdir(
            directory) if name.endswith('.yaml')])
        self.assertEqual(result, 0)

        # Test if json file was not deleted
        jcount = len([name for name in os.listdir(
            directory) if name.endswith('.json')])
        self.assertEqual(jcount, 1)

        # Delete json file
        general.delete_files(directory, extension='.json')

        # Test if json file was deleted
        jcount = len([name for name in os.listdir(
            directory) if name.endswith('.json')])
        self.assertEqual(jcount, 0)

        # Removing test directory
        os.removedirs(directory)

        # Test if directory has been deleted
        self.assertEqual(os.path.isdir(directory), False)

    def test_config_directories(self):
        """Testing method / function config_directories."""
        # Initializing key variables
        # Initialize key variables
        save_directory = None

        if 'SWITCHMAP_CONFIGDIR' in os.environ:
            save_directory = os.environ['SWITCHMAP_CONFIGDIR']

            # Try with no SWITCHMAP_CONFIGDIR
            os.environ.pop('SWITCHMAP_CONFIGDIR', None)
            directory = '{}/etc'.format(general.root_directory())
            result = general.config_directories()
            self.assertEqual(result, [directory])

        # Test with SWITCHMAP_CONFIGDIR set
        directory = tempfile.mkdtemp()
        os.environ['SWITCHMAP_CONFIGDIR'] = directory
        result = general.config_directories()
        self.assertEqual(result, [directory])

        # Restore state
        if save_directory is not None:
            os.environ['SWITCHMAP_CONFIGDIR'] = save_directory

    def test_search_file(self):
        """Testing method / function search_file."""
        # Initializing key variables
        result = general.search_file('cp')
        self.assertEqual(result, '/bin/cp')

    def test_move_files(self):
        """Testing method / function move_files."""
        # Initialize key variables
        source_filenames = {}
        target_filenames = {}

        #################################################
        # Test with invalid source directory
        #################################################

        invalid_path = '/tmp/{}.{}'.format(
            self.random_string,
            self.random_string)

        with self.assertRaises(SystemExit):
            general.move_files(invalid_path, '/tmp')

        #################################################
        # Test with invalid destination directory
        #################################################

        invalid_path = '/tmp/{}.{}'.format(
            self.random_string,
            self.random_string)

        with self.assertRaises(SystemExit):
            general.move_files('/tmp', invalid_path)

        #################################################
        # Test with valid directory
        #################################################

        # Create a source directory
        source_dir = '/tmp/{}.1'.format(self.random_string)
        if os.path.exists(source_dir) is False:
            os.makedirs(source_dir)

        # Create a target directory
        target_dir = '/tmp/{}.2'.format(self.random_string)
        if os.path.exists(target_dir) is False:
            os.makedirs(target_dir)

        # Place files in the directory
        for count in range(0, 4):
            filename = ''.join([random.choice(
                string.ascii_letters + string.digits) for n in range(15)])
            source_filenames[count] = '{}/{}'.format(source_dir, filename)
            target_filenames[count] = '{}/{}'.format(target_dir, filename)
            open(source_filenames[count], 'a').close()

            # Check files in directory
            self.assertEqual(os.path.isfile(source_filenames[count]), True)

        # Delete files in directory
        general.move_files(source_dir, target_dir)

        # Check that files are not in source_dir
        for filename in source_filenames.values():
            self.assertEqual(os.path.isfile(filename), False)

        # Check that files are in in target_dir
        for filename in target_filenames.values():
            self.assertEqual(os.path.isfile(filename), True)

        # Delete directory
        shutil.rmtree(source_dir)

        # Delete directory
        shutil.rmtree(target_dir)

    def test_create_yaml_file(self):
        """Testing method / function create_yaml_file."""
        # Initializing key variables
        pass

    def test_dict2yaml(self):
        """Testing method / function dict2yaml."""
        # Initializing key variables
        data_dict = {
            '1': 'test 1',
            'two': 'test 2'
        }
        data_yaml = """'1': test 1
two: test 2
"""
        # Do test with good dict
        yaml_result = general.dict2yaml(data_dict)
        self.assertEqual(yaml_result, data_yaml)

    def test_delete_file(self):
        """Test function delete_file."""
        # Testing with a known invalid directory
        directory = self.random_string
        with self.assertRaises(SystemExit):
            general.delete_files(directory)

        # Creating temporary yaml and json files to test with
        directory = tempfile.mkdtemp()
        filenames = ['test1.yaml', 'test2.yaml', 'test3.json']

        for filename in filenames:
            filepath = '{}/{}'.format(directory, filename)
            open(filepath, 'a').close()

        # Testing if all files were created
        yamlcount = len([name for name in os.listdir(
            directory) if name.endswith('.yaml')])
        self.assertEqual(yamlcount, 2)

        jsoncount = len([name for name in os.listdir(
            directory) if name.endswith('.json')])
        self.assertEqual(jsoncount, 1)

        # Testing if all json files are deleted
        general.delete_files(directory, extension='.json')
        result = len([name for name in os.listdir(
            directory) if name.endswith('.json')])
        self.assertEqual(result, 0)

        # Testing if all yaml files are deleted
        general.delete_files(directory, extension='.yaml')
        result = len([name for name in os.listdir(
            directory) if name.endswith('.yaml')])
        self.assertEqual(result, 0)

        # Removing test directory
        os.removedirs(directory)

        # Test if directory has been deleted
        self.assertEqual(os.path.isdir(directory), False)

    def test_delete_yaml_files(self):
        """Test function delete_yaml_files."""
        # Testing with a known invalid directory
        directory = self.random_string
        with self.assertRaises(SystemExit):
            general.delete_files(directory)

        # Creating temporary yaml and json files for testing
        directory = tempfile.mkdtemp()
        testfiles = ['test1.yaml', 'test2.yaml', 'test3.json']

        for filename in testfiles:
            filepath = '{}/{}'.format(directory, filename)
            open(filepath, 'a').close()

        # Testing if all yaml files were created
        count = len([name for name in os.listdir(
            directory) if name.endswith('.yaml')])
        self.assertEqual(count, 2)

        # Test if json file was created
        jcount = len([name for name in os.listdir(
            directory) if name.endswith('.json')])
        self.assertEqual(jcount, 1)

        # Deleting all yaml files using function
        general.delete_yaml_files(directory)

        # Test if  all yaml files were deleted
        result = len([name for name in os.listdir(
            directory) if name.endswith('.yaml')])
        self.assertEqual(result, 0)

        # Test if json file was not deleted
        jcount = len([name for name in os.listdir(
            directory) if name.endswith('.json')])
        self.assertEqual(jcount, 1)

        # Delete json file
        general.delete_files(directory, extension='.json')

        # Test if json file was deleted
        jcount = len([name for name in os.listdir(
            directory) if name.endswith('.json')])
        self.assertEqual(jcount, 0)

        # Removing test directory
        os.removedirs(directory)

        # Test if directory has been deleted
        self.assertEqual(os.path.isdir(directory), False)

    def test_cleanstring(self):
        """Testing method / function cleanstring."""
        # Initializing key variables
        dirty_string = '   {}\n   \r {}   \n {}  '.format(
            self.random_string, self.random_string, self.random_string)
        clean_string = '{} {} {}'.format(
            self.random_string, self.random_string, self.random_string)

        # Test result
        result = general.cleanstring(dirty_string)
        self.assertEqual(result, clean_string)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
