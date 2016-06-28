# -*- coding: utf-8 -*-
""" Configuration reader package """

import logging
import ConfigParser


class ReadConfiguration(object):
    """ Configuration reader class """

    def __init__(self):
        """ Configuration reader constructor """

        self.__logger = logging.getLogger(__name__)

        self.__config = dict()

    def set_configuration(self, file_path):
        """
        Set and verify configuration parameter

        @param file_path: location of configuration file
        @type file_path: str

        @raise e: TypeError
        @raise e: ValueError
        """

        self.__logger.info('Set configuration path - %s', file_path)

        if not isinstance(file_path, str):
            msg = 'Parameter: file_path needs to a string'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not file_path:
            msg = 'Parameter: no file_path provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        try:
            parser = ConfigParser.SafeConfigParser()
            parser.read(file_path)

            # read section global
            self.__config['title'] = parser.get('global', 'title')
            self.__config['company'] = parser.get('global', 'company')

            # read section structure
            self.__config['include'] = [
                e.strip() for e in parser.get('structure', 'include').split(',')
                ]
            self.__config['exclude'] = [
                e.strip() for e in parser.get('structure', 'exclude').split(',')
                ]

            # read section graph
            self.__config['location'] = parser.get('graph', 'location')

        except ConfigParser.Error as error:
            self.__logger.error(error)

    def get_configuration(self):
        """
        Return configuration as dictionary

        @return: dict
        """

        self.__logger.info('Read configuration')

        return self.__config
