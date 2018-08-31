# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import json
from threading import current_thread
from time import time

import six
from debug_toolbar import settings as dt_settings
from debug_toolbar.utils import get_stack, get_template_info, tidy_stacktrace
from django.utils.encoding import force_text
from sqlalchemy import event
from sqlalchemy.exc import CompileError


trackers = {}


class SQLAlchemyTracker(object):
    def __init__(self, engine, alias):
        self.engine = engine
        self.alias = alias
        self.loggers = {}
        self.tmp = {}

        for i in (
            (self.engine, 'before_execute', self.before_execute),
            (self.engine, 'after_execute', self.after_execute)
        ):
            if not event.contains(*i):
                event.listen(*i)

    def register(self, logger):
        self._before_execute = self._before_execute_
        self._after_execute = self._after_execute_

        self.loggers[current_thread().ident] = logger

    def unregister(self):
        self.loggers.pop(current_thread().ident, None)

        # no loggers left so make handlers very cheap to execute
        if not self.loggers:
            self._before_execute = lambda *args, **kwargs: None
            self._after_execute = lambda *args, **kwargs: None

    def before_execute(self, *args, **kwargs):
        return self._before_execute(*args, **kwargs)

    def after_execute(self, *args, **kwargs):
        return self._after_execute(*args, **kwargs)

    def _before_execute(self, conn, clause, multiparams, params):
        logger = self.loggers.get(current_thread().ident)
        if not logger:
            return

        try:
            clause.start_time = time()
        except AttributeError:
            self.tmp[id(clause)] = time()

    _before_execute_ = _before_execute

    def _after_execute(self, conn, clause, multiparams, params, result):
        logger = self.loggers.get(current_thread().ident)
        if not logger:
            return

        try:
            start_time = clause.start_time
        except AttributeError:
            start_time = self.tmp.pop(id(clause))
        stop_time = time()
        duration = (stop_time - start_time) * 1000
        config = dt_settings.get_config()

        try:
            raw_sql = ' '.join(six.text_type(
                clause.compile(dialect=self.engine.dialect,
                               compile_kwargs={})
            ).splitlines())
        except AttributeError:
            raw_sql = ' '.join(six.text_type(clause).splitlines())

        try:
            sql = ' '.join(six.text_type(
                clause.compile(dialect=self.engine.dialect,
                               compile_kwargs={'literal_binds': True})
            ).splitlines())
        except (CompileError, TypeError, NotImplementedError, AttributeError):
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

        logger.record(**params)

        return params

    _after_execute_ = _after_execute

    def _decode(self, param):
        try:
            return force_text(param, strings_only=True)
        except UnicodeDecodeError:
            return '(encoded string)'


def wrap_engine(engine, alias, panel):
    tracker = trackers.get(alias)
    if not tracker:
        tracker = trackers[alias] = SQLAlchemyTracker(engine, alias)
    tracker.register(panel)


def unwrap_engine(engine, alias, panel):
    tracker = trackers.get(alias, None)
    if tracker:
        tracker.unregister()
