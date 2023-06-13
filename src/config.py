# -*- coding: utf-8 -*-
"""Sample Configuration
"""

# For Maverick
site_prefix = "/"
template = "Galileo"
index_page_size = 10
archives_page_size = 30
fetch_remote_imgs = False
enable_jsdelivr = {
    "enabled": False,
    "repo": "SylverQG/Blogs@gh-pages"
}
locale = "Asia/Shanghai"
category_by_folder = False

# For site
# site_name = "Maverick"
# site_logo = "${static_prefix}android-chrome-512x512.png"
site_build_date = "2023-06-14T12:00+08:00"
author = "SylverQG"
email = "doublc_qluv@163.com"
author_homepage = "https://SylverQG.github.io"
description = "This is Maverick, Theme Galileo."
key_words = ["Maverick", "AlanDecode", "Galileo", "blog"]
language = 'english'
external_links = [
    {
        "name": "SylverQG@Blogs",
        "url": "https://github.com/SylverQG/Blogs",
        "brief": "Put a ping."
    },
    {
        "name": "SylverQG@Blogs",
        "url": "https://github.com/SylverQG/Blogs",
        "brief": "THere is no spoon."
    }
]
nav = [
    {
        "name": "Home",
        "url": "${site_prefix}",
        "target": "_self"
    },
    {
        "name": "Archives",
        "url": "${site_prefix}archives/",
        "target": "_self"
    },
    {
        "name": "About",
        "url": "${site_prefix}about/",
        "target": "_self"
    }
]

social_links = [
    {
        "name": "Twitter",
        "url": "https://twitter.com",
        "icon": "gi gi-twitter"
    },
    {
        "name": "GitHub",
        "url": "https://github.com/SylverQG",
        "icon": "gi gi-github"
    },
    {
        "name": "Weibo",
        "url": "https://weibo.com",
        "icon": "gi gi-weibo"
    }
]

valine = {
    "enable": True,
    "el": '#vcomments',
    "appId": "IKRAfuPq0zrz6Wfje8ahHAIP-gzGzoHsz",
    "appKey": "lFaCWkd4xCs0Ng5UWs1eHNwU",
    "visitor": True,
    "recordIP": True
}

head_addon = 'Put a ping'

footer_addon = ''

body_addon = 'THere is no spoon'
