# -*- coding: utf-8 -*-
""" XML report generator """

from defusedxml import minidom, ElementTree
from xml.etree.ElementTree import Element, SubElement

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

    def render_report(self):
        """ Create XML report """

        root_node = Element('project')

        # define meta
        meta_node = SubElement(root_node, 'meta')

        for key, value in self._report_meta.iteritems():
            if value:
                item_node = SubElement(meta_node, key)
                item_node.text = value

        # define project content
        structure_node = SubElement(root_node, 'structure')

        for key, value in self._project_content.iteritems():
            item_node = SubElement(structure_node, key)

            files_node = SubElement(item_node, 'files')
            directories_node = SubElement(item_node, 'directories')

            if value['files']:
                for file_value in value['files']:
                    file_node = SubElement(files_node, 'file', name=file_value)

            if value['directories']:
                for dir_value in value['directories']:
                    dir_node = SubElement(directories_node, 'directory', name=dir_value)

        # define roles content
        roles_node = SubElement(root_node, 'ansible_roles')

        for key, value in self._role_content.iteritems():
            role_node = SubElement(roles_node, 'ansible_role', name=key)

            if value:
                for dependency in value:
                    dependencies_node = SubElement(role_node, 'dependency', name=dependency)

        self._report = ReportXML._prettify_raw_xml(root_node)

    def get_report(self):
        """
        Return full XML report

        @return: str
        """

        return self._report
