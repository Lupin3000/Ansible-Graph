# -*- coding: utf-8 -*-
""" XML report generator """

from .report import ReportBase


class ReportXML(ReportBase):
    """XML report generator class """

    def __init__(self):
        """ XML report constructor """

        ReportBase.__init__(self)

    def render_report(self):
        """ Create XML report """

        pass

    def get_report(self):
        """
        Return full XML report

        @return: str
        """

        return self._report
