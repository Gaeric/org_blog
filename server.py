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
from datetime import datetime
import os
import config


app = Flask(__name__)
app.config.from_object(config)


# 放到单独的hooks文件中无效
@app.before_request
def get_static_html_list():
    g.HTML_LIST = []
    static_html_dir = os.path.join(os.getcwd(), 'static', config.BLOG_DIR)
    if os.path.isdir(static_html_dir):
        g.HTML_LIST = [filename for filename in os.listdir(static_html_dir)
                       if filename.endswith("html")]
        g.HTML_LIST.sort()


@app.template_filter('html_title')
def get_static_title(ox_html):
    """函数以启动文件为根目录，ox_html为其在static/static_html/下的相对位置"""
    file_path = os.path.join(os.getcwd(), "static", config.BLOG_DIR, ox_html)
    title = OrgBlog(file_path).org_title
    return title


@app.template_filter('html_summary')
def get_static_summary(ox_html):
    """函数以启动文件为根目录，ox_html为其在static/static_html/下的相对位置"""
    file_path = os.path.join(os.getcwd(), 'static', config.BLOG_DIR, ox_html)
    summary = OrgBlog(file_path).org_summary
    return summary


@app.template_filter('html_content')
def get_static_content(ox_html):
    """函数以启动文件为根目录，ox_html为其在static/static_html/下的相对位置"""
    file_path = os.path.join(os.getcwd(), "static", config.BLOG_DIR, ox_html)
    content = OrgBlog(file_path).org_content
    return content


# datetime.strptime("2020-07-05 Sun 20:34", "%Y-%m-%d %a %M:%S")
@app.template_filter('html_time')
def html_time(ox_html):
    file_path = os.path.join(os.getcwd(), 'static', config.BLOG_DIR, ox_html)
    createtime = OrgBlog(file_path).org_createtime
    return handle_time(createtime)


def handle_time(time):
    """
    time 距离现在的时间：
    1. 如果时间小于1分钟，则显示刚刚
    2. 如果时间小于1小时，则显示×××分钟前
    3. 如果时间小于24小时，则显示×××小时前
    4. 如果时间小于24*30小时，则显示×××天前
    5. 否则，则显示具体的日期（格式为××××年××月××日）
    """
    if isinstance(time, datetime):
        current_time = datetime.now()
        timestamp = (current_time - time).total_seconds()
        if timestamp < 60:
            return '刚刚'
        elif timestamp >= 60 and timestamp < 3600:
            minutes = timestamp / 60
            return f'{int(minutes)}分钟前'
        elif timestamp >= 3600 and timestamp < 86400:
            hours = timestamp / 3600
            return f'{int(hours)}小时前'
        elif timestamp >= 86400 and timestamp < 2592000:
            days = timestamp / 86400
            return f'{int(days)}天前'
        else:
            return time.strftime('%Y年%m月%d日')
        pass
    else:
        return time


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
