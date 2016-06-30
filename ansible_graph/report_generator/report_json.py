# -*- coding: utf-8 -*-
""" JSON report generator """

from .report import ReportBase


class ReportJSON(ReportBase):
    """JSON report generator class """

    def __init__(self):
        """ JSON report constructor """

        ReportBase.__init__(self)

    def render_report(self):
        """ Create JSON report """

        pass

    def get_report(self):
        """
        Return full JSON report

        @return: str
        """

        return self._report
