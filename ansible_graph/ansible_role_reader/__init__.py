# -*- coding: utf-8 -*-
""" Ansible role reader package """

import logging
import glob
import yaml


class AnsibleRoleReader(object):
    """ Ansible role reader class """

    def __init__(self):
        """ Ansible role reader constructor """

        self.__logger = logging.getLogger(__name__)

        self.__project_path = str()
        self.__ansible_roles = dict()

    def __get_ansible_role_dependencies(self, role_name, yml_path):
        """
        Read Ansible role dependencies from yml file

        @param role_name: Ansible role name
        @type role_name: str
        @param yml_path: Location for yml file
        @type yml_path: str
        """

        self.__logger.debug('Read role %s - %s', role_name, yml_path)

        with open(yml_path, 'r') as yml_file:
            yml_content = yaml.safe_load(yml_file)

        if 'dependencies' in yml_content:
            for item in yml_content['dependencies']:
                if type(item) is dict:
                    self.__ansible_roles[role_name].append(item['role'])
                else:
                    self.__ansible_roles[role_name].append(item)

    def __get_ansible_roles(self):
        """ Read Ansible meta directories for yml files """

        # define pattern
        glob_pattern = self.__project_path + '/roles/*/meta/*.y*ml'
        replace_pattern = self.__project_path + '/roles/'

        self.__logger.debug('Glob pattern - %s', glob_pattern)

        # read directories
        for item in glob.glob(glob_pattern):

            # get Ansible role name
            role = item.replace(replace_pattern, '').rsplit('/', 2)

            # add role into dictionary
            self.__ansible_roles[role[0]] = []

            # get dependencies
            self.__get_ansible_role_dependencies(role[0], item)

    def set_reader_config(self, project_path):
        """
        Settings for Ansible role reader

        @param project_path: Ansible project location
        @type project_path: str

        @raise e: TypeError
        @raise e: ValueError
        """

        self.__logger.info('Set Ansible role reader configuration')

        if not isinstance(project_path, str):
            msg = 'Parameter: project_path needs to a string'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not project_path:
            msg = 'Parameter: no project_path path provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        self.__project_path = str(project_path)

    def get_ansible_roles(self):
        """
        Return dictionary with Ansible roles and dependencies list

        @return: dict
        """

        self.__logger.info('Read Ansible roles')

        self.__get_ansible_roles()

        return self.__ansible_roles
