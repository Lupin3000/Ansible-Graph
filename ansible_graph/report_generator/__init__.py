# -*- coding: utf-8 -*-
""" Report generator package """

import logging
from .report_plain import ReportPlain


class ReportGenerator(object):
    """ Report generator class """

    __ALLOWED_FORMAT = ['default', 'xml', 'json']

    def __init__(self, report='default'):
        """
        Report generator constructor

        @param report: report output format [default, xml, json]
        @type report: str

        @raise e: TypeError
        @raise e: ValueError
        """

        self.__logger = logging.getLogger(__name__)

        if not isinstance(report, str):
            msg = 'Parameter: report needs to a string'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not report:
            msg = 'Parameter: no report provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        if str(report.lower()) not in self.__ALLOWED_FORMAT:
            msg = 'Parameter: report format not supported'
            self.__logger.error(msg)
            raise ValueError(msg)

        self.__report_format = str(report.lower())
        self.__meta = dict()
        self.__content = dict()
        self.__report = str()

    def set_report_header(self, meta):
        """
        Set report header values

        @param meta: meta for report
        @type meta: dict

        @raise e: TypeError
        @raise e: ValueError
        """

        self.__logger.debug('Set report header - %s', meta)

        if not isinstance(meta, dict):
            msg = 'Parameter: meta needs to a dictionary'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not meta:
            msg = 'Parameter: no meta provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        self.__meta = meta

    def set_report_content(self, content):
        """
        Set report content values

        @param content: content for report
        @type content: dict

        @raise e: TypeError
        @raise e: ValueError
        """

        self.__logger.debug('Set report content - %s', content)

        if not isinstance(content, dict):
            msg = 'Parameter: content needs to a dictionary'
            self.__logger.error(msg)
            raise TypeError(msg)

        if not content:
            msg = 'Parameter: no content provided'
            self.__logger.error(msg)
            raise ValueError(msg)

        self.__content = content

    def get_report(self):
        """
        Generate full test report

        @return: string
        """

        if self.__report_format == 'json':
            self.__logger.info('Parse JSON report')

            pass
        elif self.__report_format == 'xml':
            self.__logger.info('Parse XML report')

            pass
        else:
            self.__logger.info('Parse plain text report')

            plain = ReportPlain()
            plain.set_report_meta(self.__meta)
            plain.set_report_content(self.__content)
            plain.render_report()
            self.__report = plain.get_report()

        return self.__report