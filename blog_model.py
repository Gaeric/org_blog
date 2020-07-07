#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: org_blog.py
# Datetime: Wed Oct 16 22:49:56 2019
# Software: Emacs
# Author:   Gaeric

import re
from bs4 import BeautifulSoup
from datetime import datetime


title_re = re.compile(r'<title>([\s\S]*)<\/title>')
body_re = re.compile(r'<body>([\s\S]*)<\/body>')
summary_re = re.compile(r'<li><a href="#(.*)">(.*?)简介<\/a><\/li>')


class OrgBlog():
    """解析传入的ox-html文件，匹配其title和body
    文件格式必须为html，由调用者保证
    如果title不存在，则返回""
    如果body不存在，则返回ox-html文件的所有内容"""

    def __init__(self, oxhtml):
        with open(oxhtml, 'r', encoding='utf-8') as fp:
            try:
                html_context = fp.read()
            except IOError as ioerr:
                raise f"Read orghtml Failed, Error: {ioerr}"
            else:
                self._html_context = html_context
                title_ma = title_re.search(html_context)
                body_ma = body_re.search(html_context)
                summary_ma = summary_re.search(html_context)
            finally:
                self.org_title = title_ma.group(1) if title_ma else ""
                self.org_content = body_ma.group(1) \
                    if body_ma else html_context
                self._summary_id = "outline-container-" + \
                    summary_ma.group(1) if summary_ma else ""

    @property
    def org_summary(self):
        if self._summary_id == "":
            return ""
        bs = BeautifulSoup(self._html_context, "lxml")
        attrs = {'id': self._summary_id}
        su = bs.find("div", attrs=attrs).find('p')
        return su.string or ""

    @property
    def org_createtime(self):
        bs = BeautifulSoup(self._html_context, "lxml")
        attrs = {'class': "date"}
        createtime_s = bs.find("p", attrs=attrs)
        if createtime_s is None:
            return 0
        createtime = datetime.strptime(createtime_s.string,
                                       "Created: %Y-%m-%d %a %M:%S")
        return createtime
