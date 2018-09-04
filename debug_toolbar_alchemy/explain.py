# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import six
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.base import Executable


class explain(Executable, ClauseElement):
    def __init__(self, sql, bind):
        self.sql = sql
        self._bind = bind

    def execute(self, *multiparams, **params):
        e = self.bind
        handler = getattr(self, "execute_{}".format(e.dialect.name), None)
        if handler is not None:
            return handler(*multiparams, **params)
        else:
            return e.execute(six.text_type(self.compile(dialect=e.dialect)), *multiparams, **params)

    def execute_oracle(self, *multiparams, **params):
        # actually calls EXPLAIN which stores results in intermediate table
        # which we retrieve on subsequent call
        super(explain, self).execute()
        return self.bind.execute("select * from table(dbms_xplan.display)")


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


@compiles(explain, "oracle")
def pg_explain(element, compiler, **kw):
    sql = "EXPLAIN PLAN FOR "
    return sql + element.sql
