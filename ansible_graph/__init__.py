# -*- coding: utf-8 -*-
""" Ansible graph package """

import logging

from .configuration_reader import ReadConfiguration
from .ansible_role_reader import AnsibleRoleReader
from .ansible_directory_reader import AnsibleDirectoryReader
from .graph_generator import GraphGenerator
from .report_generator import ReportGenerator


class AnsibleGraphRunner(object):
    """ Ansible graph runner class """

    __LOGGER = logging.getLogger(__name__)

    @classmethod
    def __read_configuration(cls, configuration_path):
        """
        Read configuration file

        @param configuration_path: Configuration file location
        @type configuration_path: str

        @return: dict
        """

        configuration_file = str(configuration_path)
        configuration_content = dict()

        try:
            config = ReadConfiguration()
            config.set_configuration(configuration_file)
            configuration_content = config.get_configuration()
            del config
        except (TypeError, ValueError) as error:
            cls.__LOGGER.error(error)

        return configuration_content

    def __init__(self, project_path, configuration_path, arg_options):
        """
        Ansible graph runner constructor

        @param project_path: Ansible project directory location
        @type project_path: str
        @param configuration_path: Configuration file location
        @type configuration_path: str
        @param arg_options: application options
        @type arg_options: dict

        @raise e: TypeError
        @raise e: ValueError
        """

        if not isinstance(project_path, str):
            msg = 'Parameter: project_path needs to a string'
            self.__LOGGER.error(msg)
            raise TypeError(msg)

        if not project_path:
            msg = 'Parameter: no project_path path provided'
            self.__LOGGER.error(msg)
            raise ValueError(msg)

        if not isinstance(configuration_path, str):
            msg = 'Parameter: configuration_path needs to a string'
            self.__LOGGER.error(msg)
            raise TypeError(msg)

        if not configuration_path:
            msg = 'Parameter: no configuration_path path provided'
            self.__LOGGER.error(msg)
            raise ValueError(msg)

        if not isinstance(arg_options, dict):
            msg = 'Parameter: arg_options needs to a dictionary'
            self.__LOGGER.error(msg)
            raise TypeError(msg)

        self.__project_path = str(project_path)
        self.__arg_options = dict(arg_options)
        self.__config_content = AnsibleGraphRunner.__read_configuration(
            str(configuration_path))
        self.__directory_content = dict()
        self.__role_content = dict()

    def run_project_parser(self):
        """ Run Ansible project parser """

        # get Ansible roles
        try:
            roles = AnsibleRoleReader()
            roles.set_reader_config(self.__project_path)
            self.__role_content = roles.get_ansible_roles()
        except (TypeError, ValueError) as error:
            self.__LOGGER.error(error)

        self.__LOGGER.info(self.__role_content)

        try:
            role_graph = GraphGenerator()
            role_graph.set_graph_config(self.__arg_options['format'],
                                        'role',
                                        self.__config_content['location'])
            role_graph.generate_graph(self.__role_content)
        except (TypeError, ValueError) as error:
            self.__LOGGER.error(error)

        # get Ansible project structure
        include = self.__config_content['include']
        exclude = self.__config_content['exclude']

        try:
            structure = AnsibleDirectoryReader()
            structure.set_reader_config(self.__project_path, include, exclude)
            self.__directory_content = structure.get_ansible_structure()
        except (TypeError, ValueError) as error:
            self.__LOGGER.error(error)

        self.__LOGGER.info(self.__directory_content)

        try:
            dir_graph = GraphGenerator()
            dir_graph.set_graph_config(self.__arg_options['format'],
                                       'dir',
                                       self.__config_content['location'])
            dir_graph.generate_graph(self.__directory_content)
        except (TypeError, ValueError) as error:
            self.__LOGGER.error(error)

    def get_report(self):
        """
        Return full report

        @return: string
        """

        output = str()
        meta = {'title': self.__config_content['title'],
                'company': self.__config_content['company']}

        # generate report
        try:
            report = ReportGenerator(self.__arg_options['report'])
            report.set_report_header(meta)
            report.set_report_content(self.__directory_content)
            output = report.get_report()
        except (TypeError, ValueError) as error:
            self.__LOGGER.error(error)

        return output
