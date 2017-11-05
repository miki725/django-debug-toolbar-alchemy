# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import re


def swap_fields(sql):
    expr = (
        r'(JOIN</strong> [\w\d\.]+'
        r'(?: <strong>AS</strong> [\w\d\.]+)? <strong>ON</strong> )'
        r'((?:[\w\d\.]+ = [&#;\'"\w\d\.]+(?: <strong>AND</strong> )?)+)'
    )
    subs = (
        r'\1'
        r'<a class="djDebugUncollapsed djDebugToggle" href="#">'
        r'&#8226;&#8226;&#8226;'
        r'</a> '
        r'<a class="djDebugCollapsed djDebugToggle" href="#">\2</a> '
    )
    return re.sub(expr, subs, sql)


def add_newlines(sql):
    statements = [
        '<strong>FROM</strong>',
        '<strong>JOIN</strong>',
        '<strong>LEFT OUTER JOIN</strong>',
        '<strong>RIGHT OUTER JOIN</strong>',
        '<strong>WHERE</strong>',
        '<strong>GROUP BY</strong>',
        '<strong>ORDER BY</strong>',
        '<strong>LIMIT</strong>',
    ]
    for s in statements:
        sql = sql.replace(s, '<br/>{}'.format(s))
    return sql
