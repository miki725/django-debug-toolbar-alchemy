# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from debug_toolbar.panels import sql as panels
from django.conf.urls import url

from .tracking import unwrap_engine, wrap_engine
from .utils import add_newlines, get_connections, swap_fields
from .views import sql_explain, sql_select


class SQLPanel(panels.SQLPanel):
    template = "debug_toolbar/panels/sql-alchemy.html"

    @property
    def panel_id(self):
        return "Alchemy" + super(SQLPanel, self).panel_id

    @property
    def engines(self):
        return get_connections()

    def enable_instrumentation(self):
        for alias, engine in self.engines.items():
            wrap_engine(engine, alias, self)

    def disable_instrumentation(self):
        for alias, engine in self.engines.items():
            unwrap_engine(engine, alias, self)

    def record_stats(self, stats):
        for q in stats.get("queries", []):
            if q.get("sql"):
                q["sql"] = add_newlines(swap_fields(q["sql"]))
        super(SQLPanel, self).record_stats(stats)

    @classmethod
    def get_urls(cls):
        return [
            url(r"^sql_alchemy_select/$", sql_select, name="sql_alchemy_select"),
            url(r"^sql_alchemy_explain/$", sql_explain, name="sql_alchemy_explain"),
        ]
