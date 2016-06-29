# -*- coding: utf-8 -*-
""" Report generator """

import time
import os
import pwd


class ReportBase(object):
    """Report generator class"""

    def __init__(self):
        """
        Basic report constructor
        """

        self._report = str()
        self._report_meta = dict()
        self._project_content = dict()
        self._role_content = dict()

    def set_report_meta(self, meta):
        """
        Set report meta

        @param meta: meta for report
        @type meta: dict
        """

        self._report_meta = meta
        self._report_meta['user'] = pwd.getpwuid(os.getuid())[0]
        self._report_meta['date'] = time.strftime("%Y-%m-%d")
        self._report_meta['time'] = time.strftime("%I:%M:%S")

    def set_report_content(self, project_content, role_content):
        """
        Set report content

        @param project_content: content for report
        @type project_content: dict
        @param role_content: content for report
        @type role_content: dict
        """

        self._project_content = dict(project_content)
        self._role_content = dict(role_content)

    def get_report(self):
        """
        Return full report

        @return: str
        """

        return self._report
