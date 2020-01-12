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
    static_html_dir = os.path.join(os.getcwd(), 'static', config.BLOG_DIR)
    if os.path.isdir(static_html_dir):
        static_html_list = os.listdir(static_html_dir)
        try:
            # 删除.gitkeep
            static_html_list.remove(".gitkeep")
        except ValueError:
            logging.info(f"don't have .gitkeep")
        finally:
            g.HTML_LIST = static_html_list
            print(g.HTML_LIST)
    else:
        g.HTML_LIST = ""


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
    print(file_path)
    org_blog = OrgBlog(file_path)

    title = org_blog.org_title
    content = org_blog.org_content
    return render_template("blog_detail.html", title=title, content=content)


if __name__ == "__main__":
    app.run(port=8080)
