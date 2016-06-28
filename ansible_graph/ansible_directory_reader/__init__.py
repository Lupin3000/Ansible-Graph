# -*- coding: utf-8 -*-
""" Ansible directory reader package """

import logging
import os


class AnsibleDirectoryReader(object):
    """ Ansible directory reader class """

    def __init__(self):
        """ Ansible directory reader constructor """

        self.__logger = logging.getLogger(__name__)

        self.__project_path = str()
        self.__include = list()
        self.__exclude = list()
        self.__ansible_structure = dict()

    def __get_dir_content(self, directory_path):
        """
        Read directories and files inside specified directory

        @param directory_path: location of directory
        @type directory_path: str

        @return: dict
        """

        self.__logger.debug('Read directory - %s', directory_path)

        directory_content = {'directories': [], 'files': []}
        filtered_content = list()

        # read all from directory and filter excludes
        folder_reads = os.listdir(directory_path)

        for item in folder_reads:
            if item not in self.__exclude:
                filtered_content.append(item)

        # add filtered items into specific lists
        for item in filtered_content:
            item = directory_path + '/' + item

            # check for type file and add to list
            if os.path.isfile(item):
                item = item.replace(directory_path + '/', '')
                directory_content['files'].append(item)

            # check for type directory and add to list
            if os.path.isdir(item):
                item = item.replace(directory_path + '/', '')
                directory_content['directories'].append(item)

        return directory_content

    def set_reader_config(self, project_path, includes, excludes):
        """
        Settings for Ansible role reader

        @param project_path: Ansible project location
        @type project_path: str
        @param includes: list with inclusions
        @type includes: list
        @param excludes: list with exclusions
        @type excludes: list

        @raise e: TypeError
        @raise e: ValueError
        """

        self.__logger.info('Set Ansible directory reader configuration')

        if not isinstance(project_path, str):
            msg = 'Parameter: project_path needs to a string'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not project_path:
            msg = 'Parameter: no project_path path provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        if not isinstance(includes, list):
            msg = 'Parameter: includes needs to a list'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not includes:
            msg = 'Parameter: no includes provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        if not isinstance(excludes, list):
            msg = 'Parameter: exclude needs to a list'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not excludes:
            msg = 'Parameter: no exclude provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        self.__project_path = str(project_path)
        self.__include = list(includes)
        self.__exclude = list(excludes)

    def get_ansible_structure(self):
        """
        Return dictionary with Ansible directories and files list

        @return: dict
        """

        self.__logger.info('Read Ansible directory structure')

        # read root directory
        root_content = self.__get_dir_content(self.__project_path)
        self.__ansible_structure['root'] = root_content

        # read included subdirectories
        for item in self.__include:
            path = self.__project_path + '/' + item

            if item in root_content['directories']:
                self.__ansible_structure[item] = self.__get_dir_content(path)

        return self.__ansible_structure
