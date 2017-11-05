# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import json
from threading import local
from time import time

import six
from debug_toolbar import settings as dt_settings
from debug_toolbar.utils import get_stack, get_template_info, tidy_stacktrace
from django.utils.encoding import force_text
from sqlalchemy import event
from sqlalchemy.exc import CompileError


state = local()


class SQLAlchemyTracker(object):
    def __init__(self, engine, alias, logger):
        self.engine = engine
        self.alias = alias
        self.logger = logger

        self.register()

    def register(self):
        event.listen(self.engine, 'before_execute', self.before_execute)
        event.listen(self.engine, 'after_execute', self.after_execute)

    def unregister(self):
        event.remove(self.engine, 'before_execute', self.before_execute)
        event.remove(self.engine, 'after_execute', self.after_execute)

    def before_execute(self, conn, clause, multiparams, params):
        clause.start_time = time()

    def after_execute(self, conn, clause, multiparams, params, result):
        start_time = clause.start_time
        stop_time = time()
        duration = (stop_time - start_time) * 1000
        config = dt_settings.get_config()

        raw_sql = ' '.join(six.text_type(
            clause.compile(dialect=self.engine.dialect,
                           compile_kwargs={})
        ).splitlines())
        try:
            sql = ' '.join(six.text_type(
                clause.compile(dialect=self.engine.dialect,
                               compile_kwargs={'literal_binds': True})
            ).splitlines())
        except (CompileError, TypeError, NotImplementedError):
            # not all queries support literal_binds
            sql = raw_sql

        _params = ''
        try:
            _params = json.dumps(list(map(self._decode, params)))
        except Exception:
            pass  # object not JSON serializable

        if config['ENABLE_STACKTRACES']:
            stacktrace = tidy_stacktrace(reversed(get_stack()))
        else:
            stacktrace = []

        template_info = get_template_info()

        params = {
            'vendor': conn.dialect.name,
            'alias': self.alias,
            'sql': sql,
            'duration': duration,
            'raw_sql': raw_sql,
            'params': _params,
            'stacktrace': stacktrace,
            'start_time': start_time,
            'stop_time': stop_time,
            'is_slow': duration > config['SQL_WARNING_THRESHOLD'],
            'is_select': sql.lower().strip().startswith('select'),
            'template_info': template_info,
        }

        self.logger.record(**params)

        return params

    def _decode(self, param):
        try:
            return force_text(param, strings_only=True)
        except UnicodeDecodeError:
            return '(encoded string)'


def wrap_engine(engine, alias, panel):
    if not hasattr(state, 'trackers'):
        state.trackers = {}

    if alias in state.trackers:
        return
    state.trackers[alias] = SQLAlchemyTracker(engine, alias, panel)


def unwrap_engine(engine, alias):
    tracker = getattr(state, 'trackers', {}).pop(alias, None)
    if tracker:
        tracker.unregister()
        del tracker
