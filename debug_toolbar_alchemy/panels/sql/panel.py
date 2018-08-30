# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from debug_toolbar import settings as dt_settings
from debug_toolbar.panels import sql as panels
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from .tracking import unwrap_engine, wrap_engine
from .utils import add_newlines, swap_fields


class SQLPanel(panels.SQLPanel):
    @property
    def engines(self):
        try:
            path = dt_settings.get_config()['ALCHEMY_DB_ALIASES']
        except KeyError:
            raise ImproperlyConfigured(
                'Must specify ALCHEMY_DB_ALIASES in DEBUG_TOOLBAR_CONFIG'
            )
        else:
            return import_string(path)()

    def enable_instrumentation(self):
        for alias, engine in self.engines.items():
            wrap_engine(engine, alias, self)

    def disable_instrumentation(self):
        for alias, engine in self.engines.items():
            unwrap_engine(engine, alias, self)

    def record_stats(self, stats):
        for q in stats.get('queries', []):
            if q.get('sql'):
                q['sql'] = add_newlines(swap_fields(q['sql']))
        super(SQLPanel, self).record_stats(stats)

    # TODO reimplement utility views. for now let them blow up
    # @classmethod
    # def get_urls(cls):
    #     return []
