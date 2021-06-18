# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 11:25:52 2021

@author: valer
"""

import requests
from bs4 import BeautifulSoup
import html2text
import codecs

# =============================================================================
# h = html2text.HTML2Text()
# 
# html = function_to_get_some_html()
# text = html2text.html2text(html)
# =============================================================================

# list of URL to experiment the coding (from articles already datamined)
# 4.yaml → 20 → melt
# 5.yaml → 145 → multiple materials (to much data; min max global) + immersion
# 12.yaml → 165 → dia fibre x±y
# 13.yaml → 166 → not about RJS, surprise!!
# 24.yaml → 52 → melt
# Shit can't use a list of url because the site I use uses firewall with login, can't access without it


# =============================================================================
# # Providing url
# url = 'https://www.sciencedirect.com/science/article/pii/S2589234720300154'
#   
# # Creating request object
# req = requests.get(url)
#   
# # Creating soup object
# soup = BeautifulSoup(req.text, 'html.parser')
# 
# # =============================================================================
# # # Text content in inspector
# # text = soup.find_all(text=True)
# # set([t.parent.name for t in text])
# # 
# # # Html text that we do not want (tag, etc.)
# # output = ''
# # blacklist = ['[document]',
# #             'noscript',
# #             'header',
# #             'html',
# #             'meta',
# #             'head', 
# #             'input',
# #             'script',]
# # for t in text:
# #     if t.parent.name not in blacklist:
# #         output += '{} '.format(t)
# #         
# # print(output)
# # =============================================================================
# 
# # To work without html knowledge, convert to easy to read text
# text2 = html2text.html2text(soup)
# =============================================================================

path = './ArticlesHtml/4.html'
f = codecs.open(path, 'r', 'utf-8')
document = BeautifulSoup(f.read(),features='html.parser').get_text()
print(document)
f.close()


