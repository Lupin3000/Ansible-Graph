# -*- coding: utf-8 -*-
""" Graph generator package """

import logging
from graphviz import Digraph


class GraphGenerator(object):
    """ Graph generator class """

    ALLOWED_GRAPH_TYPES = ['project', 'roles']

    def __init__(self):
        """ Graph generator constructor """

        self.__logger = logging.getLogger(__name__)

        self.__graph_format = 'png'
        self.__graph_location = 'report'
        self.__dot = Digraph('g')
        self.__graph_type = str()

    def set_graph_config(self, graph_format, graph_type, graph_location):
        """
        Configuration for graph

        @param graph_format: define output format for graph
        @type graph_format: str
        @param graph_type: define output type for graph
        @type graph_type: str
        @param graph_location: define location for generated graph
        @type graph_location: str

        @raise e: TypeError
        @raise e: ValueError
        """

        self.__logger.info('Set graph configuration')

        if not isinstance(graph_format, str):
            msg = 'Parameter: graph_format needs to a string'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not graph_format:
            msg = 'Parameter: no graph_format path provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        if not isinstance(graph_type, str):
            msg = 'Parameter: graph_type needs to a string'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not graph_type:
            msg = 'Parameter: no graph_type path provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        if graph_type.lower() not in self.ALLOWED_GRAPH_TYPES:
            msg = 'Parameter: graph_location needs to a string'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not graph_location:
            msg = 'Parameter: no graph_location path provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        self.__graph_format = str(graph_format)
        self.__graph_type = str(graph_type)

        if str(graph_type) == 'project':
            name = '/project'
        else:
            name = '/roles'

        self.__graph_location = str(graph_location + name)

        self.__logger.debug('Location for graph - %s', self.__graph_location)

    def __run_graph_generation(self, graph_content):
        """
        Run Graphviz generation

        @param graph_content: content for graph
        @type graph_content: dict
        """

        for key, value in graph_content.iteritems():

            # generate role graph
            if self.__graph_type == 'roles':
                self.__dot.node(str(key))
                if value:
                    for item in value:
                        self.__dot.edge(key, item)

            # generate directory graph
            if self.__graph_type == 'project':
                self.__dot.node(str(key), shape='folder')
                if value['directories']:
                    for item in value['directories']:
                        self.__dot.node(str(item), shape='folder')
                        self.__dot.edge(key, item)
                if value['files']:
                    for item in value['files']:
                        self.__dot.node(str(item), shape='note')
                        self.__dot.edge(key, item)

    def generate_graph(self, content):
        """
        Generate graphs

        @param content: content for graph
        @type content: dict

        @raise e: TypeError
        @raise e: ValueError
        """

        if not isinstance(content, dict):
            msg = 'Parameter: content needs to a dictionary'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not content:
            msg = 'Parameter: no content path provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        self.__logger.debug('%s', content)

        self.__run_graph_generation(dict(content))
        self.__logger.debug(self.__dot.source)

        self.__dot.format = self.__graph_format
        self.__dot.render(self.__graph_location)
