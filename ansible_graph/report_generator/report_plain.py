# -*- coding: utf-8 -*-
""" Plain report generator """

from .report import ReportBase


class ReportPlain(ReportBase):
    """Plain text report generator class """

    def __init__(self):
        """ Plain text report constructor """

        ReportBase.__init__(self)

    @staticmethod
    def _iterate_project(project_content):
        """
        Iterate over dictionary

        @param project_content: project content dictionary with lists
        @type project_content: dict

        @return: str
        """

        content = str()

        content += '\n\nFiles:'
        for item in project_content['files']:
            content += '\n - %s' % item
        content += '\n\nSubdirectories:'
        for item in project_content['directories']:
            content += '\n - %s' % item

        return content

    @staticmethod
    def _iterate_roles(roles_content):
        """

        @param roles_content: roles content dictionary with lists
        @type roles_content: dict

        @return: str
        """

        content = str()

        for key, value in roles_content.iteritems():
            content += '\n' + key + ':\n'
            if value:
                for item in value:
                    content += ' - ' + item + '\n'

        return content

    def render_report(self):
        """ Create report """

        double_line = '=' * 80
        simple_line = '-' * 80

        # define meta
        meta = double_line
        for key, value in self._report_meta.iteritems():
            if value:
                meta += "\n{:<15} {:<30}".format(key.title() + ':', value)
        meta += "\n" + double_line

        # define project content
        project = str()

        project += '\nDirectory: root'
        project += ReportPlain._iterate_project(self._project_content['root'])
        del self._project_content['root']
        project += '\n' + simple_line

        for key, value in self._project_content.iteritems():
            project += '\nDirectory: %s' % key
            project += ReportPlain._iterate_project(value)
            project += "\n" + simple_line

        # define roles content
        roles = str()

        roles += '\nRoles and Dependencies:\n'
        roles += ReportPlain._iterate_roles(self._role_content)

        # combine reports
        self._report = meta + project + roles

    def get_report(self):
        """
        Return full plain report

        @return: str
        """

        return self._report
