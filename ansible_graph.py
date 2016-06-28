#!/usr/bin/env python
# -*- coding: utf8 -*-
""" AnsibleGraph main file """

import argparse
import logging
import sys

from ansible_graph import AnsibleGraphRunner
from os import path, access, R_OK


class AnsibleGraph(object):
    """ AnsibleGraph main class """

    @staticmethod
    def __parse_arguments():
        """
        Parse given command-line arguments

        @return: class
        """

        # set argument description/epilog
        description = 'Ansible-Graph automated graphs for Ansible'
        epilog = 'Please read the README for detailed description!'
        parser = argparse.ArgumentParser(description=description,
                                         epilog=epilog)

        # set optional arguments
        parser.add_argument("-v", "--verbosity",
                            action="count",
                            help="increase output verbosity")

        parser.add_argument("-r", "--report",
                            choices=['default', 'xml', 'json'],
                            default='default',
                            help="set report output format")

        parser.add_argument("-f", "--format",
                            choices=['svg', 'png', 'tif', 'gif', 'jpg'],
                            default='png',
                            help="set graph output format")

        # set mandatory arguments
        parser.add_argument("project", help="the Ansible project directory")
        parser.add_argument("config", help="location of configuration file")

        return parser.parse_args()

    def __init__(self):
        """ AnsibleGraph constructor """

        # initialize logging
        self.__logger = logging.getLogger(__name__)

        # parse arguments
        args = AnsibleGraph.__parse_arguments()

        # set logging level
        if args.verbosity > 1:
            logging.basicConfig(level=logging.DEBUG)
        elif args.verbosity == 1:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)

        # assign arguments
        self.__args = args

    def __verify_dir_path(self, dir_path):
        """
        Verify directory path and access

        @param dir_path: path to directory
        @type dir_path: str

        @return: bool
        """

        self.__logger.info('Verify directory path - %s', dir_path)

        if not path.isdir(dir_path) or not access(dir_path, R_OK):
            return False
        else:
            return True

    def __verify_file_path(self, file_path):
        """
        Verify file path and access

        @param file_path: path to to file
        @type file_path: str

        @return: bool
        """

        self.__logger.info('Verify file path - %s', file_path)

        if not path.isfile(file_path) or not access(file_path, R_OK):
            return False
        else:
            return True

    def verify_arguments(self):
        """ Verify application arguments """

        self.__logger.info('** verify given arguments **')
        self.__logger.debug('project path - %s', self.__args.project)
        self.__logger.debug('configuration file - %s', self.__args.config)

        # check ansible project argument
        if not self.__verify_dir_path(self.__args.project):
            self.__logger.error('%s not found', self.__args.project)
            sys.exit(1)

        # check configuration file argument
        if not self.__verify_file_path(self.__args.config):
            self.__logger.error('%s not found', self.__args.config)
            sys.exit(1)

    def run_documentation(self):
        """ Start documentation run """

        options = dict()
        options['report'] = self.__args.report
        options['format'] = self.__args.format

        self.__logger.debug('options - %s', options)

        try:
            self.__logger.info('** start statistics run **')

            documentation = AnsibleGraphRunner(self.__args.project,
                                               self.__args.config,
                                               options)
            documentation.run_project_parser()

            self.__logger.info('** generate report output **')
            print documentation.get_report()

        except (ValueError, TypeError) as error:
            self.__logger.error(error)


if __name__ == '__main__':
    RUN = AnsibleGraph()
    RUN.verify_arguments()
    RUN.run_documentation()
