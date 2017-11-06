============================
Django Debug Toolbar Alchemy
============================

.. image:: https://badge.fury.io/py/django-debug-toolbar-alchemy.svg
    :target: http://badge.fury.io/py/django-debug-toolbar-alchemy

Django Debug Toolbar panel for SQLAlchemy.

* Free software: MIT license
* GitHub: https://github.com/miki725/django-debug-toolbar-alchemy

Overview
--------

This package completely mimics default Django Debug Toolbar SQL panel
(internally its actually subclassed) but instead of displaying queries done
via Django ORM, SQLAlchemy generated queries are displayed.
Rest of the functionality is the same.

Installing
----------

First install::

    $ pip install django-debug-toolbar-alchemy

Then in your settings::

    # settings.py
    DEBUG_TOOLBAR_PANELS = [
        # other panels
        'debug_toolbar_alchemy.panels.sql.SQLPanel',
        # other panels
    ]

In order to support multiple DB databases, alias getter callable
must be specified in settings::

    # settings.py
    DEBUG_TOOLBAR_CONFIG = {
        'ALCHEMY_DB_ALIASES': '<dot patht to alias getter>',
    }

Alias getter must return a dictionary of aliases as keys and
SQLAlchemy engines as values.
If your application uses global session,
you can get the engine from session instances::

    from myapp.db import session, session_slave

    def alchemy_dbs():
        return {
            'default': session.bind,
            'slave': session_slave.bind,
        }
