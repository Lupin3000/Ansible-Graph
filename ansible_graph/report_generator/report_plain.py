# -*- coding: utf-8 -*-
""" Plain report generator """

from .report import ReportBase


class ReportPlain(ReportBase):
    """Plain text report generator class """

    def __init__(self):
        """ Plain text report constructor """

        ReportBase.__init__(self)

    @staticmethod
    def __iterate_dict(dict_content):
        """
        Iterate over dictionary

        @param dict_content: content dictionary with lists
        @type dict_content: dict

        @return: string
        """

        content = str()
        content += '\n\nFiles:'
        for item in dict_content['files']:
            content += '\n - %s' % item
        content += '\n\nSubdirectories:'
        for item in dict_content['directories']:
            content += '\n - %s' % item
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

        # define content
        content = str()
        content += '\nDirectory: root'
        content += ReportPlain.__iterate_dict(self._report_content['root'])
        del self._report_content['root']
        content += '\n' + simple_line

        for key, value in self._report_content.iteritems():
            content += '\nDirectory: %s' % key
            content += ReportPlain.__iterate_dict(value)
            content += "\n" + simple_line

        self._report = meta + content

    def get_report(self):
        """
        Return full report

        @return: string
        """

        return self._report
