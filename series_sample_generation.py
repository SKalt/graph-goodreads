#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetches sample goodreads series.show data and transforms it to JSON.
Created on Sat Aug  5 12:28:24 2017

@author: steven
"""

import requests
from lxml import etree
import json

def recursive_dict(element):
    """
    Recursively transform an lxml.etree._Element into a dict
    See http://lxml.de/FAQ.html#how-can-i-map-an-xml-tree-into-a-dict-of-dicts
    Overwrites repeated child tags.
    """
    return element.tag, dict(map(recursive_dict, element)) or element.text

#%%
if __name__ == '__main__':
    r = requests.get(
        'https://www.goodreads.com/series/40321-drina?' + 
        'format=xml&key=lCUhWljJn1WuCZD6khMl1A'
    )
    raw_xml = r.text.replace('<?xml version="1.0" encoding="UTF-8"?>\n', '')
    xml = etree.fromstring(raw_xml)
    _, rd = recursive_dict(xml)
    blacklist = ['series_works', 'Request']
    series_data = {k:v for k,v in rd.items() if k not in blacklist}
    series_data['series_works'] = []
    for work in xml.xpath('//series_work'):
        _, rd = recursive_dict(work)
        series_data['series_works'].append(rd)
    with open('series_data_sample.json', 'w') as f:
        f.write(json.dumps(series_data))

#%%
