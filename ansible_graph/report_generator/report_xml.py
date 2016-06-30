# -*- coding: utf-8 -*-
""" XML report generator """

from xml.etree.ElementTree import Element, SubElement
from defusedxml import minidom, ElementTree

from .report import ReportBase


class ReportXML(ReportBase):
    """XML report generator class """

    def __init__(self):
        """ XML report constructor """

        ReportBase.__init__(self)

    @staticmethod
    def _prettify_raw_xml(raw_xml):
        """
        Return a pretty-printed XML string for the Element

        @param raw_xml: raw xml object
        @type raw_xml: object

        @return: str
        """
        rough_string = ElementTree.tostring(raw_xml, 'utf-8')
        re_parsed = minidom.parseString(rough_string)

        return re_parsed.toprettyxml(indent="\t", encoding='utf-8')

    def __set_meta_nodes(self):
        """
        Define all project meta nodes

        @return: object
        """

        root = Element('root')
        meta_node = SubElement(root, 'project_meta')

        for key, value in self._report_meta.iteritems():
            if value:
                item_node = SubElement(meta_node, key)
                item_node.text = value

        return root

    def __set_project_nodes(self):
        """
        Define all project structure nodes

        @return: object
        """

        root = Element('root')
        structure_node = SubElement(root, 'project_structure')

        for key, value in self._project_content.iteritems():
            item_node = SubElement(structure_node, key)

            files_node = SubElement(item_node, 'files')
            directories_node = SubElement(item_node, 'directories')

            if value['files']:
                children = [
                    Element('file', name=file_value)
                    for file_value in value['files']
                    ]
                files_node.extend(children)

            if value['directories']:
                children = [
                    Element('directory', name=dir_value)
                    for dir_value in value['directories']
                    ]
                directories_node.extend(children)

        return root

    def __set_roles_nodes(self):
        """
        Define all roles structure nodes

        @return: object
        """

        root = Element('root')
        roles_node = SubElement(root, 'ansible_roles')

        for key, value in self._role_content.iteritems():
            role_node = SubElement(roles_node, 'ansible_role', name=key)

            if value:
                children = [
                    Element('dependency', name=dependency)
                    for dependency in value
                    ]
                role_node.extend(children)

        return root

    def render_report(self):
        """ Create XML report """

        root_node = Element('project')
        root_node.extend(self.__set_meta_nodes())
        root_node.extend(self.__set_project_nodes())
        root_node.extend(self.__set_roles_nodes())

        self._report = ReportXML._prettify_raw_xml(root_node)

    def get_report(self):
        """
        Return full XML report

        @return: str
        """

        return self._report
