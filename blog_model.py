#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: org_blog.py
# Datetime: Wed Oct 16 22:49:56 2019
# Software: Emacs
# Author:   Gaeric

import re


title_re = re.compile(r'<title>([\s\S]*)<\/title>')
body_re = re.compile(r'<body>([\s\S]*)<\/body>')


class OrgBlog():
    """解析传入的ox-html文件，匹配其title和body
    如果title不存在，则返回""
    如果body不存在，则返回ox-html文件的所有内容
"""

    def __init__(self, oxhtml):
        with open(oxhtml, 'r', encoding='utf-8') as fp:
            try:
                html_context = fp.read()
            except IOError as ioerr:
                raise f"Read orghtml Failed, Error: {ioerr}"
            else:
                title_ma = title_re.search(html_context)
                body_ma = body_re.search(html_context)
            finally:
                self.org_title = title_ma.group(1) if title_ma else ""
                self.org_content = body_ma.group(1) \
                    if body_ma else html_context
