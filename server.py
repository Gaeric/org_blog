#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: demo.py
# Datetime: Wed Oct 16 23:20:20 2019
# Software: Emacs
# Author:   Gaeric

from flask import Flask
from flask import render_template
from flask import g
from blog_model import OrgBlog
import os
import config
import logging


app = Flask(__name__)
app.config.from_object(config)


# 放到单独的hooks文件中无效
@app.before_request
def get_static_html_list():
    g.HTML_LIST = []
    static_html_dir = os.path.join(os.getcwd(), 'static', config.BLOG_DIR)
    if os.path.isdir(static_html_dir):
        g.HTML_LIST = [filename for filename in os.listdir(static_html_dir)\
                       if filename.endswith("html")]
        g.HTML_LIST.sort()


@app.template_filter('html_title')
def get_static_title(ox_html):
    """函数以启动文件为根目录，ox_html为其在static/static_html/下的相对位置"""
    file_path = os.path.join(os.getcwd(), "static", config.BLOG_DIR, ox_html)
    title = OrgBlog(file_path).org_title
    return title


@app.route('/')
def index():
    return render_template('blog_index.html')


@app.route('/blog/<path:blog_file>')
def show_blog(blog_file):
    """函数以启动文件为根目录，blog_file为其在static/static_html下的相对位置"""
    file_path = os.path.join(os.getcwd(), "static", config.BLOG_DIR, blog_file)
    org_blog = OrgBlog(file_path)

    title = org_blog.org_title
    content = org_blog.org_content
    return render_template("blog_detail.html", title=title, content=content)


if __name__ == "__main__":
    app.run(port=8080)
