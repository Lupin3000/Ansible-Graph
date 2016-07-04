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
        self.__project_content = dict()
        self.__role_content = dict()

    def __get_ansible_project_content(self):
        """ Read Ansible project directories and files into dictionary """

        include = list(self.__config_content['include'])
        exclude = list(self.__config_content['exclude'])

        try:
            structure = AnsibleDirectoryReader()
            structure.set_reader_config(self.__project_path, include, exclude)
            self.__project_content = structure.get_ansible_structure()
        except (TypeError, ValueError) as error:
            self.__LOGGER.error(error)

    def __get_ansible_roles_content(self):
        """ Read Ansible roles and dependencies into dictionary """

        try:
            roles = AnsibleRoleReader()
            roles.set_reader_config(self.__project_path)
            self.__role_content = roles.get_ansible_roles()
        except (TypeError, ValueError) as error:
            self.__LOGGER.error(error)

    def __generate_graph(self, graph_type, graph_content):
        """
        Generate graphviz graph by type and content

        @param graph_type: definition for graph
        @type graph_type: str
        @param graph_content: content for graph
        @type graph_content: dict
        """

        gv_format = str(self.__arg_options['format'])
        gv_type = str(graph_type)
        gv_location = str(self.__config_content['location'])
        gv_content = dict(graph_content)

        try:
            graph = GraphGenerator()
            graph.set_graph_config(gv_format, gv_type, gv_location)
            graph.generate_graph(gv_content)
        except (TypeError, ValueError) as error:
            self.__LOGGER.error(error)

    def run_project_parser(self):
        """ Run Ansible project parser """

        # get Ansible project structure
        self.__get_ansible_project_content()
        self.__generate_graph('dir', self.__project_content)

        # get Ansible roles
        self.__get_ansible_roles_content()
        self.__generate_graph('role', self.__role_content)

    def get_report(self):
        """
        Return full report

        @return: str
        """

        output = str()
        meta = {'title': self.__config_content['title'],
                'company': self.__config_content['company']}

        # generate report
        try:
            report = ReportGenerator(self.__arg_options['report'])
            report.set_report_header(meta)
            report.set_report_content(self.__project_content,
                                      self.__role_content)
            output = report.get_report()
        except (TypeError, ValueError) as error:
            self.__LOGGER.error(error)

        return output
