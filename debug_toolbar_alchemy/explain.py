# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.base import Executable


class explain(Executable, ClauseElement):
    def __init__(self, sql):
        self.sql = sql


@compiles(explain)
def generic_explain(element, compiler, **kw):
    return "EXPLAIN " + element.sql


@compiles(explain, "sqlite")
def sqlite_explain(element, compiler, **kw):
    return "EXPLAIN QUERY PLAN " + element.sql


@compiles(explain, "postgresql")
def pg_explain(element, compiler, **kw):
    sql = "EXPLAIN "
    if element.sql.lower().startswith("select"):
        sql += "ANALYZE "
    return sql + element.sql
